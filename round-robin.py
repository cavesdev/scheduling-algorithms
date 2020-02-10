import matplotlib.pyplot as plt
from models.process import Process


def get_process_times(process_list):
    sum = 0
    for process in process_list:
        sum += process.get_remaining_time()
    return sum


print('Round Robin')
process_number = int(input('Numero de procesos a crear: '))
process_list = []

# get process times
for i in range(process_number):
    time = int(input(f'Tiempo de rafaga del proceso {i + 1}: '))
    new_process = Process(time)
    process_list.append(new_process)

quantum = int(input('Quantum: '))

# initialize graph
# Declaring a figure "gnt"
fig, gnt = plt.subplots()

# Setting Y-axis limits
gnt.set_ylim(0, 50)

# Setting X-axis limits
gnt.set_xlim(0, get_process_times(process_list))

# Setting labels for x-axis and y-axis
gnt.set_xlabel('seconds since start')
gnt.set_ylabel('Processor')

# Setting ticks on y-axis
gnt.set_yticks([15, 25, 35])
# Labelling tickes of y-axis
gnt.set_yticklabels(['1', '2', '3'])

i = 0

for process in process_list:
    if process.get_remaining_time() > quantum:
        process.reduce_time(quantum)
        print(f'P{process.number} - {quantum}')
        process.add_time(i, quantum)
        process_list.append(process)
        i += quantum
    else:
        print(f'P{process.number} - {process.get_remaining_time()}')
        process.add_time(i, process.get_remaining_time())
        i += process.get_remaining_time()

colors = ['red', 'green', 'blue', 'orange', 'black']

for process in set(process_list):
    color = colors[process.number - 1]
    lists = process.get_times()
    gnt.broken_barh(lists, (20, 9), facecolors=f'{color}', label=f'P{process.number}')


gnt.legend()
plt.savefig('gantt_rr.png')
plt.show()