class Process:
    number = 1

    def __init__(self, duration):
        self.duration = duration
        self.number = Process.number
        self.times = []
        self.waiting_time = 0
        Process.number += 1

    def get_remaining_time(self):
        return self.duration

    def reduce_duration(self, time_reduced):
        self.duration -= time_reduced

    def add_processing_time(self, begin, duration):
        self.times.append((begin, duration))

    def get_processing_times(self):
        return self.times

    def add_waiting_time(self, time_added):
        self.waiting_time += time_added

    def get_waiting_time(self):
        return self.waiting_time