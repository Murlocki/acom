from overrides import overrides

from iz2.Operator import Operator


class PriutOperator(Operator):
    @overrides
    def process(self,img,x,y)->tuple[float,float]:
        Gx = -int(img[x-1][y-1]) + int(img[x-1][y+1]) - int(img[x][y-1]) + int(img[x][y+1]) - int(img[x+1][y-1]) + int(img[x+1][y+1])
        Gy = -int(img[x-1][y-1]) - int(img[x-1][y]) - int(img[x-1][y+1]) + int(img[x+1][y-1]) + int(img[x+1][y]) + int(img[x+1][y+1])
        return (Gx,Gy)
