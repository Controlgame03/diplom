import matplotlib.pyplot as plt
import random

# Генерация данных
data = [random.randint(1, 100) for _ in range(100)]

# Построение гистограммы
plt.hist(data, bins=10, edgecolor='black')

# Добавление заголовков и меток осей
plt.title('Пример простой гистограммы')
plt.xlabel('Значения')
plt.ylabel('Частота')

# Показ графика
plt.show()
