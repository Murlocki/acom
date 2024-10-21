import statistics
from abc import ABC,abstractmethod
from difflib import SequenceMatcher



class Checker(ABC):
    @abstractmethod
    def checkOne(self,result,truth):
        pass
    @staticmethod
    def setDefault():
        FullCorrect.value = 0

    @abstractmethod
    def checkList(self, results, truth):
        pass

    @abstractmethod
    def endOutput(self, imagesCount):
        return ""
class FullCorrect(Checker):
    value = 0
    @staticmethod
    def setDefault():
        FullCorrect.value = 0
    def checkOne(self, result, truth):
        if (result.lower() == truth.lower()):
            FullCorrect.value += 1
        return FullCorrect.value
    def checkList(self,results,truth):
        for result in results:
            if (result.lower() == truth.lower()):
                FullCorrect.value += 1
                break
        return FullCorrect.value

    def endOutput(self, imagesCount):
        return f"Угадано {FullCorrect.value} / {imagesCount} капч"


class Similarity(Checker):
    value = []

    @staticmethod
    def setDefault():
        Similarity.value = []

    def checkList(self,results,truth):
        max_similarity = 0
        for result in results:
            similarity = SequenceMatcher(
                None, truth.lower(), result.lower()
            ).ratio()
            max_similarity = max(similarity, max_similarity)
        Similarity.value.append(max_similarity)
        return Similarity.value
    def checkOne(self, result, truth):
        similarity = SequenceMatcher(
            None, truth.lower(), result.lower()
        ).ratio()
        Similarity.value.append(similarity)
        return Similarity.value

    def endOutput(self, imagesCount):
        return f"Средняя схожесть: {statistics.fmean(Similarity.value) * 100}%"

