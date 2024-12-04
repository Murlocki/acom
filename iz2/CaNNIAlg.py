import cv2
import numpy as np
import math

from iz2.Operator import Operator
from iz2.PriutOperator import PriutOperator
from iz2.SharOperator import SharOperator
from iz2.SobelOperator import SobelOperator


class CanniAlg:
    def __init__(self,operator):
        self.__operator = operator

    def __printImageInfo(self,image):
        height, width, channels = image.shape
        print(f"Размер изображения: {width}x{height} пикселей")

        # Вывод информации о каналах
        print(f"Количество каналов: {channels}")

        # Получение типа данных изображения
        dtype = image.dtype
        print(f"Тип данных изображения: {dtype}")

        # Получение цветового пространства (предполагается BGR)
        if channels == 3:
            color_space = "BGR"
        elif channels == 1:
            color_space = "Grayscale"
        else:
            color_space = "Unknown"

        print(f"Цветовое пространство: {color_space}")


    def preprocessImage(self,path,kernelSize = 5,sigmaX=10,sigmaY=10,sizeX=640,sizeY=640,lowerBound=100,upperBound=160):
        img = cv2.imread(path)
        self.__printImageInfo(img)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #img = cv2.resize(img,(sizeX,sizeY))
        cv2.imshow("GrayScale image",img)

        imgGaussian = cv2.GaussianBlur(img,(kernelSize,kernelSize),sigmaX=sigmaX,sigmaY=sigmaY)
        cv2.imshow("Gaussian image",imgGaussian)

        grads = self.calcGradients(imgGaussian)
        lengths = self.caclGradLengths(imgGaussian,grads)

        corners = self.calcCorners(imgGaussian,grads)

        suppressed_img = self.supressNotMax(lengths, corners)
        # Вывод изображений на экран
        cv2.imshow('Suppressed Image', suppressed_img)
        #
        edgeImg = self.checkThreshAndEdge(imgGaussian,suppressed_img,lengths,lowerBound,upperBound)
        cv2.imshow('Edge Image', edgeImg)


        # Draw all contours on the original image
        edges = cv2.Canny(imgGaussian, 50, 150)
        # Find contours from the edged image
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(imgGaussian, contours, -1, (0, 255, 0), 3)  # Green color for contours
        cv2.imshow('Edge built',imgGaussian)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def calcGradients(self,img):

        gradientMatrix = []
        for x in range(1,img.shape[0]-1):
            matrixRow = []
            for y in range(1,img.shape[1] - 1):
                Gx,Gy = self.__operator.process(img,x,y)
                matrixRow.append((Gx,Gy))
            gradientMatrix.append(matrixRow)
        return gradientMatrix
    def caclGradLengths(self,img,grads):
        res = np.zeros((img.shape[0],img.shape[1]))
        k = 0
        for i in range(1,img.shape[0]-1):
            l = 0
            for j in range(1,img.shape[1]-1):
                res[i][j] = math.sqrt(grads[k][l][0]**2+grads[k][l][1]**2)
                l=l+1
            k=k+1
        return res

    def calcCorner(self,grad):
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

    def calcCorners(self,img,grads):
        corners = np.zeros((img.shape[0],img.shape[1]))
        k=1
        for i in range(len(grads)):
            l = 1
            for j in range(len(grads[0])):
                corners[k][l] = self.calcCorner(grads[i][j])
                l = l + 1
            k = k + 1
        return corners

    def supressNotMax(self,gradsLenths,corners):
        height, width = gradsLenths.shape
        print(height,width)
        suppressed = np.zeros_like(gradsLenths)

        for y in range(1, width - 1):
            for x in range(1, height - 1):
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

                if gradsLenths[x][y] > q and gradsLenths[x][y] > r:
                    suppressed[x][y] = 255
                else:
                    suppressed[x][y] = 0

        return suppressed
    def checkThreshAndEdge(self,img,filteredImg,gradientsLength,lower_bound,upper_bound):
        img_border_filter = np.zeros(img.shape)
        #maxGrad = np.max(gradientsLength)
        #lower_bound = maxGrad/25;
        #upper_bound = maxGrad/10;
        print(f'Пороги {lower_bound} {upper_bound}')

        for i in range(0,img.shape[0]):
            for j in range(0,img.shape[1]):
                gradient = gradientsLength[i][j]
                # является лок максимумом
                if (filteredImg[i][j] == 255):
                    if (gradient >= lower_bound and gradient <= upper_bound):
                        flag = False
                        # проверим соседние пиксели текусщего пикселя
                        for k in range(-1, 2):
                            for l in range(-1, 2):
                                if (flag):
                                    break
                                if (filteredImg[i + k][j + l] == 255 and filteredImg[i + k][j + l] >= lower_bound):
                                    flag = True
                                    break
                        if (flag):
                            filteredImg[i][j] = 255
                    elif (gradient > upper_bound):
                        img_border_filter[i][j] = 255
        return img_border_filter

#CanniAlg(SobelOperator()).preprocessImage("test4.jpeg")
#CanniAlg(PriutOperator()).preprocessImage("test4.jpeg")
CanniAlg(SobelOperator()).preprocessImage("testImage3.jpg",kernelSize=5,sigmaX=12,sigmaY=12,lowerBound=80,upperBound=110)