import pandas as pd
import numpy as np
from scipy.stats import t

data_before = pd.read_excel('var10_Z2.xls', sheet_name='Sheet2', usecols='B')
data_before = data_before[data_before['Z5A'].notna()]

data_after = pd.read_excel('var10_Z2.xls', sheet_name='Sheet2', usecols='C')
data_after = data_after[data_after['Z5B'].notna()]

alpha = 0.05
# Направление ожиданий исследователя уменьшится, значит ожидается что mu1-mu2>0

# Смещенная дисперсия
def disp(data):
    res = 0
    for i in range(1, len(data)+1):
        res += pow(data[i-1], 2)
    res *= 1/len(data)
    return res - pow(np.mean(data), 2)

def characterictics(data):
    print(f"Объем выборки: {len(data)}")
    print(f"Среднее: {round(np.mean(data), 2)}")
    s = pow(np.var(data, ddof=0), 0.5)
    print(f"Стандартное отклонение: {round(s, 3)}")
    print(f"Стандартная ошибка среднего: {round(s/pow(len(data)-1, 0.5), 3)}")

# Найдем разности выборочных значений
def find_u(d1, d2):
    u = []
    for i in range(len(d1)):
        u_i = d1[i] - d2[i]
        u.append(u_i)
    return u

u = find_u(data_before['Z5A'], data_after['Z5B'])
u_mean = np.mean(u) # Среднее арифметическое разностей
disp_u = np.var(u, ddof=0) # Смещенная дисперсия

s_1 = np.var(data_before['Z5A'], ddof=0)
s_2 = np.var(data_after['Z5B'], ddof=0)

n = len(data_before)
T = u_mean * pow(n, 0.5) / pow(disp_u, 0.5) # Статистика Стьюдента

C = t.ppf(1-alpha, n-1) # T>=C - КРИТИЧЕСКАЯ КОНСТАНТА(верхняя квантиль Стьюдента)

print("ДО")
characterictics(data_before['Z5A'])
print("ПОСЛЕ")
characterictics(data_after['Z5B'])
print("ПО РАЗНОСТЯМ")
characterictics(u)
print(f"Статистика Стьюдента: {round(T, 3)}")
print(f"{alpha*100}%-ая критическая область: T >= {round(C, 3)}")

if (T >= C):
    print("Нулевая гипотеза отвергается")
else:
    print("Нулевая гипотеза принимается")

p_value = 1 - t.cdf(T, n-1)
print(f"Критический уровень значимости: {round(p_value, 2)}")

if (p_value > alpha):
    print("Отклонение от нулевой гипотезы не значимо, принимается нулевая гипотеза")
else:
    print("Отклонение от нулевой гипотезы значимо, принимается альтернатива")






