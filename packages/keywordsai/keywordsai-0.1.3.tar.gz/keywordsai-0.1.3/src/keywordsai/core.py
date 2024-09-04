from threading import Thread
from .utils.debug_print import *
from typing import List, Literal
from .constants import *
from queue import Queue
from threading import Lock

class UploadConsumer(Thread):
    _queue = Queue()
    state: Literal["running", "paused", "stopped"] = "running"

    def __init__(self):
        Thread.__init__(self)
    
    def run(self):

        while self.state == "running":
            data = self._queue.get()
            if data:
                self._send_to_keywords(data)
                self._queue.task_done()
            
    def _send_to_keywords(self, data):
        print_info(f"Sending data to KeywordsAI: {data}")

class KeywordsAI:
    _consumers: List[UploadConsumer] = []
    _lock = Lock()
    _singleton = True

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(KeywordsAI, cls).__new__(cls)
        else:
            if cls._singleton:
                print_info("Singleton instance already exists")
                return cls._instance
            else:
                cls._instance = super(KeywordsAI, cls).__new__(cls)
        
        return cls._instance

    def __init__(self) -> None:
        for _ in range(KEYWORDSAI_NUM_THREADS):
            self._consumers.append(UploadConsumer())

        
    def initialize(self):
        for consumer in self._consumers:
            consumer.start()
