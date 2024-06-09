import matplotlib.pyplot as plt
import math

N = 100
arguments = []
for i in range(N):
    arguments.append(i)


lin = []
log = []
lin_hard = []


for i in range(1, len(arguments) + 1):
    lin.append(i)
    log.append(math.log(i, 3))
    if i > 5:
        lin_hard.append(5)
    else:
        lin_hard.append(i)

for i in range(len(arguments)):
    lin[i] = lin[i] / 100
    log[i] = log[i] / 100
    lin_hard[i] = lin_hard[i] / 100
    arguments[i] = arguments[i] / 100

plt.plot(arguments, lin, label='Линейная зависимость', color='blue')
plt.xlabel('Количество стейка')
plt.ylabel('Вероятность выигрыша')
plt.legend()
plt.show()

plt.plot(arguments, log, label='Логарифмическая зависимость', color='green')
plt.xlabel('Количество стейка')
plt.ylabel('Вероятность выигрыша')
plt.legend()
plt.show()

plt.plot(arguments, lin_hard, label='Линейная зависимость с порогом', color='red')
plt.xlabel('Количество стейка')
plt.ylabel('Вероятность выигрыша')
plt.legend()
plt.show()

