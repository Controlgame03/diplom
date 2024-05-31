import os
import struct
import matplotlib.pyplot as plt
import math
import random

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
    result = max(stack_distribution) / (sum(stack_distribution) - max(stack_distribution))
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
    
    #stack_distribution = absolute_to_relative_stack(n, stack_distribution)
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
        stack_distribution[element] = stack_distribution[element] + stack_distribution[element - 1]
    stack_distribution[len(stack_distribution) - 1] = 1.0
    
    for cur_node in range(n):
        result[cur_node] = (stack_distribution[cur_node], stack_distribution[cur_node + 1])

    return result

def poisson_stream(input_lambda): # сколько сообщений появилось в новом окне
    messages_count = 0
    exp = math.exp(-input_lambda)
    random_int = random.random()
    while random_int > exp:
        messages_count += 1
        exp += math.exp(-input_lambda) * (input_lambda**messages_count) / math.factorial(messages_count)
    return messages_count

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
transaction_count = 1000
delay = 20

output_lambda = transaction_count/delay
basic_input_lambda = 60

arguments = []
values = []

for input_lambda in range(1,basic_input_lambda, 1):
    transactions = []
    max_transaction_len = 10000

    finish_transaction = []
    is_broken = False
    for cur_epokh in range(epoch_count):
        for cur_slot in range(slot_count):

            for i in range(transaction_count):
                if len(transactions) != 0:
                    finish_transaction.append(transactions[0])
                    transactions.pop(0)
            

            new_transactions = 0
            for i in range(delay):
                new_transactions += poisson_stream(input_lambda)
            for i in range(new_transactions):
                transactions.append(-10)
            
            for i in range(len(transactions)):
                transactions[i] += delay
        
        if (len(transactions) >= max_transaction_len):
            is_broken = True
            break
    
    if is_broken:
        arguments.append(input_lambda)
        values.append(1000)
        break
    else:
        arguments.append(input_lambda)
        values.append(sum(finish_transaction)/len(finish_transaction))
    print(input_lambda)

plt.plot(arguments, values)
plt.title('Зависимость ин-сти выход. потока от ин-сти вход. потока')
plt.xlabel('Инт-сть вход.потока')
plt.ylabel('Инт-сть выход.потока')
plt.show()
