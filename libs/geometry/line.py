from libs.geometry.point import vector
class line:
    def __init__(self,point:vector, slope:float):
        self.point = point
        self.slope = slope
        self.const = self.point.y - self.slope*self.point.x
    
    @classmethod
    def from2Points(cls, point1:vector, point2 :vector):
        point = point1
        slope = (point1 - point2).slope()
        return cls(point,slope)
    def get_y(self,x):
        return self.const + self.slope*x
    def find_collision(self,l2):

        x  = (l2.const - self.const)/(self.slope - l2.slope)
        y = self.get_y(x)
        return vector(x,y)
        