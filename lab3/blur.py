import numpy as np
# Задание 1 Выполнить пункты 1 и 2 алгоритма, то есть построить
# матрицу Гаусса. Просмотреть итоговую матрицу для размерностей 3, 5, 7
def gaussMatrix(kernelSize, standardDeviation=0.2):
    kernel = np.ones((kernelSize, kernelSize))
    a = b = (kernelSize + 1) // 2

    # Строим матрицу свёртки
    for i in range(kernelSize):
        for j in range(kernelSize):
            kernel[i, j] = gaussFunc(i, j, standardDeviation, a, b)

    print(kernel)
    print("//////////")

    # Задание 2 Нормировать полученную матрицу Гаусса. Протестировать результаты на матрицах из предыдущего пункта.
    # нормирование матрицы
    # Находим сумму
    elementSum = np.sum(kernel)
    kernel = kernel/elementSum
    print(kernel)
def gaussFunc(x, y, omega, a, b):
    omega2 = 2 * omega ** 2
    m1 = 1 / (np.pi * omega2)
    m2 = np.exp(-((x-a) ** 2 + (y-b) ** 2) / omega2)
    return m1 * m2

gaussMatrix(3,0.4)
gaussMatrix(5,0.4)
gaussMatrix(7,0.4)