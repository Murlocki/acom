import cv2

def processVideo(path,frameSize=(1920,1080),color=cv2.COLOR_BGR2GRAY):
    cap = cv2.VideoCapture(path, cv2.CAP_ANY)
    cap = cv2.VideoCapture(r'video.avi', cv2.CAP_ANY)

    if not cap.isOpened():
        print("Error opening video stream or file")
        exit()

    while True:
        ret, frame = cap.read()
        if not(ret):
            break
        #В документации написано делать так: https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html#:~:text=Changing%20Color%2Dspace&text=For%20color%20conversion%2C%20we%20use,determines%20the%20type%20of%20conversion.&text=For%20HSV%2C%20hue%20range%20is,value%20range%20is%20%5B0%2C255%5D.
        updateFrame = cv2.resize(cv2.cvtColor(frame, color), frameSize)
        cv2.imshow('frame', updateFrame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()

processVideo('video.avi')
processVideo('../task4/video.mp4')
processVideo('video.avi', (1280, 720), cv2.COLOR_BGR2XYZ)
processVideo('video.avi', (640, 360), cv2.COLOR_BGR2HSV)