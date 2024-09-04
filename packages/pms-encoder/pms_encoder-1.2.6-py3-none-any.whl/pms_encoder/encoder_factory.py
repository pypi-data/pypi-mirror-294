import uvloop
import cv2
import asyncio
import ray
 
import os

from typing import Union
from loguru import logger
from .encoder._video_encoder import VideoEncoder
from .encoder._image_encoder import ImageEncoder
from pms_inference_engine import (
    SleepAndPassProcessor,
    register,
    EngineIOData,
    Engine,
    EngineIOData,
    StaticProcessorFactory,
)
from ._config import *
 
from ray.util.queue import Queue as RayQueue
 
 
@register
class RzSleepAndPassProcessor(SleepAndPassProcessor):
    def __init__(
        self, concurrency: int, index: int, scale: float, sleep_time: float = 0.1
    ) -> None:
        super().__init__(concurrency, index, sleep_time)
        self.scale = scale
 
    async def _run(self, input_data: EngineIOData) -> EngineIOData:
        await asyncio.sleep(self._sleep_time)
        frame = input_data.frame
        h, w, c = frame.shape
        resize_width = int(w * self.scale)
        resize_height = int(h * self.scale)
        frame_rz = cv2.resize(frame[:, :, :3], (resize_width, resize_height))
        return EngineIOData(input_data.frame_id, frame_rz)
 
 
class EncoderFactory:
    @staticmethod
    def create_encoder(
        redis_data: dict,
        number_of_processors: int,
        processor_kwargs: dict,
    ):
        processor_type_map = {
            "M001": "Ray_DPIRProcessor",
            "M002": "Ray_DRURBPNSRF3Processor",
            "M003": "Ray_DRURBPNSRF5Processor",
        }
        processor_type = processor_type_map.get(
            redis_data.get("model"), "Ray_SleepAndPassProcessor"
        )
 
        if redis_data.get("contentType") == "image":
            logger.debug("image encoder")
            return ImageEncoder(
                processor_type=processor_type,  # processor_key,
                number_of_processors=number_of_processors,
                processor_kwargs=processor_kwargs,
            )
        else:
            logger.debug("video encoder")
            return VideoEncoder(
                processor_type=processor_type,  # processor_key,
                number_of_processors=number_of_processors,
                processor_kwargs=processor_kwargs,
            )
 
        logger.debug("encoder init end")
 
 
@ray.remote(**RAY_ENCODER_ACTOR_OPTIONS)
class RayEncoderFactory:
    def __init__(
        self,
        redis_data: dict,
        number_of_processors: int,
        model_name: str,
        model_alias: str,
        processor_type: str,
        processor_kwargs: dict,
        head_ip: str,
        work_dir: str,
        upload_dir: str,
        download_dir: str,
        scheduling_max: int,
        scheduling_timeout: int,
        encoder_resource: dict,
        processor_resource: dict,
        processor_count: int,
        processor_concurrency: int,
        processor_device: str,
        # model_alias: str,
        max_queue_size: int,
        compute_unit: str,
        ray_queue: RayQueue,
    ) -> None:
        import pms_model_manager as mml
 
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        model_key = (
            StaticProcessorFactory.get_local_processor_type(processor_type)
            if StaticProcessorFactory.is_wrapped_ray(processor_type)
            else processor_type
        )
        if model_key in [SleepAndPassProcessor.__name__]:
            assert (
                model_name == ""
            ), f"ERROR, Processor[{model_key}]'s model_name must be emptry string."
            assert (
                model_alias == ""
            ), f"ERROR, Processor[{model_key}]'s model_alias must be emptry string."
        else:
            model_manager = mml.ModelManager(ROOT_DIR)
            model_manager.download(model_name, model_alias)
 
        logger.debug(f"Processor kwargs : {processor_kwargs}")
        if redis_data["contentType"] == "video":
            self.encoder = VideoEncoder(
                processor_type=processor_type,  # processor_key,
                number_of_processors=number_of_processors,
                processor_kwargs=processor_kwargs,
                head_ip=head_ip,
                work_dir=work_dir,
                scheduling_max=scheduling_max,
                scheduling_timeout=scheduling_timeout,
                encoder_resource=encoder_resource,
                processor_resource=processor_resource,
                processor_count=processor_count,
                processor_concurrency=processor_concurrency,
                processor_device=processor_device,
                model_alias=model_alias,
                max_queue_size=max_queue_size,
                compute_unit=compute_unit,
                ray_queue=ray_queue,
            )
        else:
            self.encoder = ImageEncoder(
                processor_type=processor_type,  # processor_key,
                number_of_processors=number_of_processors,
                processor_kwargs=processor_kwargs,
                head_ip=head_ip,
                work_dir=work_dir,
                scheduling_max=scheduling_max,
                scheduling_timeout=scheduling_timeout,
                encoder_resource=encoder_resource,
                processor_resource=processor_resource,
                processor_count=processor_count,
                processor_concurrency=processor_concurrency,
                processor_device=processor_device,
                model_alias=model_alias,
                max_queue_size=max_queue_size,
                compute_unit=compute_unit,
            )
 
    async def run(self, *args, **kwrags) -> Union[dict, None]:
        encoder = self.encoder
        return await encoder(*args, **kwrags)