import os
import struct
import matplotlib.pyplot as plt
import math

def random_float(): 
    random_bytes = os.urandom(8)
    random_number = struct.unpack("Q", random_bytes)[0]
    max_value = 2**64 - 1
    return random_number / max_value

def capture_winning_prob(n, stack_distribution, index, algorithm):
    if algorithm == 'log':
        base = 3
        log_base_array = [math.log(x, base) for x in stack_distribution]
        stack_distribution = log_base_array
    elif algorithm == 'lin':
        maximum = sum(stack_distribution) / n
        for element in range(n):
            if stack_distribution[element] > maximum:
                stack_distribution[element] = maximum
    return (stack_distribution[index] / sum(stack_distribution)) 


def find_interval(value, intervals):
    for i, (start, end) in enumerate(intervals):
        if start <= value < end:
            return i
    return None

def absolute_to_relative_stack(n, stack_distribution):
    sum = 0
    result = [0 for i in range(n)]
    for element in range(n):
        sum += stack_distribution[element]
    for element in range(n):
        result[element] = stack_distribution[element] / sum
    return result

def generate_intervals(n, stack_distribution, algorithm):
    if algorithm == 'log':
        base = 3
        log_base_array = [math.log(x, base) for x in stack_distribution]
        stack_distribution = log_base_array
    elif algorithm == 'lin':
        maximum = sum(stack_distribution) / n
        for element in range(n):
            if stack_distribution[element] > maximum:
                stack_distribution[element] = maximum

    result = [0 for i in range(n)]
    stack_distribution = absolute_to_relative_stack(n, stack_distribution)

    stack_distribution.insert(0, 0)
    for element in range(1, n):
        stack_distribution[element] = stack_distribution[element] + stack_distribution[element - 1]
    stack_distribution[len(stack_distribution) - 1] = 1.0
    
    for cur_node in range(n):
        result[cur_node] = (stack_distribution[cur_node], stack_distribution[cur_node + 1])

    return result

nodes_count = 100
epoch_count = 10000
slot_count = 1
initial_resources = 25000
max_resources = 450000
reserv_resources = max_resources - initial_resources
prize_koef = 0.00005
winner_prize = reserv_resources * prize_koef
stack_distribution = []
winners = []
algorithm = 'log'

winning_prob = []
winning_index = 0

for cur_node in range(nodes_count):
    stack_distribution.append(initial_resources / nodes_count)
    winners.append(0)

# stack_distribution[0] =+ 20 * stack_distribution[1]
# stack_distribution[400] *= 0.5
# stack_distribution[401] = 0
# stack_distribution[402] = 0
# stack_distribution[403] = 0
# stack_distribution[404] = 0

check_intervals = epoch_count + 1
is_network_takeover = False

for cur_epokh in range(0, epoch_count):
    # print('начало ', str(cur_epokh + 1), ' эпохи')
    winner_prize = reserv_resources * prize_koef
    #winner_prize = sum(stack_distribution) * prize_koef
    # print(winner_prize)
    intervals = generate_intervals(nodes_count, stack_distribution.copy(), algorithm)
    winning_prob.append(capture_winning_prob(nodes_count, stack_distribution.copy(), winning_index, algorithm))
    for cur_slot in range(0, slot_count):
        # print(str(cur_slot + 1), 'слот')
        random_number = random_float()
        interval_index = find_interval(random_number, intervals)
        # print('выиграл ', str(interval_index), ' узел')
        winners[interval_index] += 1
     
    for i in range(len(winners)):
        stack_distribution[i] += winner_prize / slot_count * winners[i]

    reserv_resources -= winner_prize

    if cur_epokh != 0 and cur_epokh % check_intervals == 0:
        if max(absolute_to_relative_stack(len(stack_distribution), stack_distribution)) > 0.5:
            is_network_takeover = True
        
    if is_network_takeover:
        print('the network was captured for ' + str(cur_slot) + ' slots')
        break
    for i in range(len(winners)):
        winners[i] = 0


if not(is_network_takeover):
    print('система работала корректно ' + str(epoch_count) + ' эпох( 1 эпоха =' + str(slot_count) + ' слотов)')
#print(absolute_to_relative_stack(len(stack_distribution), stack_distribution))
#print('total coins = ' + str(sum(stack_distribution)))

arguments = []
for i in range(1, nodes_count + 1):
    arguments.append(i)
plt.plot(arguments, absolute_to_relative_stack(len(stack_distribution), stack_distribution))

plt.title('Соотношение ресурсов между пользователями')
plt.xlabel('Пользователи')
plt.ylabel('Количество стека')
plt.show()

arguments = []
for i in range(epoch_count):
    arguments.append(i)

plt.plot(arguments, winning_prob)
plt.title('Динамика изменения вероятности выигрыша ' + str(winning_index + 1) + ' пользователя')
plt.xlabel('Эпохи')
plt.ylabel('Вероятность выигрыша')
plt.show()

arguments = []
values = []
for i in range(nodes_count):
    arguments.append(i)
    values.append(capture_winning_prob(nodes_count, stack_distribution.copy(), i, algorithm))

plt.plot(arguments, values)
plt.title('Вероятности выигрыша конкретных узлов')
plt.xlabel('Пользователи')
plt.ylabel('Вероятность выигрыша')
plt.show()

print('end')