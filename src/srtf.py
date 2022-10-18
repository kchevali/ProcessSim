from sjf import SJF

class SRTF(SJF):
    def check_cpu(self) -> bool:
        return True
