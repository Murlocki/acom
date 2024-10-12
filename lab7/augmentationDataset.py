import csv
import pathlib
import cv2


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

AugmentationDataset().createAugmentation("dataset","dataset2")