from libs.GUI_UTILS.sliders import Sliders
from libs.geometry.line import line
from libs.geometry.point import vector
from libs.image_provider.camera import *
import cv2
import numpy as np
import math

fov = 27.7665349671
tan_frame = math.tan(math.radians(fov))
tm = 0.325
class process:
    def __init__(self,path,using_camera = True):
        self.sliders = Sliders(isGUI=True,path = path)
        self.using_cam = using_camera
        settings_path = Path.joinpath(Path.cwd(),"json","settings.json")
        if(self.using_cam):
            self.settingsSlider = settingsSliders(settings_path=settings_path,isGUI=True)
            self.cam = camera(0,settings_path=settings_path)
        else: 
            self.image_fetcher = imagefetcher(path = Path.joinpath(Path.cwd(),"images"))

    
    def run(self):

        debug_messages = []
        if (self.using_cam):
            if(not self.cam.is_open()):
                print("cam closed. waiting")
                return # wait until the camera is opened

            self.cam.updateSettings(self.settingsSlider.getSettings())
            img = self.cam.read()
        else:
            img = self.image_fetcher.read() 
        
        img = cv2.resize(img,(420,320),interpolation=cv2.INTER_AREA)
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)

        upper,lower = self.sliders.getHSV()

        mask_img = cv2.inRange(hsv_img,lower,upper)
        bit_img = cv2.bitwise_and(img,img,mask = mask_img)

        mid_frame  = img.shape[1]/2

        contours, _ = cv2.findContours(mask_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        filtered_contours = []

        for cnt in contours:
            if(cv2.contourArea(cnt) > 150):
                x,y,w,h = cv2.boundingRect(cnt)
                filtered_contours.append((cnt,x))        
        
        #sort the contours from left to right
        sorted(filtered_contours,key = lambda x: x[1])
        filtered_contours = [cnt[0] for cnt in filtered_contours]

        results = []
        for i in range(0 ,len(filtered_contours)-1, 1):
            # find the middle y value of both rectangles
            _,y_1,_,h_1 = cv2.boundingRect(filtered_contours[i])
            _,y_2,_,h_2 = cv2.boundingRect(filtered_contours[i+1])
            mid_y  = (y_1+y_2+(h_1+h_2)/2)/2

            #get the lines from the contors
            [vx_1,vy_1,x_1,y_1] = cv2.fitLine(filtered_contours[i], cv2.DIST_L2,0,0.01,0.01)
            [vx_2,vy_2,x_2,y_2] = cv2.fitLine(filtered_contours[i+1], cv2.DIST_L2,0,0.01,0.01)
            l1 = line(vector(x_1,y_1),vy_1/vx_1)
            l2 = line(vector(x_2,y_2),vy_2/vx_2)

            # find point of collision between those lines
            collision_point = l1.find_collision(l2)
            
            # if the collision point is lower then the mid_y then go to next couple of contors
            if collision_point.y >= mid_y: 
                continue

            # draw debug stuff
            cv2.line(bit_img,(int(collision_point.x),int(0)),(int(collision_point.x),int(mid_frame*2)),(255,0,0),2)
            
            





        return {
            "images": [
                {
                    "title": "image",
                    "image": img
                },
                {
                    "title": "bit wise image",
                    "image": bit_img    
                }
            ],
            "messages": debug_messages,
            "results": results
        }

        
    def end(self):
        cv2.destroyAllWindows()
        if self.using_cam:
            self.cam.close()
        self.sliders.writeHSVvals()
