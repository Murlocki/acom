from overrides import overrides

from iz2.Operator import Operator


class SharOperator(Operator):
    @overrides
    def process(self,img,x,y)->tuple[float,float]:
        Gx = 3*int(img[x-1][y-1]) + 10*int(img[x-1][y]) + 3 * int(img[x-1][y+1]) -3 * int(img[x+1][y-1]) - 3 * int(img[x+1][y]) - 10 * int(img[x+1][y+1])
        Gy = 3 * int(img[x-1][y-1]) - 3 * int(img[x-1][y+1]) + 10 * int(img[x][y-1]) - 10 * int(img[x][y+1]) + 3 * int(img[x+1][y-1]) - 3 * int(img[x+1][y+1])
        return (Gx,Gy)