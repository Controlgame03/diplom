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


def new_koef_k1(n, stack_distribution, algorithm):
    result = 0
    if algorithm == 'log':
        base = 3
        log_base_array = [math.log(x, base) for x in stack_distribution]
        stack_distribution = log_base_array
    elif algorithm == 'lin':
        maximum = sum(stack_distribution) / n
        for element in range(n):
            if stack_distribution[element] > maximum:
                stack_distribution[element] = maximum

    stack_distribution = absolute_to_relative_stack(n, stack_distribution)
    result = max(stack_distribution) / \
        (sum(stack_distribution) - max(stack_distribution))
    return result


def new_koef_k2(n, stack_distribution, algorithm):
    result = 0
    if algorithm == 'log':
        base = 3
        log_base_array = [math.log(x, base) for x in stack_distribution]
        stack_distribution = log_base_array
    elif algorithm == 'lin':
        maximum = sum(stack_distribution) / n
        for element in range(n):
            if stack_distribution[element] > maximum:
                stack_distribution[element] = maximum

    stack_distribution.sort(reverse=True)
    cur_koef = 0
    for i in range(1, len(stack_distribution)):
        cur_koef = sum(stack_distribution[:i])
        tmp = (cur_koef / i) / ((sum(stack_distribution) - cur_koef) / (n - i))
        cur_koef = tmp
        if cur_koef > result:
            result = cur_koef
    return result


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
        stack_distribution[element] = stack_distribution[element] + \
            stack_distribution[element - 1]
    stack_distribution[len(stack_distribution) - 1] = 1.0

    for cur_node in range(n):
        result[cur_node] = (stack_distribution[cur_node],
                            stack_distribution[cur_node + 1])

    return result


nodes_count = 100
epoch_count = 10000
slot_count = 1
initial_resources = 10000
max_resources = 100000
reserv_resources = max_resources - initial_resources
prize_koef = 0.00001
winner_prize = reserv_resources * prize_koef
stack_distribution = []
winners = []
algorithm = 'lin'

k1 = []
k2 = []

winning_prob = []
winning_index = 0

loser_prob = []
loser_index = 1

stack_distribution.append(10 * (initial_resources / nodes_count))
winners.append(0)
initial_resources -= 10 * (initial_resources / nodes_count)
for cur_node in range(nodes_count - 1):
    stack_distribution.append(initial_resources / nodes_count)
    winners.append(0)


check_intervals = epoch_count + 1
is_network_takeover = False

for cur_epokh in range(0, epoch_count):
    winner_prize = reserv_resources * prize_koef
    intervals = generate_intervals(
        nodes_count, stack_distribution.copy(), algorithm)
    winning_prob.append(
        capture_winning_prob(
            nodes_count,
            stack_distribution.copy(),
            winning_index,
            algorithm))
    loser_prob.append(
        capture_winning_prob(
            nodes_count,
            stack_distribution.copy(),
            loser_index,
            algorithm))

    k1.append(new_koef_k1(nodes_count, stack_distribution.copy(), algorithm))
    k2.append(new_koef_k2(nodes_count, stack_distribution.copy(), algorithm))
    for cur_slot in range(0, slot_count):
        random_number = random_float()
        interval_index = find_interval(random_number, intervals)
        winners[interval_index] += 1

    for i in range(len(winners)):
        stack_distribution[i] += winner_prize / slot_count * winners[i]

    reserv_resources -= winner_prize

    if cur_epokh != 0 and cur_epokh % check_intervals == 0:
        if max(absolute_to_relative_stack(
                len(stack_distribution), stack_distribution)) > 0.5:
            is_network_takeover = True

    if is_network_takeover:
        print('the network was captured for ' + str(cur_slot) + ' slots')
        break
    for i in range(len(winners)):
        winners[i] = 0


if not (is_network_takeover):
    print('система работала корректно ' + str(epoch_count) +
          ' эпох( 1 эпоха =' + str(slot_count) + ' слотов)')

arguments = []
for i in range(1, nodes_count + 1):
    arguments.append(i)
plt.plot(arguments, absolute_to_relative_stack(
    len(stack_distribution), stack_distribution))

plt.title('Зависимость количества стека от номера узла')
plt.xlabel('Номер узла')
plt.ylabel('Количество стека (доля от 1.00)')
plt.show()

arguments = []
for i in range(epoch_count):
    arguments.append(i)

plt.plot(arguments, winning_prob)
plt.title('Динамика изменения вероятности выигрыша конкретного(' +
          str(winning_index + 1) + '-ого) пользователя')
plt.xlabel('Номер эпохи')
plt.ylabel('Вероятность выигрыша')
plt.show()


arguments = []
for i in range(epoch_count):
    arguments.append(i)

plt.plot(arguments, loser_prob)
plt.title('Динамика изменения вероятности выигрыша конкретного(' +
          str(loser_index + 1) + '-ого) пользователя')
plt.xlabel('Номер эпохи')
plt.ylabel('Вероятность выигрыша')
plt.show()

arguments = []
values = []
for i in range(nodes_count):
    arguments.append(i)
    values.append(
        capture_winning_prob(
            nodes_count,
            stack_distribution.copy(),
            i,
            algorithm))

plt.plot(arguments, values)
plt.title(
    'Зависимость вероятности выигрыша от номера узла после ' +
    str(epoch_count) +
    ' эпох')
plt.xlabel('Номер узла')
plt.ylabel('Вероятность выигрыша')
plt.show()

arguments = []
for i in range(epoch_count):
    arguments.append(i)

plt.plot(arguments, k1)
plt.title('Динамика изменения коэффициента k1')
plt.xlabel('Номер эпохи')
plt.ylabel('Значаение')
plt.show()

arguments = []
for i in range(epoch_count):
    arguments.append(i)

plt.plot(arguments, k2)
plt.title('Динамика изменения коэффициента k2')
plt.xlabel('Номер эпохи')
plt.ylabel('Значаение')
plt.show()


print('end')
