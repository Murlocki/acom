import csv
import pathlib
import re
import statistics
from difflib import SequenceMatcher

import cv2
from pytesseract import pytesseract

from lab7.Checkers import FullCorrect, Similarity
from lab7.Finders import Straight, AverageOfAug, Boxes, Filtered
from lab7.augmentationDataset import AugmentationDataset


def relativePath(relPath):
    path = pathlib.Path(__file__).parent / relPath
    return path



class Tesseract:
    def __init__(self, recType, valType):
        self.valType = valType
        self.recType = recType
        if valType == "full_correct":
            self.check = FullCorrect()
        elif valType == "similarity":
            self.check = Similarity()

        if recType == "straight_recognition":
            self.finder = Straight()
        elif recType== "boxes_recognition":
            self.finder = Boxes()
        elif recType== "avg_of_aug":
            self.finder = AverageOfAug()
        elif recType == "filtered_recognition":
            self.finder = Filtered()
    def testRecognition(self, datasetName, showImg=False):
        outputStr = ""
        labels = {}
        imagesCount = 0

        with open(str(relativePath(datasetName + "/labels.csv")), newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=",", quotechar="'")
            for row in reader:
                labels[row[0]] = row[1]

        imgFiles = list(
            pathlib.Path(str(relativePath(datasetName + "/"))).glob("*.jpg")
        )


        for imgFile in imgFiles:
            img = cv2.imread(str(imgFile.resolve()), 0)
            groud_truth = labels[imgFile.name]

            result = self.finder.process(img,groud_truth=groud_truth,imgFile=imgFile)

            result = "".join(result.splitlines())

            outputStr += f"{imgFile.name} | {groud_truth} | {result}\n"
            print(f"{imgFile.name} | {groud_truth} | {result}\n")
            self.check.checkOne(result, groud_truth)

            imagesCount += 1

            # print(result)
            if showImg:
                cv2.imshow("capthca", img)
                cv2.waitKey()

        outputStr += "\n"

        if self.recType == "avg_of_aug":
            imagesCount = 0
            self.check.setValueDefault()
            for key in self.finder.value.keys():
                results = self.finder.value[key]
                groud_truth = self.finder.truths[key]
                self.check.checkList(results,groud_truth)
                imagesCount += 1

        outputStr += self.check.endOutput(imagesCount)

        with open(str(relativePath("results_" + self.valType + "_" + self.recType + "_" + datasetName + ".txt")), "w",
                  encoding="utf-8", ) as f:
            f.write(outputStr)


#Tesseract("avg_of_aug", "full_correct").testRecognition("dataset3", showImg=False)
#Tesseract("avg_of_aug", "similarity").testRecognition("dataset3", showImg=False)
#Tesseract("straight_recognition", "full_correct").testRecognition("dataset", showImg=False)
#Tesseract("straight_recognition", "similarity").testRecognition( "dataset", showImg=False)
#Tesseract("boxes_recognition", "full_correct").testRecognition("dataset", showImg=False)
#Tesseract("boxes_recognition", "similarity").testRecognition("dataset", showImg=False)

# Tesseract("filtered_recognition", "full_correct").testRecognition("dataset2", showImg=False)
# Tesseract("filtered_recognition", "similarity").testRecognition("dataset", showImg=False)
# Tesseract("filtered_recognition", "similarity").testRecognition("dataset2", showImg=False)
# Tesseract("filtered_recognition", "full_correct").testRecognition("dataset", showImg=False)