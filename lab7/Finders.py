import re

import cv2
from pytesseract import pytesseract
from abc import ABC,abstractmethod


class BaseFinder(ABC):
    @abstractmethod
    def process(self,img,**kwargs):
        pass

class Straight(BaseFinder):
    def process(self,img,**kwargs):
        return pytesseract.image_to_string(img, lang="rus+eng")

class Boxes(BaseFinder):
    def process(self,img,**kwargs):
        h, w = img.shape
        boxes = pytesseract.image_to_boxes(img, lang="rus+eng")

        for box in boxes.splitlines():
            boxData = box.split(" ")
            cv2.rectangle(img, (int(boxData[1]), h - int(boxData[2])), (int(boxData[3]), h - int(boxData[4])),
                          (0, 255, 0), 2, )
        return  "".join([sym_data.split(" ")[0] for sym_data in boxes.split("\n")])

class AverageOfAug(BaseFinder):
    value = {}
    truths = {}
    def process(self,img,**kwargs):
        result = pytesseract.image_to_string(img, lang="rus+eng")

        imgName = kwargs['imgFile'].name.split("_")[0]
        if imgName in AverageOfAug.value:
            AverageOfAug.value[imgName].append(result)
        else:
            AverageOfAug.value[imgName] = [result]
            AverageOfAug.truths[imgName] = kwargs['groud_truth']

        return result


class Filtered(BaseFinder):
    @staticmethod
    def clearStr(string):
        string = string.lower()
        string = re.sub(
            r"[0123456789\!\#\$\%\^\&\*\(\)\_\~@\`\n\/\|\,\"\<\°\„\?\.\«\’\‚\”\“\®\¥\>\`\'\—\™\‘\:\ \]\[\{\}\=\+\-\\]",
            " ", string, )
        return str(string).rstrip().lstrip()
    def process(self,img,**kwargs):
        result = pytesseract.image_to_string(img, lang="rus+eng")
        return Filtered.clearStr(result)