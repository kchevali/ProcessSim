from base_queue import Queue

class SinkQueue(Queue):
    def is_ready(self) -> bool:
        return False
