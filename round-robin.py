import matplotlib.pyplot as plt
import tkinter as tk
import random

from tkinter.font import Font
from PIL import ImageTk, Image
from models.process import Process


def add_waiting_times(actual_process, time, process_list):
    for process in process_list:
        if process is actual_process:
            continue
        process.add_waiting_time(time)


def get_waiting_times_text(process_list, n):
    waiting_text = 'PROCESO\t ESPERA\n'
    avg = 0
    for process in set(process_list):
        waiting_text += f'P{process.number}\t {process.get_waiting_time()}\n'
        avg += process.get_waiting_time()
    waiting_text += f'PROMEDIO = {format(avg / n, ".2f")}'
    return waiting_text


def get_random_color():
    red = random.random()
    green = random.random()
    blue = random.random()
    alpha = 1.0
    return red, green, blue, alpha


class RoundRobin:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Round Robin')
        self.process_text = 'PROCESO\t RAFAGA\n'
        self.process_number = 0
        self.process_list = []
        self.quantum = 0
        self.passed_time = 0
        self.total_time = 0
        _, self.gnt = plt.subplots()

    def ask_input(self):
        self.process_number = int(input('Numero de procesos a crear: '))

        # get process times
        for i in range(self.process_number):
            duration = int(input(f'Tiempo de rafaga del proceso {i + 1}: '))
            new_process = Process(duration)
            self.process_list.append(new_process)

        self.quantum = int(input('Quantum: '))
        self.total_time = self.get_process_times()

    def get_process_times(self):
        sum = 0
        for process in self.process_list:
            sum += process.get_remaining_time()
            self.process_text += f'P{process.number}\t {process.duration}\n'
        return sum

    def run(self):
        unfinished_process_list = self.process_list.copy()
        for process in self.process_list:
            if process.get_remaining_time() > self.quantum:
                process.reduce_duration(self.quantum)
                process.add_processing_time(begin=self.passed_time, duration=self.quantum)
                self.process_list.append(process)
                self.passed_time += self.quantum
                add_waiting_times(actual_process=process, time=self.quantum, process_list=unfinished_process_list)
            else:
                process.add_processing_time(begin=self.passed_time, duration=process.get_remaining_time())
                self.passed_time += process.get_remaining_time()
                unfinished_process_list.remove(process)
                add_waiting_times(actual_process=process, time=process.get_remaining_time(),
                                  process_list=unfinished_process_list)

    def graph(self):
        self.gnt.set_ylim(0, 50)
        self.gnt.set_xlim(0, self.total_time)
        self.gnt.set_xlabel('seconds since start')
        self.gnt.set_yticks([15, 25, 35])
        self.gnt.set_yticklabels(['1', '2', '3'])

        for process in set(self.process_list):
            color = get_random_color()
            time_list = process.get_processing_times()
            self.gnt.broken_barh(time_list, (20, 9), color=color, label=f'P{process.number}', edgecolor='black')

        self.gnt.legend()
        plt.savefig('gantt_rr.png')

    def show(self):
        font = Font(family='Helvetica', size=20)

        # add graph at East
        img = ImageTk.PhotoImage(Image.open('gantt_rr.png'))
        img_panel = tk.Label(self.window, image=img)
        img_panel.grid(column=1, row=0)

        # add process times at West
        label = tk.Label(self.window, text=self.process_text, font=font)
        label.grid(column=0, row=0)

        # add waiting times at SE
        text = get_waiting_times_text(self.process_list, self.process_number)
        label = tk.Label(self.window, text=text, font=font)
        label.grid(column=1, row=1)

        self.window.mainloop()


if __name__ == "__main__":
    rr = RoundRobin()
    rr.ask_input()
    rr.run()
    rr.graph()
    rr.show()
