import cv2
from pathlib import Path
import os
import math
import json
import numpy as np
defult_settings = {
    "size": [420,320],
    "brightness": 100,
    "contrast": 100,
    "saturation":100,
    "gain":100,
}

class camera:
    """
    this class handles all the things that belong to the camera in the project
    the fetching of images and settings handling
    """
    def __init__(self,cam_path = 0,settings_path = "settings.json"):
        self._prev_settings = defult_settings
        self.cap = cv2.VideoCapture(cam_path)
        self.settings_manager = cameraSettingsSaver(settings_path)
        
    def read(self):
        return self.cap.read()[1]
    
    def is_open(self):
        return self.cap.isOpened()

    def updateSettings(self,settings, reload_from_file = False):
        if reload_from_file:
            self.settings_manager.reload()
        else:
            self.settings_manager.updateSettings(settings)
        new_settings = self.settings_manager.getSettings()
        if self._prev_settings != new_settings:
            print("setting the settings")
            ''' this doesn't work currently. may want to try it with a camera that's not built in '''
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,int(new_settings["size"][0])) 
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,int(new_settings["size"][1]))
            self.cap.set(cv2.CAP_PROP_BRIGHTNESS,int(new_settings["brightness"]))
            self.cap.set(cv2.CAP_PROP_CONTRAST,int(new_settings["contrast"]))
            self.cap.set(cv2.CAP_PROP_GAIN,int(new_settings["gain"]))
            self.cap.set(cv2.CAP_PROP_SATURATION,int(new_settings["saturation"]))
            self._prev_settings = new_settings

    def close(self):
        self.settings_manager.saveSettings()
        self.cap.release()


class imagefetcher:
    '''
    imagefetcher class is a small class created to get images out of a directory

    note that all of the class expects that all of the files in the image directory are image files.
    '''
    def __init__(self,path = "images"):
        self.index = 0
        self.path = path
        self.images = os.listdir(self.path)
        self.fov = (27.7665349671,27.7665349671)
        
    def read(self):
        image_path = self.path.joinpath(self.images[self.index])
        return cv2.imread(image_path.__str__())

    def next(self):
        self.index = abs((self.index+1)%len(self.images))
    
    def prev(self):
        self.index = abs((self.index-1)%len(self.images))



class cameraSettingsSaver:
    """
    a simple class that handles the saving of of camera settings
    """
    def __init__(self,path = "settings.json"):
        self.path = path
        try:
            self._settings = json.load(open(self.path))
        except:
            with open(self.path,"w") as file:
                json.dump(defult_settings,file)
            self._settings = json.load(open(self.path))
            pass

    def saveSettings(self):
        with open(self.path,"w") as file:
            json.dump(self._settings,file)
    
    def getSettings(self):
        return self._settings

    def reload(self):
        self._settings = json.load(open(self.path))

    def updateSettings(self,new_settings):
        self._settings = new_settings

class settingsSliders:
    """
    this is a debug class ment to create sliders for changing the camera settings
    it could be easly removed from the code
    """
    def __init__(self,settings_path = "settings.json",isGUI = True):
        self.settings = cameraSettingsSaver(settings_path)
        self.winName = "cam settings"
        self.isGUI = isGUI
        if(isGUI):
            self.createTrackBars()
    

    def createTrackBars(self):
        # Create a black image, a window
        img = np.zeros((1 ,1, 3), np.uint8)
        cv2.namedWindow(self.winName)
        
        settings_map = self.settings.getSettings()
        cv2.createTrackbar("brightness", self.winName, settings_map["brightness"], 255,lambda a: None)
        cv2.createTrackbar("contrast",   self.winName, settings_map["contrast"], 255,lambda a: None)
        cv2.createTrackbar("saturation", self.winName, settings_map["saturation"], 255,lambda a: None)
        cv2.createTrackbar("gain",       self.winName, settings_map["gain"], 255,lambda a: None)
    def getSettings(self):
        if self.isGUI:
            return  {
                "size": [420,320],
                "brightness": cv2.getTrackbarPos("brightness",self.winName),
                "contrast": cv2.getTrackbarPos("contrast",self.winName),
                "saturation":cv2.getTrackbarPos("saturation",self.winName),
                "gain": cv2.getTrackbarPos("gain",self.winName),
            }
