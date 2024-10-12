import csv
import math
import pathlib
import cv2
import numpy as np


def relativaPath(relativePath):
    path = pathlib.Path(__file__).parent / relativePath
    return path
class AugmentationDataset:
    def createAugmentation(self,datasetName,newDatasetName):
        imgFiles = list(pathlib.Path(str(relativaPath(datasetName))).glob("*.jpg"))
        labels = {}
        csv_str = ""
        with open(str(relativaPath(datasetName + "/labels.csv"))) as csvfile:
            reader = csv.reader(csvfile, delimiter=",", quotechar="'")
            for row in reader:
                labels[row[0]] = row[1]

        for imgFile in imgFiles:
            img = cv2.imread(str(imgFile.resolve()))
            for angle in range(-20, 21, 1):
                height, width = img.shape[:2]
                imageCenter = (width / 2,height / 2,)
                rotationMat = cv2.getRotationMatrix2D(imageCenter, angle, 1.0)

                # Корректируем размеры изображения
                #Вычисялем косинус и синус угла поворота
                absCos = abs(rotationMat[0, 0])
                absSin = abs(rotationMat[0, 1])

                #Вычисляем новые размеры складывая катеты боковых треугольников
                bound_w = int(height * absSin + width * absCos)
                bound_h = int(height * absCos + width * absSin)

                # Центрируем изображения
                rotationMat[0, 2] += bound_w / 2 - imageCenter[0]
                rotationMat[1, 2] += bound_h / 2 - imageCenter[1]

                # Поворачиваем по новой матрице
                rotatedMat = cv2.warpAffine(img, rotationMat, (bound_w,bound_h))
                # Записываем новое изображение
                new_file_name = (imgFile.name[0: len(imgFile.name) - 4] + "_" + str(angle) + ".jpg")
                output_str = newDatasetName + "/" + new_file_name
                cv2.imwrite(output_str,rotatedMat,)
                csv_str += new_file_name + "," + labels[imgFile.name] + "\n"

        with open(newDatasetName + "\labels.csv", "w") as text_file:
            text_file.write(csv_str)
    def createAugmentationBox(self,datasetName,newDatasetName):
        imgFiles = list(pathlib.Path(str(relativaPath(datasetName))).glob("*.jpg"))
        boxFiles = list(pathlib.Path(str(relativaPath(datasetName))).glob("*.box"))

        for (index,imgFile) in enumerate(imgFiles):
            img = cv2.imread(str(imgFile.resolve()))
            boxFile = open(boxFiles[index],'r')
            boxes = boxFile.readlines()
            boxFile.close()
            #print(boxes)
            for angle in range(-20, 21, 1):
                height, width = img.shape[:2]
                imageCenter = (width / 2,height / 2,)
                rotationMat = cv2.getRotationMatrix2D(imageCenter, -angle, 1.0)

                # Корректируем размеры изображения
                #Вычисялем косинус и синус угла поворота
                absCos = abs(rotationMat[0, 0])
                absSin = abs(rotationMat[0, 1])

                #Вычисляем новые размеры складывая катеты боковых треугольников
                bound_w = int(height * absSin + width * absCos)
                bound_h = int(height * absCos + width * absSin)

                # Центрируем изображения
                rotationMat[0, 2] += bound_w / 2 - imageCenter[0]
                rotationMat[1, 2] += bound_h / 2 - imageCenter[1]

                # Поворачиваем по новой матрице
                outputBox = ""
                for box in boxes:
                    boxElems = box.split(' ')
                    outputBox +=boxElems[0]
                    boxCoords = boxElems[1:]
                    for i in range(0,len(boxCoords)-1,2):
                        point = np.array([[int(boxCoords[i])] ,[int(boxCoords[i+1])],[1]])
                        newPoint = rotationMat @ point
                        outputBox +=f' {math.ceil(newPoint[0])} {math.ceil(newPoint[1])}'
                    outputBox+=' 0\n'
                # Записываем новое изображение
                new_file_name = (boxFiles[index].name[0: len(boxFiles[index].name) - 4] + "_" + str(angle) + ".box")
                print(new_file_name)
                output_str = newDatasetName + "/" + new_file_name
                newBox = open(output_str,'w')
                newBox.write(outputBox)
                newBox.close()


AugmentationDataset().createAugmentation("dataset","dataset2")
AugmentationDataset().createAugmentationBox("dataset","dataset2")