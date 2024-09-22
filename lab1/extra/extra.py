import cv2
import math
def print_cam(radius,frameSize=(640,480)):
    #ipwebcam
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    videoWriter = cv2.VideoWriter("output.mp4", fourcc, fps=25, frameSize=(frameSize[0], frameSize[1]))
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, frameSize)

        # Вычисляем центральные координаты
        centerX = frameSize[0] // 2
        centerY = frameSize[1] // 2

        #Цвет центрального пикселя
        centralPixel = frame[centerY, centerX]

        #Определяем цвет
        blue, green, red = centralPixel  # BGR формат
        if red > green and red > blue:
            fillColor = (0, 0, 255)  # Красный
        elif green > red and green > blue:
            fillColor = (0, 255, 0)  # Зеленый
        else:
            fillColor = (255, 0, 0)  # Синий

        #Рисуем крест
        cv2.circle(frame,(centerX,centerY),radius,fillColor,3)

        rads1 = math.radians(18)
        rads2 = math.radians(45)
        points = [
            (centerX,centerY-radius),
            (int(centerX + radius * math.cos(rads1)),int(centerY - radius * math.sin(rads1))),
            (int(centerX+radius*math.cos(rads2)),int(centerY+radius*math.sin(rads2))),
            (int(centerX - radius * math.cos(rads2)), int(centerY + radius * math.sin(rads2))),
            (int(centerX - radius * math.cos(rads1)), int(centerY - radius * math.sin(rads1)))
            ]
        print(points)
        cv2.line(frame,points[0],points[2],fillColor,3)
        cv2.line(frame, points[0], points[3], fillColor, 3)
        cv2.line(frame, points[1], points[4], fillColor, 3)
        cv2.line(frame, points[1], points[3], fillColor, 3)
        cv2.line(frame, points[2], points[4], fillColor, 3)
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame',frame)
        videoWriter.write(frame)
        if cv2.waitKey(1)&0xFF==27:
            break
    cap.release()
    videoWriter.release()
    cv2.destroyAllWindows()
print_cam(160)