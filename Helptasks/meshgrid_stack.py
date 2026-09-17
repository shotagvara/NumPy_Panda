"""Задание 1: Создай одномерный массив от 1 до 5. 
С помощью np.where замени все нечетные числа в нем на -1. 
(Подсказка: проверка на нечетность — это arr % 2 != 0)."""

import numpy as np

mylist=list(range(1,6))
print(mylist)
array = np.array(mylist)
print(array)

arr = np.where(array % 2 != 0, -1, array)
print(arr)
