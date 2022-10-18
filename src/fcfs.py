from base_queue import Queue

class FCFS(Queue):
    def less_than_idx(self, a:int, b:int) -> bool:
        return a < b