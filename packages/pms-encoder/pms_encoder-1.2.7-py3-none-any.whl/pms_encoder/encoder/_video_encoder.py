import os
import asyncio
import ffmpeg
import json
import pms_inference_engine as E

from loguru import logger
from queue import Queue
from .processor import _video_processor as v_processor
from .repository._file_status_repo import *
from .repository._video_meta_repo import insert_inferenced_file_meta
from .utils import _delete_file_util as dfu
from .redis._progress import save_progress

from ray.util.queue import Queue as RayQueue
# if os.getenv("COMPUTE_UNIT") == "NPU":
#     import pms_furiosa_processor
#     from pms_furiosa_processor._const import NPU_DEVICES
# elif os.getenv("COMPUTE_UNIT") == "GPU":
#     import pms_nvidia_processor


class VideoEncoder:
    def __init__(
        self,
        processor_type: str,
        number_of_processors: int,
        processor_kwargs: dict,
        head_ip: str,
        work_dir: str,
        scheduling_max: int,
        scheduling_timeout: int,
        encoder_resource: dict,
        processor_resource: dict,
        processor_count: int,
        processor_concurrency: int,
        processor_device: str,
        model_alias: str,
        max_queue_size: int,
        compute_unit: str,
        ray_queue: RayQueue,
    ):
        logger.debug("initiate video encoder")
        
        if str(compute_unit) == "NPU":
            import pms_furiosa_processor
            from pms_furiosa_processor._const import NPU_DEVICES
        elif str(compute_unit) == "GPU":
            import pms_nvidia_processor
            
        self.processor_type = processor_type
        self.number_of_processors = number_of_processors
        self.processor_kwargs=processor_kwargs
        self.max_queue_size = max_queue_size
        self.enqueue = Queue(
            maxsize=self.max_queue_size,
        )
        self.dequeue = Queue(
            maxsize=self.max_queue_size,
        )
        self.spand_queue = Queue(
            maxsize=self.max_queue_size,
        )
        self.redis_data = None  # json.dumps(data)
        self.meta_data = None
        self.audio = "N"
        self.compute_unit = compute_unit
        self.work_dir = work_dir
        self.ray_queue = ray_queue
        
    async def __call__(self, redis_data) -> dict:
        logger.debug("Video Encoder Call")
        self.redis_data = redis_data
        
        # change status start
        # set_start_status(redis_data["fileKey"])

        probe = ffmpeg.probe(self.redis_data["filePath"])
        self.audio = next(
            ("Y" for stream in probe["streams"] if stream["codec_type"] == "audio"),
            "N"
        )
        
        self.meta_data = next(s for s in probe["streams"] if s["codec_type"] == "video")
        # Calc framerate
        frame_rate_fraction = self.meta_data["r_frame_rate"]
        frame_rate_numerator, frame_rate_denominator = map(
            int, frame_rate_fraction.split("/")
        )
        frame_rate = frame_rate_numerator / frame_rate_denominator
        self.meta_data["frame_rate"] = frame_rate
        
        # check nb_frames
        if "nb_frames" not in self.meta_data:
            duration = float(self.meta_data["duration"])
            self.meta_data["nb_frames"] = int(duration * frame_rate)
        
        # initiate engine
        engine = E.Engine(
            processor_type=self.processor_type,
            number_of_processors=len(NPU_DEVICES) if str(self.compute_unit) == "NPU" else self.number_of_processors,
            processor_kwargs=self.processor_kwargs,
        )
        
        # processing
        await asyncio.gather(
            asyncio.to_thread(
                v_processor.split_frames,
                redis_data=self.redis_data,
                meta_data=self.meta_data,
                audio=self.audio,
                enqueue=self.enqueue,
                max_queue_size=self.max_queue_size,
                work_dir=self.work_dir,
            ),
            asyncio.to_thread(
                engine.run,
                dequeue=self.enqueue,
                enqueue=self.dequeue
            ),
            asyncio.to_thread(
                v_processor.spand_frames,
                n_worker=engine.n_worker,
                dequeue=self.dequeue,
                spand_queue=self.spand_queue,
            ),
            asyncio.to_thread(
                v_processor.merge_frames,
                redis_data=self.redis_data,
                meta_data=self.meta_data,
                spand_queue=self.spand_queue,
                ray_queue=self.ray_queue,
                work_dir=self.work_dir,
            ),
            return_exceptions=False,
        )

        # set progress 100
        save_progress(
            self.redis_data["fileKey"],
            json.dumps({"progress": "100", "time": "0"}),
            self.ray_queue
        )
        
        # two_pass_encoding
        if self.redis_data["bestQuality"] == "N" and self.redis_data["twoPass"] == "Y":
            await asyncio.to_thread(
                v_processor.two_pass_encoding,
                redis_data=self.redis_data,
                meta_data=self.meta_data,
                work_dir=self.work_dir,
            )
            
        # merge audio
        v_processor.merge_audio(self.redis_data, self.audio, self.work_dir)
        
        # inferenced metadata save
        # v_processor.save_inferenced_meta(self.redis_data, self.meta_data, self.audio, self.work_dir)
        inferenced_data = v_processor.get_inferenced_meta(self.redis_data, self.meta_data, self.audio, self.work_dir)
        
        # downscale file & move download folder
        v_processor.downscale_and_upload(self.redis_data, self.meta_data, self.work_dir)
        
        # delete worked files
        dfu.delete_video_temp_files(self.redis_data, self.work_dir)
        
        # delete original files
        # dfu.delete_upload_files(self.redis_data)
        
        # change status end
        # set_success_status(redis_data["fileKey"])
        
        return {
            "redis_data": self.redis_data,
            "original_data": self.meta_data,
            "inferenced_data": inferenced_data["inferenced_data"],
            "format_data": inferenced_data["format_data"],
            "file_size": inferenced_data["inferenced_size"],
            "audio": self.audio
        }
        