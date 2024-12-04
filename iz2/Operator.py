from abc import ABC,abstractmethod

class Operator(ABC):
    @abstractmethod
    def process(self,img,x,y)->tuple[float,float]:
        return (0,0)