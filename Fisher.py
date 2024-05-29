import pandas as pd
import numpy as np
from scipy.stats import f

data_1 = pd.read_excel('var10_Z2.xls', sheet_name='Sheet2', usecols='K')
data_1 = data_1[data_1['Z9A'].notna()]

data_2 = pd.read_excel('var10_Z2.xls', sheet_name='Sheet2', usecols='L')
data_2 = data_2[data_2['Z9B'].notna()]

alpha = 0.05
# Направление ожиданий исследователя: 1-я группа меньше, т.е. вторая точнее (отклонение меньше)
# (то есть ожидается что disp_1 > disp_2)

def characterictics(data):
    print(f"Объем выборки: {len(data)}")
    print(f"Среднее: {round(np.mean(data), 2)}")
    S = np.var(data, ddof=1, axis=0)
    print(f"Несмещенная оценка дисперсии: {round(S, 3)}")

# Несмещенные дисперсии
disp_1 = np.var(data_1['Z9A'], ddof=1, axis=0)
disp_2 = np.var(data_2['Z9B'], ddof=1, axis=0)

# disp_1 > disp_2
F = disp_1 / disp_2 # Статистика Фишера
m = len(data_2) # числитель степеней свободы
n = len(data_1) # знаменатель степеней свободы
C = f.ppf(1-alpha, n-1, m-1) # F>C !Критическая константа-верхняя квантиль распределения Фишера

print("1-й прибор")
characterictics(data_1['Z9A'])
print("2-й прибор")
characterictics(data_2['Z9B'])
print(f"Статистика Фишера: {round(F, 3)}")
print(f"{alpha*100}%-ая критическая область: F > {round(C, 3)}")

if (F > C):
    print("Нулевая гипотеза отвергается")
else:
    print("Нулевая гипотеза принимается")

p_value = 1-f.cdf(F, n-1, m-1)
print(f"Критический уровень значимости: {round(p_value, 4)}")

if (p_value > alpha):
    print("Отклонение от нулевой гипотезы не значимо, принимается нулевая гипотеза")
else:
    print("Отклонение от нулевой гипотезы значимо, принимается альтернатива")