from typing import Optional
from base_queue import Queue
from process import Process

class BlockingQueue(Queue):

    def __init__(self, blocked_time:int, quantum:int, max_time:int) -> None:
        super().__init__(quantum, False, False, max_time)
        self.blocked_time: int = blocked_time
    
    def add(self, p:Process, prepend:bool=False) -> None:
        super().add(p, prepend)
        p.block(self.blocked_time)
        # print("Blocked:", p)
    
    def less_than(self, a:Process, b:Process) -> bool:
        return a.blocked_time < b.blocked_time or (a.blocked_time == b.blocked_time and a.id < b.id)
    
    def next(self) -> Optional[int]:
        idx: Optional[int] = super().next()
        # print("NEXT BLOCK IDX:", idx)
        if idx is None: return
        p: Process = self.array[idx]
        # print("NEXT BLOCK P:", p, p.is_ready())
        if not p.is_ready(): return
        return idx
