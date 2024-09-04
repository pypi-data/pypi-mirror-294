import os
import asyncio
import pms_inference_engine as E
# if os.getenv("COMPUTE_UNIT") == "NPU":
#     import pms_furiosa_processor
# elif os.getenv("COMPUTE_UNIT") == "GPU":
#     import pms_nvidia_processor

from loguru import logger
from queue import Queue
from .processor import _image_processor as i_processor
from .repository._file_status_repo import *
from .utils import _delete_file_util as dfu

class ImageEncoder:
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
    ):
        logger.debug("initiate image encoder")
        
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
        self.redis_data = None
        self.meta_data = None
        self.frame_map = {}
        self.compute_unit = compute_unit
        self.work_dir = work_dir
        
    async def __call__(self, redis_data) -> None:
        self.redis_data = redis_data
        # set_start_status(redis_data["fileKey"])
        
        # initiate engine
        engine = E.Engine(
            processor_type=self.processor_type,
            number_of_processors=self.number_of_processors,
            processor_kwargs=self.processor_kwargs,
        )
        
        await asyncio.gather(
            asyncio.to_thread(
                i_processor.insert_image_enqueue,
                redis_data=self.redis_data,
                frame_map=self.frame_map,
                enqueue=self.enqueue,
            ),
            asyncio.to_thread(
                engine.run,
                dequeue=self.enqueue,
                enqueue=self.dequeue,
            ),
            asyncio.to_thread(
                i_processor.spand_frames,
                n_worker=engine.n_worker,
                dequeue=self.dequeue,
                spand_queue=self.spand_queue,
            ),
            asyncio.to_thread(
                i_processor.save_frames,
                redis_data=self.redis_data,
                frame_map=self.frame_map,
                spand_queue=self.spand_queue,
                work_dir=self.work_dir,
            ),
            return_exceptions=False,
        )
        
        if self.redis_data["combined"] == "Y":
            i_processor.zip_combined_files(self.redis_data, self.work_dir)

        i_processor.upload_workdone_files(self.redis_data, self.work_dir)
        
        # delete original files
        # dfu.delete_upload_files(self.redis_data)
        
        # change status end
        # set_success_status(self.redis_data["fileKey"])
        
        