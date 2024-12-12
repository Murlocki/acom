import cv2
import os

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


# Путь к папке с изображениями
input_folder = './vagons/'
# Путь к папке для сохранения результатов
output_folder = './edgeResults/'

# Создание выходной папки, если она не существует
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
print(os.listdir(input_folder))
# Проход по всем файлам в папке с изображениями
for filename in os.listdir(input_folder):
        # Полный путь к изображению
        img_path = os.path.join(input_folder, filename)

        # Чтение изображения
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.GaussianBlur(img, (5, 5), 0)

        kernel = np.ones((5, 5), np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        # Применение алгоритма Канни для обнаружения границ
        #edges = cv2.Canny(img, 60, 100)
        edges = kirsch_operator(img)
        # Сохранение результата в выходную папку
        output_path = os.path.join(output_folder, f'edges_{filename}')
        #cv2.imshow("fff",edges)
        #cv2.waitKey()
        cv2.imwrite(output_path, edges)

print("Обработка завершена!")