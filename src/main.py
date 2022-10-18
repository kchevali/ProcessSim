from process import Process
from cpu import CPU
from all_queue import *

def main() -> None:
    max_time:int = 250
    blocked_time:int = 6
    quantum: int = 5
    priority:bool = True
    preemptive:bool = True
    # processes: list[Process] = [
    #     Process(max_time, 14, 12, 17),
    #     Process(max_time, 2,2,2,3),
    #     Process(max_time, 6,3,8,2)
    # ]
    processes: list[Process] = [
        Process(1, max_time, 14, 12, 17),
        Process(0, max_time, 2,2,2,3,2,2,2,3),
        Process(0, max_time, 6,3,8,2,1,3,4,9,7)
    ]

    cpu: CPU = CPU(RR, FCFS, processes, blocked_time, quantum, priority, preemptive, max_time)
    print("'Time','CPU','Ready Queue','Waiting Queue','Termination'")

    max_iterations:int = max_time
    # print(cpu)
    while cpu.update() and max_iterations > 0:
        print(cpu)
        max_iterations -= 1
    print(cpu)

if __name__ == '__main__':
    main()