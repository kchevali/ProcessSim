from base_queue import Queue
from process import Process

class SJF(Queue):
    def less_than(self, a:Process, b:Process) -> bool:
        return a.rem_time < b.rem_time or (a.rem_time == b.rem_time and a.id < b.id)
