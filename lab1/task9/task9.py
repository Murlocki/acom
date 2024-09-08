import cv2
def print_cam(rectWidth,rectHeight,frameSize=(640,480)):
    #ipwebcam
    cap = cv2.VideoCapture("http://192.168.0.148:8080/video")
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
        cv2.rectangle(frame, (centerX - rectWidth // 2, centerY - rectHeight // 2),
                      (centerX + rectWidth // 2, centerY + rectHeight // 2), fillColor, -1)

        cv2.rectangle(frame, (centerX - rectHeight // 2, centerY - int(rectWidth*0.7)),
                      (centerX+rectHeight//2, centerY-rectHeight//2), fillColor, -1)
        cv2.rectangle(frame, (centerX - rectHeight // 2, centerY+rectHeight//2),
                      (centerX + rectHeight // 2, centerY + int(rectWidth*0.7)), fillColor, -1)

        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame',frame)
        videoWriter.write(frame)
        if cv2.waitKey(1)&0xFF==27:
            break
    cap.release()
    videoWriter.release()
    cv2.destroyAllWindows()
print_cam(160,30)