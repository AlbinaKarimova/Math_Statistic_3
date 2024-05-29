import pandas as pd
import numpy as np
from scipy.stats import norm

data_1 = pd.read_excel('var10_Z2.xls', sheet_name='Sheet2', usecols='I')
data_1 = data_1[data_1['Z8A'].notna()]
data_1_arr = list(data_1['Z8A'])
data_1_arr.sort()

data_2 = pd.read_excel('var10_Z2.xls', sheet_name='Sheet2', usecols='J')
data_2 = data_2[data_2['Z8B'].notna()]
data_2_arr = list(data_2['Z8B'])
data_2_arr.sort()

alpha = 0.05
# Направление ожиданий исследователя: 1-я группа меньше

n_1 = len(data_1)
n_2 = len(data_2)

# Объединяем данные
data = data_1_arr
for elem in data_2_arr:
    data.append(elem)

# Функция для подсчета рангов и статистики
def find_W(d, n):
    k = 0
    count = 0
    v = []
    for i in range(1, n+1):
        if d[i - 1] == d[i]:
            k += i
            count += 1
        else:
            count += 1
            k += i
            if count > 1:
                for j in range(0, count):
                    v.append(k / count)
            else:
                v.append(i)
            k = 0
            count = 0
    return len(v)*(len(v)+1)/2

W = find_W(data, n_1) # Статистика Вилкоксона W<C!!!!
print(f"Сумма рангов 1-й выборки W: {W}")

mu = n_1 * (n_1 + n_2 + 1) / 2 # Матожидание
print(f"Математическое ожидание: {mu}")
std = np.sqrt(n_1 * n_2 * (n_1 + n_2 + 1) / 12)
print(f"Стандартное отклонение: {round(std, 3)}")

C = mu + std * norm.ppf(0.05) # Критическая константа
print(f"{alpha*100}%-я критическая область: W < {round(C, 3)}")


if (W < C): # то есть если попадаем в крит область, то нулевая гипотеза отвергается
    print("Нулевая гипотеза отвергается")
else:
    print("Нулевая гипотеза принимается")

p_value = norm.cdf((W - mu) / std)
if p_value < 0.00001:
    print(f"Критический уровень значимости: p_value < 0.00001")
else:
    print(f"Критический уровень значимости: {p_value}")

if (p_value > alpha):
    print("Отклонение от нулевой гипотезы не значимо, принимается нулевая гипотеза")
else:
    print("Отклонение от нулевой гипотезы значимо, принимается альтернатива")

print(n_1)
print(n_2)
