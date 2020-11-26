import cv2
from pathlib import Path
import os
import math
import json
defult_settings = {

}
class camera:
    """
    this class handles all the things that belong to the camera in the project
    the fetching of images and settings handling
    """
    def __init__(self,cam_path = 0,settings_path = "settings.json"):
        self.cap = cv2.VideoCapture(cam_path)
        self.settings_manager = cameraSettingsSaver(settings_path)
        
    def read(self):
        return self.cap.read()[1]
    
    def is_open(self):
        return self.cap.isOpened()

    def updateSettings(self,settings):
        self.settings_manager.updateSettings(settings)

    def close(self):
        self.settings_manager.saveSettings()
        self.cap.cl
class imagefetcher:
    '''
    imagefetcher class is a small class created to get images out of a directory

    note that all of the class expects that all of the files in the image directory are image files.
    '''
    def __init__(self,path = "images"):
        self.index = 0
        self.path = path
        self.images = os.listdir(self.path)

    def read(self):
        image_path = self.path.joinpath(self.images[self.index])
        print(image_path)
        return cv2.imread(image_path.__str__())

    def next(self):
        self.index = abs((self.index+1)%len(self.images))
    
    def prev(self):
        self.index = abs((self.index-1)%len(self.images))


defult_settings = {
    "size": [420,320],

}
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

    def saveSettings(self):
        with open(self.path,"w") as file:
            json.dump(self._settings,file)
    
    def getSettings(self):
        return self._settings

    def updateSettings(self,new_settings):
        self._settings = new_settings

