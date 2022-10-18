# algorithms: first come first serve, shortest job first, shortest remaining time first, round robin

from typing import List, Optional, Type
from base_queue import Queue
from process import Process
from sink_queue import SinkQueue
from block_queue import BlockingQueue

class CPU:
    t: int = 0

    def __init__(self, cpu_algo:Type[Queue], q_algo:Type[Queue], processes:List[Process], blocked_time:int, quantum:int, priority:bool, preemptive:bool, max_time:int) -> None:
        self.max_time: int = max_time
        self.processes: List[Process] = processes

        self.cpu:Queue = cpu_algo(quantum, priority, preemptive, max_time)
        self.block: BlockingQueue = BlockingQueue(blocked_time, quantum, max_time)
        self.ready: Queue = q_algo(quantum, priority, preemptive, max_time)
        for p in self.processes:
            self.ready.add(p)
        
        self.q_list: List[Queue] = [
            self.ready,
            self.cpu,
            self.block
        ]
        self.update_list: List[Queue] = [
            self.cpu,
            self.block
        ]
        self.terminated_q: SinkQueue = SinkQueue(quantum, priority,preemptive, max_time)
    
    def update(self) -> bool:
        
        min_time: int = self.max_time
        for q in self.update_list:
            peek_time: int = q.min_peek_time()
            min_time = min(min_time, peek_time)
            # print("time:", peek_time)
        # print("dt:", min_time)
        if min_time < self.max_time:
            self.t += min_time
            for q in self.update_list:
                q.update(min_time)
        
        self.move_processes()
        return len(self.terminated_q) != len(self.q_list)
    
    def move_process(self, src:Queue, dest:Queue, prepend:bool=False) -> Optional[Process]:
        p: Optional[Process] = src.poll()
        if p is None: return
        if p.terminated:
            self.terminated_q.add(p)
        else:
            dest.add(p, prepend)
        return p
    
    def move_processes(self) -> None:
        # if cpu is done -> move to block
        if self.cpu.is_ready():
            self.cpu.inc()
            self.move_process(self.cpu, self.block)
        
        # if block is ready and cpu need check -> recheck cpu
        if self.block.is_ready() and self.ready.check_cpu():
            self.move_process(self.cpu, self.ready, True)

        while self.block.is_ready():
            p:Optional[Process] = self.move_process(self.block, self.ready)
            if p is not None: p.unblock()
        
        if self.cpu.limit_cpu():
            p = self.move_process(self.cpu, self.ready)
            if p is not None:
                p.cpu_time = 0
        
        if self.cpu.is_empty() and not self.ready.is_empty():
            self.move_process(self.ready, self.cpu)
    
    def __str__(self) -> str:
        return "{}, {}, {}, {}, {}".format(self.t, self.cpu, self.ready, self.block, self.terminated_q)
