import cv2
def print_cam(rectWidth,rectHeight):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

    while True:
        ret, frame = cap.read()

        # Получаем размеры кадра
        height, width, channels = frame.shape

        # Вычисляем центральные координаты
        center_x = width // 2
        center_y = height // 2

        #Рисуем крест
        cv2.rectangle(frame, (center_x - rectWidth // 2, center_y - rectHeight // 2),
                      (center_x + rectWidth // 2, center_y + rectHeight // 2), (0, 0, 255), 1)

        cv2.rectangle(frame, (center_x - rectHeight // 2, center_y - int(rectWidth*0.7)),
                      (center_x+rectHeight//2, center_y-rectHeight//2), (0, 0, 255), 1)
        cv2.rectangle(frame, (center_x - rectHeight // 2, center_y+rectHeight//2),
                      (center_x + rectHeight // 2, center_y + int(rectWidth*0.7)), (0, 0, 255), 1)


        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1)&0xFF==27:
            break
    cap.release()
    cv2.destroyAllWindows()
print_cam(160,30)