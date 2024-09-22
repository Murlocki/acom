import cv2
import numpy as np
# Задание 1 Выполнить пункты 1 и 2 алгоритма, то есть построить
# матрицу Гаусса. Просмотреть итоговую матрицу для размерностей 3, 5, 7
def gaussMatrix(kernelSize=3, standardDeviation=0.2):
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
    return kernel
def gaussFunc(x, y, omega, a, b):
    omega2 = 2 * omega ** 2
    m1 = 1 / (np.pi * omega2)
    m2 = np.exp(-((x-a) ** 2 + (y-b) ** 2) / omega2)
    return m1 * m2

def gaussBlur(img,kernelSize=3,standardDeviation=0.2):
    kernel = gaussMatrix(kernelSize,standardDeviation)
    imgBlur = img.copy()

    #Заводим стартовые индексы
    xStart = kernelSize // 2
    yStart = kernelSize // 2
    for i in range(xStart, imgBlur.shape[0] - xStart):
        for j in range(yStart, imgBlur.shape[1] - yStart):
            # операция свёртки
            val = 0
            for k in range(-(kernelSize // 2), kernelSize // 2 + 1):
                for l in range(-(kernelSize // 2), kernelSize // 2 + 1):
                    val += img[i + k, j + l] * kernel[k + (kernelSize // 2), l + (kernelSize // 2)]
            imgBlur[i, j] = val
    return imgBlur

#Встроенная реализация фильтра Гаусса
def applyGaussianFilterOpencv(image, size, sigma):
    return cv2.GaussianBlur(image, (size, size), sigmaX=sigma,sigmaY=sigma)

def BlurFuss():
    img = cv2.imread("test2.jpg", cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img,(640,640))
    #  размер ядра фильтра и стандартное отклонение
    kernel_size = 5
    standard_deviation = 100

    imgBlur1 = gaussBlur(img, kernel_size, standard_deviation)
    cv2.imshow(f"{str(kernel_size)}x{str(kernel_size)} and deviation {str(standard_deviation)}", imgBlur1)
    imgBlur1 = applyGaussianFilterOpencv(img, kernel_size, standard_deviation)
    cv2.imshow(f"{str(kernel_size)}x{str(kernel_size)} and deviation {str(standard_deviation)} openCv", imgBlur1)


    kernel_size = 5
    standard_deviation = 50

    imgBlur1 = gaussBlur(img, kernel_size, standard_deviation)
    cv2.imshow(f"{str(kernel_size)}x{str(kernel_size)} and deviation {str(standard_deviation)}", imgBlur1)
    imgBlur1 = applyGaussianFilterOpencv(img, kernel_size, standard_deviation)
    cv2.imshow(f"{str(kernel_size)}x{str(kernel_size)} and deviation {str(standard_deviation)} openCv", imgBlur1)

    # другие параметры
    kernel_size = 11
    standard_deviation = 50

    imgBlur2 = gaussBlur(img, kernel_size, standard_deviation)
    cv2.imshow(f"{str(kernel_size)}x{str(kernel_size)} and deviation {str(standard_deviation)}", imgBlur2)
    imgBlur2 = applyGaussianFilterOpencv(img, kernel_size, standard_deviation)
    cv2.imshow(f"{str(kernel_size)}x{str(kernel_size)} and deviation {str(standard_deviation)} openCv", imgBlur2)


    kernel_size = 11
    standard_deviation = 100

    imgBlur2 = gaussBlur(img, kernel_size, standard_deviation)
    cv2.imshow(f"{str(kernel_size)}x{str(kernel_size)} and deviation {str(standard_deviation)}", imgBlur2)
    imgBlur2 = applyGaussianFilterOpencv(img, kernel_size, standard_deviation)
    cv2.imshow(f"{str(kernel_size)}x{str(kernel_size)} and deviation {str(standard_deviation)} openCv", imgBlur2)


    cv2.imshow("Original image",img)
    cv2.waitKey(0)

BlurFuss()
