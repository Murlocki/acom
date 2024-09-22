import cv2

def preprocessImage(path,kernelSize = 5,sigmaX=10,sigmaY=10,sizeX=640,sizeY=640):
    img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img,(sizeX,sizeY))
    cv2.imshow("GrayScale image",img)

    imgGaussian = cv2.GaussianBlur(img,(kernelSize,kernelSize),sigmaX=sigmaX,sigmaY=sigmaY)
    cv2.imshow("Gaussian image",imgGaussian)

    cv2.waitKey(0)

preprocessImage("test2.jpg")