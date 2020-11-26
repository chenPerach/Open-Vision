from libs.geometry.point import vector
import math
class measure:
    """
    this is the class that does all the work
    
    handle all the important mathematicl calculations that the program will do
    """
    '''
    calculates the angle between you and the target

    fov - in radians
    p - input point
    img_size - in pixles
    return - tuple of angles in radians
    '''
    @staticmethod
    def measure_angle(p :vector,img_size :tuple,fov :tuple):
        
        f = measure._normalize_point(p,img_size,fov)

        return (math.tan(f.x),math.tan(f.y))

    '''
    this function does most of the work,
    it normalized the image a corrding to the img_size
    then it resizes it according to the fov
    '''
    @staticmethod
    def _normalize_point(p :vector,img_size :tuple,fov :tuple):
        # find the distance to the center of the image
        # normalize the point
        n = vector((p.x - img_size[0]/2)/(img_size[0]/2),(img_size[1]/2-p.y)/(img_size[1]/2))

        
        vp = vector(math.tan(fov[0]/2),math.tan(fov[1]/2))*2
        # resize according to the fov
        
        n.x *= vp.x
        n.y *= vp.y

        return n


    '''
    this method return a tuple specifing the distance to the target in the horizontal axis and vertical axis
    p1,p2 - 2 points you know the distance between
    img_size - the size of the image
    fov - image fov in radians
    real_distance - the real distance between p1 and p2
    angles - the angles in the vertical and horizantal direction in radians
    '''
    @staticmethod
    def get_distance(p1 :vector,p2:vector,img_size :tuple,fov :tuple,real_distance:float,angles:tuple):
        f1 = measure._normalize_point(p1,img_size,fov)
        f2 = measure._normalize_point(p2,img_size,fov)
        
        delta = f1-f2

        perpendicular_distance = real_distance/delta.size()

        horizontal_distance = perpendicular_distance*math.cos(angles[0])
        vertical_distance = perpendicular_distance*math.cos(angles[1])

        return (horizontal_distance,vertical_distance)
        
