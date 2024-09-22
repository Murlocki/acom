import math

import cv2
import numpy as np


def preprocessImage(path,kernelSize = 5,sigmaX=10,sigmaY=10,sizeX=32,sizeY=32):
    img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img,(sizeX,sizeY))
    cv2.imshow("GrayScale image",img)

    imgGaussian = cv2.GaussianBlur(img,(kernelSize,kernelSize),sigmaX=sigmaX,sigmaY=sigmaY)
    cv2.imshow("Gaussian image",imgGaussian)

    grads = calcGradients(imgGaussian)
    print(grads)
    lengths = caclGradLengths(grads)
    print(lengths)
    corners = calcCorners(grads)
    print(corners)

    cv2.waitKey(0)

def calcGradients(img):
    gradientMatrix = []
    for i in range(1,img.shape[0]-1):
        matrixRow = []
        for j in range(1,img.shape[1] - 1):
            resX = -img[i-1,j-1] + img[i-1,j+1] -2 * img[i,j-1] + 2 * img[i,j+1] - img[i+1,j-1] + img[i+1,j+1]
            resY = -img[i - 1, j - 1] -2 * img[i - 1, j] - img[i - 1, j + 1] + img[i + 1, j - 1] + 2 * img[i + 1, j] + \
                   img[i + 1, j + 1]
            matrixRow.append((resX,resY))
        gradientMatrix.append(matrixRow)
    return gradientMatrix
def caclGradLengths(grads):
    return np.sqrt(np.sum(np.pow(grads,2),axis=2))

def calcCorner(grad):
    tang = grad[1]/grad[0]
    if grad[0]< 0 and grad[1]<0 and tang< -2.414 or grad[0]< 0 and grad[1]<0 and tang > 2.414:
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
def calcCorners(grads):
    corners = []
    for row in grads:
        corRow = []
        for col in row:
            corRow.append(calcCorner(col))
        corners.append(corRow)
    return corners
preprocessImage("test2.jpg")