import cv2
import numpy as np


def kirsch_operator(image):
    # Определение масок Кирша для 8 направлений
    kernels = [
        np.array([[5, 5, 5], [-3, 0, -3], [-3, -3, -3]]),  # North
        np.array([[5, 5, -3], [5, 0, -3], [-3, -3, -3]]),  # North-East
        np.array([[5, -3, -3], [5, 0, -3], [5, -3, -3]]),  # East
        np.array([[-3, -3, -3], [5, 0, -3], [5, 5, -3]]),  # South-East
        np.array([[-3, -3, -3], [-3, 0, 5], [-3, 5, 5]]),  # South
        np.array([[-3, -3, -3], [-3, 0, 5], [-3, -3, 5]]),  # South-West
        np.array([[-3, -3, 5], [-3, 0, 5], [-3, -3, 5]]),  # West
        np.array([[5, -3, -3], [-3, 0, -3], [-3, -3, -3]])  # North-West
    ]

    # Применение масок и нахождение максимума
    max_response = np.zeros(image.shape)

    for kernel in kernels:
        response = cv2.filter2D(image, cv2.CV_64F, kernel)
        max_response = np.maximum(max_response, response)

    return max_response


# Загрузка изображения и преобразование в оттенки серого
image = cv2.imread('testImage5.jpg')
minValue = 150

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray_image = cv2.GaussianBlur(gray_image, (5, 5), sigmaX=12, sigmaY=12)
# Применение алгоритма Кирша
edges_kirsch = kirsch_operator(gray_image)

# Нормализация результата для отображения
edges_kirsch = cv2.normalize(edges_kirsch, None, alpha=0, beta=255,
                             norm_type=cv2.NORM_MINMAX)
edges_kirsch = np.uint8(edges_kirsch)
_, edges_kirsch = cv2.threshold(edges_kirsch,minValue,255,cv2.THRESH_BINARY)
# Отображение результатов
cv2.imshow('Original Image', image)
cv2.imshow('Edges using Kirsch Operator', edges_kirsch)
cv2.imwrite('result.jpg',edges_kirsch)
cv2.waitKey(0)
cv2.destroyAllWindows()