import os
import struct
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
        maximum = 3 * sum(stack_distribution) / n
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
        maximum = 3 * sum(stack_distribution) / n
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


N = 100
M = []
V = []
komis = 0.09

for j in range(N):
    nodes_count = 100
    epoch_count = 1000
    slot_count = 1
    initial_resources = 10000
    max_resources = 100000
    reserv_resources = max_resources - initial_resources
    prize_koef = 0.00001
    winner_prize = reserv_resources * prize_koef

    winners = []
    algorithm = 'simple'

    k1 = []
    k2 = []

    winning_prob = []
    index = nodes_count - 1

    loser_prob = []
    loser_index = 1

    stack_distribution = []

    for cur_node in range(nodes_count - 1):
        stack_distribution.append(initial_resources / nodes_count)
        winners.append(0)

    index_stack = initial_resources / nodes_count
    index_stack = 10 * index_stack
    my_nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    stack_index = []
    for i in range(nodes_count - 1):
        if i in my_nodes:
            stack_index.append(index_stack / len(my_nodes))
            stack_distribution[i] += stack_index[i]
        else:
            stack_index.append(0)

    check_intervals = epoch_count + 1
    is_network_takeover = False

    for cur_epokh in range(0, epoch_count):
        winner_prize = reserv_resources * prize_koef
        intervals = generate_intervals(
            nodes_count - 1, stack_distribution.copy(), algorithm)

        for cur_slot in range(0, slot_count):
            random_number = random_float()
            interval_index = find_interval(random_number, intervals)
            winners[interval_index] += 1

        for i in range(len(winners)):
            stack_index[i] += (1 - komis) * (winner_prize / slot_count *
                                             winners[i]) * ((stack_index[i]) / (stack_distribution[i]))
            stack_distribution[i] += komis * (winner_prize / slot_count * winners[i]) * (
                (stack_index[i]) / (stack_distribution[i]))
            stack_distribution[i] += (winner_prize / slot_count * winners[i]) * (
                (stack_distribution[i] - stack_index[i]) / (stack_distribution[i]))

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

    result = 0
    for i in range(nodes_count - 1):
        result += stack_index[i]
        stack_distribution[i] -= stack_index[i]
    stack_distribution.append(result)
    V.append(stack_distribution[index])
    stack_distribution = absolute_to_relative_stack(
        len(stack_distribution), stack_distribution)
    M.append(stack_distribution[index])
print(V)
