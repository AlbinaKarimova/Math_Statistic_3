import pandas as pd
import numpy as np
from scipy.stats import chi2

data_1 = pd.read_excel('var10_Z2.xls', sheet_name='Sheet2', usecols='M')
data_1 = data_1[data_1['Z10A'].notna()]
data_1_arr = list(data_1['Z10A'])
data_1_arr.sort()

data_2 = pd.read_excel('var10_Z2.xls', sheet_name='Sheet2', usecols='N')
data_2 = data_2[data_2['Z10B'].notna()]
data_2_arr = list(data_2['Z10B'])
data_2_arr.sort()

alpha = 0.05
X_o = 14.4
delta = 2
r = 8
bins = np.linspace(X_o, X_o + delta * r, r + 1) # Разбиение чиловой прямой на r групп
print(bins)
# Количество попаданий в интервал
def count_v(data, left, right):
    v = 0
    for i in range(len(data)):
        if data[i] >= left and data[i] < right: # Берем интервалы типа [ ; )
            v += 1
    return v

# Массив из количества попаданий
def find_v(data, bins_):
    v = []
    v.append(count_v(data, -1, bins_[0]))
    for i in range(0, r-2):
        v.append(count_v(data, bins_[i], bins_[i+1]))
    v.append(len(data)-sum(v))
    return v

v_1 = find_v(data_1_arr, bins)
v_1 = list(v_1)

print(f"Группа А: {v_1}")
v_2 = find_v(data_2_arr, bins)
print(f"Группа B: {v_2}")

n_1 = len(data_1_arr)
n_2 = len(data_2_arr)

# Общее число данных попавших в интервалы
v = []
for i in range(len(v_1)):
    v.append(v_1[i]+v_2[i])

# Ищем статистику Хи^2
def find_T():
    res = 0
    T = []
    for i in range(r):
        res += ((v_1[i] / n_1 - v_2[i] / n_2) ** 2) / v[i]
        T.append(round(n_1 * n_2 * ((v_1[i] / n_1 - v_2[i] / n_2) ** 2) / v[i], 3))
    return res * n_1 * n_2, T

T = find_T()[0] # Статистика хи-квадрат
print(f"Статистика: {round(T, 3)}")

T_i = find_T()[1] # Статистика для групп
print(f"Статистики: {T_i}")

def frequency(v_i):
    fr = []
    n = sum(v_i)
    for i in range(len(v_i)):
        res = v_i[i] / n
        fr.append(round(res, 4))
    return fr

fr_1 = frequency(v_1) # Частоты первой группы
print(f"Частоты группы А: {fr_1}")
fr_2 = frequency(v_2) # Частоты второй группы
print(f"Частоты группы B: {fr_2}")

C = chi2.ppf(1-alpha, r-1) # Критическая константа-верхняя альфа квантиль
print(f"{alpha*100}%-я критическая область: X^2 > {round(C, 3)}")

if (T > C): # то есть если попадаем в крит область, то нулевая гипотеза отвергается
    print("Нулевая гипотеза отвергается")
else:
    print("Нулевая гипотеза принимается")

p_value = 1 - chi2.cdf(T, r-1)
print(f"Критический уровень значимости: {round(p_value, 3)}")

if (p_value > alpha):
    print("Отклонение от нулевой гипотезы не значимо, принимается нулевая гипотеза")
else:
    print("Отклонение от нулевой гипотезы значимо, принимается альтернатива")

