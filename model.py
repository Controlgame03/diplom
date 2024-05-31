import os
import struct

def random_float(): 
    random_bytes = os.urandom(8)
    random_number = struct.unpack("Q", random_bytes)[0]
    max_value = 2**64 - 1
    return random_number / max_value

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

def generate_intervals(n, stack_distribution):
    result = [0 for i in range(n)]
    stack_distribution = absolute_to_relative_stack(n, stack_distribution)

    stack_distribution.insert(0, 0)
    for element in range(1, n):
        stack_distribution[element] = stack_distribution[element] + stack_distribution[element - 1]
    stack_distribution[len(stack_distribution) - 1] = 1.0
    
    for cur_node in range(n):
        result[cur_node] = (stack_distribution[cur_node], stack_distribution[cur_node + 1])

    return result

N = 10
nodes_count = 3
epoch_count = 365 * 24 * 25 #(100 / 5)
slot_count = 5
initial_resources = 25000
max_resources = 45000
reserv_resources = max_resources - initial_resources
prize_koef = 0.5

stack_distribution = []
winners = []
results = []

for cur_node in range(nodes_count):
        stack_distribution.append(initial_resources / nodes_count)
        winners.append(0)

for cur_test in range(N):
    winner_prize = reserv_resources * prize_koef

    for cur_node in range(nodes_count):
        stack_distribution[cur_node] = initial_resources / nodes_count
        winners[cur_node] = 0

    check_intervals = 1
    is_network_takeover = False

    for cur_epokh in range(0, epoch_count):
        #print('eploch ', cur_epokh)
        winner_prize = reserv_resources * prize_koef
        intervals = generate_intervals(nodes_count, stack_distribution.copy())
        for cur_slot in range(0, slot_count):
            
            random_number = random_float()
            interval_index = find_interval(random_number, intervals)

            winners[interval_index] += 1
        
        for i in range(len(winners)):
            stack_distribution[i] += winner_prize / slot_count * winners[i]

        #reserv_resources -= winner_prize

        if cur_epokh % check_intervals == 0:
            if max(absolute_to_relative_stack(len(stack_distribution), stack_distribution)) > 0.5:
                is_network_takeover = True
            
        if is_network_takeover:
            break
        
        for i in range(len(winners)):
            winners[i] = 0
    result_koef = max(absolute_to_relative_stack(len(stack_distribution), stack_distribution))
    result_koef = result_koef / (1 - result_koef)
    results.append((result_koef, 0))
    print(is_network_takeover)

print(results[j][0] for j in range(len(results)))
for j in range(len(results)):
    print(results[j][0])


# обратотка результатов

print('end')
