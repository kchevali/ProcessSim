from typing import Tuple


class Process:
    idx:int = 0
    rem_time:int = 0
    blocked_time:int = 0
    cpu_time:int = 0
    blocked:bool = False
    terminated:bool = False
    class_id:int = 1

    def __init__(self, priority:int, max_time:int, *times:int) -> None:
        self.id: int = Process.class_id
        Process.class_id += 1
        self.priority:int = priority
        self.max_time: int = max_time
        self.times: Tuple[int] = times
        self.inc()
    
        """_summary_ returns if element should be popped
        """
    def update(self, dt:int) -> None:
        if self.terminated or dt == 0: return

        if self.blocked:
            self.blocked_time -= dt
        else:
            self.rem_time -= dt
            self.cpu_time += dt
    
    def is_ready(self) -> bool:
        return (self.blocked and self.blocked_time <= 0) or (not self.blocked and self.rem_time <= 0)
    
    def inc(self) -> None:
        if not self.is_ready(): return
        # print("P INC")

        if self.idx < len(self.times):
            self.rem_time = self.times[self.idx]
            # print(self, "INC:", self.idx, self.rem_time)
            self.idx += 1
            self.cpu_time = 0
        else:
            self.terminated = True
    
    def peek_rem_time(self) -> int:
        return self.max_time if self.terminated else (self.blocked_time if self.blocked else self.rem_time)
    
    def block(self, blocked_time:int) -> None:
        self.blocked_time = blocked_time
        self.blocked = True
    
    def unblock(self) -> None:
        self.blocked = False
    
    def __str__(self) -> str:
        return "P{}({}){}".format(self.id, self.rem_time, "B{}".format(self.blocked_time) if self.blocked else "")
    
    