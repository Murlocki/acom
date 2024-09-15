import cv2
def trackRed():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        frameUpdate = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        cv2.imshow('frame', frameUpdate)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

trackRed()