from typing import List, Optional

import time

from .conn import get_redis_connection


class RedisQueue:
    """
    Class to implement queue using Redis Sorted Sets

    Attributes:
        key (str): REDIS KEY or QUEUE Name
        rc: Redis Connection
        sleep_time (int): Sleep time for queue
    """

    def __init__(self, key: str, host: str, port: int, sleep_time: int = 5) -> None:
        self.key = key
        self.rc = get_redis_connection(host, port)
        self.sleep_time = sleep_time

    def push_to_pipeline(self, object_id: str, score: Optional[float] = None) -> None:
        """
        Push item to Redis Queue
        Args:
            object_id (str): The item to push into queue.
            score (float): Priority Score in the queue
        """
        if not score:
            score = time.time()
        if not self.rc.zscore(self.key, object_id):
            self.rc.zadd(self.key, {object_id: score})

    def consumer_pipeline(self) -> None:
        """
        Queue Consumer
        Function which consumes the queue and process the items
        """
        min_score = 0
        while True:
            max_score = time.time()
            result = self.rc.zrangebyscore(
                self.key, min_score, max_score, start=0, num=1, withscores=True
            )
            if len(result) == 1:
                if self.rc.zrem(self.key, result[0][0]):
                    self.process_result(result)
            else:
                print(
                    "Nothing found in {} sleeping for {} "
                    "seconds".format(self.key, self.sleep_time)
                )
                time.sleep(self.sleep_time)

    @staticmethod
    def process_result(result: List[List[int]]) -> int:
        """
        Process the element in the queue
        """
        print(result)
        return 0

    def __str__(self):
        return "{1}: Queue :{0} with current length {2}".format(
            self.__class__, self.key, self.rc.zcard(self.key)
        )
