import cv2
import numpy as np
def trackRed():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        hsv_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        cv2.imshow('frame', hsv_frame)

        # Задание 2: Создаем маску по 2 цветам
        # Создаем маску
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([180, 255, 255])
        mask1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
        red_mask = cv2.bitwise_or(mask1, mask2)
        # Отображаем красное на изображении
        cv2.imshow('Thresholded Red', red_mask)

        # Задание 3: Морфологические преобразования (открытие и закрытие)
        kernel = np.ones((5, 5), np.uint8)  # Определяем ядро для морфологических операций
        # При открытии сначала делается erosion - "уменьшаются" размеры пикселей объектов на переднем фоне, затем делает dilation - увеличение
        # При erosion пиксель будет 1 если все пиксели под ядром будут 1
        # При dilation пиксель будет 1 если хотя бы 1 пиксель под ядром будет 1
        # В результате убирается шум на изображении
        opened = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
        # При открытии сначала делается dilation, затем делает erosion
        # Используется для закрытия дырок на объектах
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)  # Закрытие
        # Отображаем результаты морфологических операций
        cv2.imshow('Opened', opened)
        cv2.imshow('Closed', closed)

        res = cv2.bitwise_and(hsv_frame,hsv_frame,mask=red_mask)
        cv2.imshow("Result",cv2.cvtColor(res,cv2.COLOR_HSV2BGR))
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

trackRed()