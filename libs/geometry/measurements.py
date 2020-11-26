from libs.geometry.point import vector
import math
class measure:
    '''
    calculates the angle between you and the target

    fov - in radians
    p - input point
    img_size - in pixles
    return - tuple of angles in radians
    '''
    @staticmethod
    def measure_angle(p :vector,img_size :tuple,fov :tuple):
        img_size[0] /= 2
        img_size[1] /= 2

        n = (p - vector(img_size[0],img_size[1]))

        n.x /= img_size[0]
        n.y /= img_size[1]

        vp = vector(math.tan(fov[0]),math.tan(fov[1]))*2

        f = n
        f.x *= vp.x
        f.y *= vp.y

        return (math.tan(f.x),math.tan(f.y))