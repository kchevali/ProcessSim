from typing import List, Optional
from process import Process

class Queue:
    def __init__(self, quantum:int, priority:bool, preemptive:bool, max_time:int) -> None:
        self.array:List[Process] = []
        self.quantum: int = quantum
        self.priority: bool = priority
        self.preemptive: bool = preemptive
        self.max_time: int = max_time
    
    def add(self, p:Process, prepend:bool=False) -> None:
        if prepend:
            self.array.insert(0, p)
        else:
            self.array.append(p)
    
    def peek_time(self) -> int:
        p:Optional[Process] = self.peek()
        return self.max_time if p is None else p.peek_rem_time()
    
    def min_peek_time(self) -> int:
        min_time: int = self.max_time
        for p in self.array:
            min_time = min(min_time, p.peek_rem_time())
        return min_time
    
    def peek(self) -> Optional[Process]:
        if not self.array: return None
        idx:Optional[int] = self.next()
        if idx is None: return None
        return self.array[idx]
    
    def poll(self) -> Optional[Process]:
        p:Optional[Process] = self.peek()
        if p is None: return None
        self.array.remove(p)
        return p
    
    def inc(self) -> None:
        p:Optional[Process] = self.peek()
        # print("Q INC:", p)
        if p is None: return
        p.inc()
        # print("Q INC'd:", p)
    
    def is_empty(self) -> bool:
        return len(self.array) == 0
    
    def __len__(self) -> int:
        return len(self.array)
    
    def is_ready(self) -> bool:
        p:Optional[Process] = self.peek()
        if p is None: return False
        return p.is_ready()
    
    def update(self, dt:int) -> None:
        for p in self.array:
            p.update(dt)

    def next(self) -> Optional[int]:
        best:Optional[int] = None
        for i in range(len(self.array)):
            if best is None or self.less_than_priority(i, best):
                best = i
        return best
    
    def less_than_idx(self, a:int, b:int) -> bool:
        return self.less_than(self.array[a], self.array[b])
    
    def less_than(self, a:Process, b:Process) -> bool:
        return True
    
    def less_than_priority(self, a:int, b:int) -> bool:
        p: Process = self.array[a]
        q: Process = self.array[b]
        less_priority: bool = self.priority and p.priority < q.priority
        equal_priority: bool = not self.priority or p.priority == q.priority
        return less_priority or (equal_priority and self.less_than_idx(a, b))
    
    def check_cpu(self) -> bool:
        return self.preemptive
    
    def limit_cpu(self) -> bool:
        return False
    
    def __str__(self) -> str:
        return "{}".format("/" if self.is_empty() else " ".join([str(p) for p in self.array]))