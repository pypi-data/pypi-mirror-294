import time


class Timer:
    start: float

    def __init__(self):
        self.start = time.perf_counter() * 1000

    def stop(self):
        end = time.perf_counter() * 1000
        dur = end - self.start
        return dur

    def seq_stop(self):
        self.start = time.perf_counter() * 1000
        return self.stop()
