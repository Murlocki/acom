import numpy as np
# Задание 1 Выполнить пункты 1 и 2 алгоритма, то есть построить
# матрицу Гаусса. Просмотреть итоговую матрицу для размерностей 3, 5, 7
def gaussMatrix(kernel_size, standard_deviation=0.2):
    kernel = np.ones((kernel_size, kernel_size))
    a = b = (kernel_size + 1) // 2

    # Строим матрицу свёртки
    for i in range(kernel_size):
        for j in range(kernel_size):
            kernel[i, j] = gaussFunc(i, j, standard_deviation, a, b)

    print(kernel)
    print("//////////")
def gaussFunc(x, y, omega, a, b):
    omega2 = 2 * omega ** 2
    m1 = 1 / (np.pi * omega2)
    m2 = np.exp(-((x-a) ** 2 + (y-b) ** 2) / omega2)
    return m1 * m2

gaussMatrix(3,0.4)