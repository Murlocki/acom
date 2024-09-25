import math

import cv2
import numpy as np


def preprocessImage(path,kernelSize = 5,sigmaX=10,sigmaY=10,sizeX=640,sizeY=640):
    img = cv2.imread(path)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img,(sizeX,sizeY))
    print(img)
    cv2.imshow("GrayScale image",img)

    imgGaussian = cv2.GaussianBlur(img,(kernelSize,kernelSize),sigmaX=sigmaX,sigmaY=sigmaY)
    cv2.imshow("Gaussian image",imgGaussian)

    grads = calcGradients(imgGaussian)
    print(grads)
    lengths = caclGradLengths(grads)
    print(lengths)
    corners = calcCorners(grads)
    print(corners)

    suppressed_img = supressNotMax(lengths, corners)

    # Вывод изображений на экран
    cv2.imshow('Suppressed Image', suppressed_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(0)

def calcGradients(img):
    # sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)  # Границы по оси X
    # sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)  # Границы по оси Y
    # print(sobel_x)
    # print(sobel_y)
    gradientMatrix = []
    for x in range(1,img.shape[0]-1):
        matrixRow = []
        for y in range(1,img.shape[1] - 1):
            Gx = -int(img[x - 1][y - 1]) - 2*int(img[x][y-1]) - int(img[x + 1][y - 1]) + \
                 int(img[x - 1][y + 1]) + 2*int(img[x][y + 1]) + int(img[x + 1][y + 1])
            Gy = -int(img[x - 1][y - 1]) - 2*int(img[x - 1][y]) - int(img[x - 1][y + 1]) + \
                 int(img[x + 1][y - 1]) + 2*int(img[x + 1][y]) + int(img[x + 1][y + 1])
            matrixRow.append((Gx,Gy))
        gradientMatrix.append(matrixRow)
    return gradientMatrix
def caclGradLengths(grads):
    return np.sqrt(np.sum(np.pow(grads,2),axis=2))

def calcCorner(grad):
    tang = grad[1]/grad[0] if grad[0] != 0 else 999
    if grad[0] > 0 and grad[1]<0 and tang < -2.414 or grad[0]< 0 and grad[1]<0 and tang > 2.414:
        return 0
    elif grad[0] > 0 and grad[1]<0 and tang < -0.414:
        return 1
    elif grad[0] > 0 and grad[1]<0 and tang > -0.414 or grad[0] > 0 and grad[1] > 0 and tang < 0.414:
        return 2
    elif grad[0] > 0 and grad[1] > 0 and tang < 2.414:
        return 3
    elif grad[0] > 0 and grad[1] > 0 and tang > 2.414 or grad[0] < 0 and grad[1] > 0 and tang< -2.414:
        return 4
    elif grad[0] < 0 and grad[1] > 0 and tang< -0.414:
        return 5
    elif grad[0] < 0 and grad[1] > 0 and tang > -0.414 or grad[0]< 0 and grad[1]<0 and tang < 0.414:
        return 6
    elif grad[0] < 0 and grad[1] < 0 and tang < 2.414:
        return 7
    if (grad[0] == 0):
        if (grad[1] > 0):
            return 4
        elif (grad[1] <= 0):
            return 0
    else:
        if (grad[1] > 0):
            return 2
        elif (grad[1] <= 0):
            return 6

def calcCorners(grads):
    corners = []
    for row in grads:
        corRow = []
        for col in row:
            corRow.append(calcCorner(col))
        corners.append(corRow)
    return corners

def supressNotMax(gradsLenths,corners):
    height, width = gradsLenths.shape
    suppressed = np.zeros_like(gradsLenths)

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            angle = corners[x][y]

            if angle==0 or angle==4:
                q = gradsLenths[x+1][y]
                r = gradsLenths[x-1][y]
            elif angle==1 or angle==5:
                q = gradsLenths[x-1][y+1]
                r = gradsLenths[x + 1][y - 1]
            elif angle==2 or angle==6:
                q = gradsLenths[x][y+1]
                r = gradsLenths[x][y-1]
            elif angle==3 or angle==7:
                q = gradsLenths[x+1][y+1]
                r = gradsLenths[x-1][y-1]

            if gradsLenths[x,][y] >= q and gradsLenths[x][y] >= r:
                suppressed[x][y] = gradsLenths[x][y]

    return suppressed

preprocessImage("test4.jpeg")