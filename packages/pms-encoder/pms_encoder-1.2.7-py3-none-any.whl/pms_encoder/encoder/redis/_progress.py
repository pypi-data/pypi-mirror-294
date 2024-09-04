# from ...common._redis_client import RedisClient
import redis
import os
import json
from ray.util.queue import Queue as RayQueue

def save_progress(
    file_key: str,
    progress: str,
    ray_queue: RayQueue,
) -> None:
    # client = RedisClient.get_instance()
    # client.set(
    #     name=f"pms:encoder:progress:{file_key}",
    #     value=progress,
    #     ex=1800
    # )
    # progress_data = json.loads(progress)
    ray_queue.put(
        {
            "key": f"pms:encoder:progress:{file_key}",
            "value": progress,
            # "progress": progress_data['progress'],
            # "time": progress_data['time']
        }
    )