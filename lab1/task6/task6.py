import cv2
def print_cam(rectWidth,rectHeight,frameSize=(640,480)):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,frameSize[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,frameSize[1])

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    videoWriter = cv2.VideoWriter("output.mp4", fourcc, fps=25, frameSize=(frameSize[0], frameSize[1]))
    while True:
        ret, frame = cap.read()


        # Вычисляем центральные координаты
        center_x = frameSize[0] // 2
        center_y = frameSize[1] // 2

        #Рисуем крест
        cv2.rectangle(frame, (center_x - rectWidth // 2, center_y - rectHeight // 2),
                      (center_x + rectWidth // 2, center_y + rectHeight // 2), (0, 0, 255), 1)

        cv2.rectangle(frame, (center_x - rectHeight // 2, center_y - int(rectWidth*0.7)),
                      (center_x+rectHeight//2, center_y-rectHeight//2), (0, 0, 255), 1)
        cv2.rectangle(frame, (center_x - rectHeight // 2, center_y+rectHeight//2),
                      (center_x + rectHeight // 2, center_y + int(rectWidth*0.7)), (0, 0, 255), 1)


        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame',frame)
        videoWriter.write(frame)
        if cv2.waitKey(1)&0xFF==27:
            break
    cap.release()
    videoWriter.release()
    cv2.destroyAllWindows()
print_cam(160,30)