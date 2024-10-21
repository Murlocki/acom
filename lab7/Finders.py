import re

import cv2
import numpy as np
from pytesseract import pytesseract
from abc import ABC,abstractmethod
from easyocr import easyocr
from scipy.spatial import distance


class BaseFinder(ABC):
    @abstractmethod
    def process(self,img,**kwargs):
        pass

    def setDefault(self):
        pass

class Straight(BaseFinder):
    def process(self,img,**kwargs):
        return pytesseract.image_to_string(img, lang="rus+eng")

class Boxes(BaseFinder):
    def process(self,image,**kwargs):
        h, w = image.shape[:2]
        boxes = pytesseract.image_to_boxes(image, lang="rus+eng")

        symbols = []
        centers = []

        # Обработка каждой коробки и сбор символов и их центров
        for box in boxes.splitlines():
            b = box.split(' ')
            char, x1, y1, x2, y2 = b[0], int(b[1]), int(b[2]), int(b[3]), int(b[4])
            y1, y2 = h - y1, h - y2  # Корректировка координат для OpenCV

            # Вырезаем изображение символа и определяем его центр
            symbol_image = image[y2:y1, x1:x2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            recognized_char = self.process_symbol(symbol_image)
            symbols.append((recognized_char, (cx, cy)))  # Сохраняем символ и его центр
            centers.append((cx, cy))

        # Создаем связи между центрами символов
        if(len(centers)>0):
            word_with_spaces = self.build_connections(symbols, centers)
            return word_with_spaces
        return ''
    def process_symbol(self, symbol_image):
        """Применяет connected components и распознает символ с вращением."""
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(symbol_image)

        recognized_chars = ""
        for i in range(1, num_labels):  # Пропускаем фон (label 0)
            x, y, w, h, _ = stats[i]
            component = symbol_image[y:y + h, x:x + w]

            char = self.rotate_and_recognize(component)
            recognized_chars += char

        return recognized_chars or "?"

    def rotate_and_recognize(self, component):
        """Вращает изображение и распознает символ."""
        for angle in range(0, 360, 10):
            rotated = self.rotate_image(component, angle)
            text = pytesseract.image_to_string(rotated,lang="rus+eng").strip()
            if text:
                return text
        return '?'  # Если ничего не распознано

    def rotate_image(self, image, angle):
        """Вспомогательная функция для вращения изображения."""
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, matrix, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        return rotated

    def build_connections(self, symbols, centers):
        """Создает связи между символами и вставляет пробелы на месте удаленных связей."""
        distances = distance.cdist(centers, centers)  # Матрица расстояний
        np.fill_diagonal(distances, np.inf)  # Исключаем самих себя

        # Собираем все связи с их длинами
        edges = [
            (i, j, distances[i, j])
            for i in range(len(centers)) for j in range(i + 1, len(centers))
        ]

        # Находим две самые длинные связи и удаляем их
        longest_edges = sorted(edges, key=lambda x: x[2], reverse=True)[:2]
        removed_indices = set((edge[0], edge[1]) for edge in longest_edges)

        # Создаем итоговое слово с пробелами
        word = []
        for i, (char, _) in enumerate(symbols):
            word.append(char)
            # Если между текущим и следующим символом была удаленная связь, добавляем пробел
            if any((i, i + 1) in removed_indices or (i + 1, i) in removed_indices for _ in range(2)):
                word.append(' ')

        return ''.join(word).strip()


class AverageOfAug(BaseFinder):
    value = {}
    truths = {}
    def setDefault(self):
        AverageOfAug.value = {}
        AverageOfAug.truths = {}
    def process(self,img,**kwargs):
        result = pytesseract.image_to_string(img, lang="rus+eng")

        imgName = kwargs['imgFile'].name.split("_")[0]
        if imgName in AverageOfAug.value:
            AverageOfAug.value[imgName].append(result)
        else:
            AverageOfAug.value[imgName] = [result]
            AverageOfAug.truths[imgName] = kwargs['groud_truth']

        return result

class EasyOcr(BaseFinder):
    def process(self,img,**kwargs):
        reader = easyocr.Reader(["en", "ru"])
        # reader = easyocr.Reader(
        #     ["ru"],
        #     user_network_directory="trainEasyOcr/user_network",
        #     model_storage_directory="trainEasyOcr/model",
        #     recog_network="train_easy",
        # )
        result_easy = reader.readtext(img, detail=0, paragraph=True)

        result = ""
        for i in result_easy:
            result += i
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