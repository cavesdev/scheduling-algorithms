class Process:
    number = 1

    def __init__(self, duration):
        self.duration = duration
        self.number = Process.number
        self.times = []
        Process.number += 1

    def get_remaining_time(self):
        return self.duration

    def reduce_time(self, time_reduced):
        self.duration -= time_reduced
        return self.duration

    def add_time(self, time, duration):
        self.times.append((time, duration))

    def get_times(self):
        return self.times