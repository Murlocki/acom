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

        # Задание 4: Нахождение моментов и площади объекта
        moments = cv2.moments(closed)
        print(moments)
        if moments['m00'] != 0:
            area = moments['m00']  # Площадь объекта
            print(f"Area of the object: {area}")
            print(f"Zero-moment:{moments['m00']}")
            print(f"First-order moments:{moments['m01']},{moments['m10']}")
            # Находим центр объекта
            cx = int(moments['m10'] / moments['m00'])
            cy = int(moments['m01'] / moments['m00'])

            # Рисуем черный прямоугольник вокруг объекта
            (cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for countour in cnts:
                (x, y, w, h) = cv2.boundingRect(countour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 2)

            #Общий прямоугольник на все
            white_pixels = np.argwhere(closed == 255)
            min_y, min_x = np.min(white_pixels, axis=0)
            max_y, max_x = np.max(white_pixels, axis=0)
            cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 255, 0), 2)

            #Общий прицел на все
            white_pixels = np.argwhere(closed == 255)
            minY, minX = np.min(white_pixels, axis=0)
            maxY, maxX = np.max(white_pixels, axis=0)
            centerX = (maxX+minX)//2
            centerY = (maxY+minY)//2
            radius = max(maxX - centerX,maxY - centerY)
            cv2.circle(frame,(centerX,centerY),radius,(0,0,0),2)
            cv2.line(frame,(centerX-radius,centerY),(centerX+radius,centerY),(0,0,0),2)
            cv2.line(frame, (centerX, centerY-radius), (centerX, centerY+radius), (0, 0, 0), 2)
            #Накладываем затемнение вне прицела
            # Рисуем белый круг на маске
            mask = np.zeros((frame.shape[0],frame.shape[1]), dtype=np.uint8)
            cv2.circle(mask, (centerX, centerY), radius, 255, -1)
            # Применяем маску к изображению
            # Все пиксели вне круга будут черными, а внутри круга — исходными
            frame = cv2.bitwise_and(frame, frame, mask=mask)
        else:
            area = 0
            print("No object detected.")

        # Display the resulting frame
        cv2.imshow('Result', frame)


        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

trackRed()