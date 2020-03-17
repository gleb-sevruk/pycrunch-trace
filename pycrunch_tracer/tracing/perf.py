class TracerPerf:
    def __init__(self):
        self.total_samples = 1
        self.total_time = 0.00
        pass

    def did_execute_line(self, ts_diff: float):
        self.total_samples += 1
        self.total_time += ts_diff

    def print_avg_time(self):
        each = 1
        should_print = self.total_samples % each == 0
        should_print = True
        if should_print:
            time_per_sample = self.total_time / self.total_samples
            print(f'total_samples - {self.total_samples}')
            print(f'total overhead time - {self.total_time}')
            print(f'{time_per_sample:.5f} ms avg call time overhead')