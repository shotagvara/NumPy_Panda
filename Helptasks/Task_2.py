"""Задание 2: У тебя есть координаты X = np.array([0, 1]) и Y = np.array([10, 20]).
 Используя np.meshgrid и np.stack, получи массив всех возможных точек (x, y). 
 На выходе должен получиться массив:text[[ 0 10]
 [ 0 20]
 [ 1 10]
 [ 1 20]]"""
import numpy as np

X = np.array([0,1])
Y = np.array([10,20])
X_grid, Y_grid=np.meshgrid(X, Y, indexing="ij")
print(X_grid)
print(Y_grid)

Z = np.stack((X_grid, Y_grid), axis=-1)
print(f"Z:\n{Z}")