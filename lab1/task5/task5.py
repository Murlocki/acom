import cv2

def processToHsv(path):
    img = cv2.imread(path)
    updateImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    print(updateImg)
    print(img)
    cv2.imshow('frame update', updateImg)
    cv2.imshow('frame original', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    img.release()

processToHsv('red.png')