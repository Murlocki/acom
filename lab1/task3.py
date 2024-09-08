import cv2
cap = cv2.VideoCapture(r'video.mp4', cv2.CAP_ANY)
while True:
    ret, frame = cap.read()
    if not(ret):
        break
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break