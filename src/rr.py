from fcfs import FCFS

class RR(FCFS):

    def min_peek_time(self) -> int:
        min_time: int = super().min_peek_time()
        for p in self.array:
            min_time = min(min_time, self.quantum - p.cpu_time)
        return min_time

    def limit_cpu(self) -> bool:
        return not self.is_empty() and self.array[0].cpu_time >= self.quantum
