import cv2
import os

# Путь к папке с изображениями
input_folder = 'C:/Users/kirill/AppData/Roaming/JetBrains/DataSpell2024.3/projects/workspace/vagons/vagons'
# Путь к папке для сохранения результатов
output_folder = 'C:/Users/kirill/AppData/Roaming/JetBrains/DataSpell2024.3/projects/workspace/vagons/vagons/edgeResults'

# Создание выходной папки, если она не существует
if not os.path.exists(output_folder):
        os.makedirs(output_folder)
print(os.listdir(input_folder))
# Проход по всем файлам в папке с изображениями
for filename in os.listdir(input_folder):
        # Полный путь к изображению
        img_path = os.path.join(input_folder, filename)

        # Чтение изображения
        img = cv2.imread("28032449.jpg")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.GaussianBlur(img, (5, 5), 0)
        # Применение алгоритма Канни для обнаружения границ
        edges = cv2.Canny(img, 100, 200)
        print(edges)
        # Сохранение результата в выходную папку
        output_path = os.path.join(output_folder, f'edges_{filename}')
        cv2.imshow("fff",edges)
        cv2.waitKey()
        cv2.imwrite(output_path, edges)

print("Обработка завершена!")