import pandas as pd
import numpy as np
from scipy.stats import binom

data = pd.read_excel('var10_Z2.xls', sheet_name='Sheet2', usecols='D')
data = data[data['Z6I'].notna()]
# A-успех

alpha = 0.05
# Направление ожиданий исследователя:  p < 0.2

n = len(data)

# Количество успешных исходов
def find_T(d):
    T = 0
    for i in range(len(d)):
        if d[i] == 'A':
            T += 1
    return T, T*1/len(d)

chastota = find_T(data['Z6I'])[1]
T = find_T(data['Z6I'])[0]
print(f"Статистика: {T} из {n}")

# Найдем критическую константу (T=<C)!
C = binom.ppf(alpha, n, 0.2)
print(f"{alpha*100}%-ая критическая область: T <= {C}")
if (T <= C):
    print("Нулевая гипотеза отвергается")
else:
    print("Нулевая гипотеза принимается")

p_value = binom.cdf(T, n, 0.2)
print(f"Критический уровень значимости: {p_value}")

if (p_value > alpha):
    print("Отклонение от нулевой гипотезы не значимо, принимается нулевая гипотеза")
else:
    print("Отклонение от нулевой гипотезы значимо, принимается альтернатива")
print(binom.cdf(9, 75, 0.2))

