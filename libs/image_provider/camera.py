import cv2
from pathlib import Path
import os
import math
defult_settings = {

}
class camera:
    """
    this class handles all the things that belong to the camera in the project
    the fetching of images and settings handling
    """
    def __init__(self,path):
        self.cap = cv2.VideoCapture(path)
        
    def read(self):
        return self.cap.read()[1]

    def updateSettings(self,settings):
        pass        

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
    "size": [1920,1080],

}
class cameraSettingsSaver:
    """
    a simple class that handles the saving of of camera settings
    """
    def __init__(self,path = "settings.json"):
        self.path = path
        try:
            self.settings = json.load(open(self.path))
        except:
            with open(self.path,"w") as file:
                json.dump(defult_settings,file)
            self.settings = json.load(open(self.path))
        
class cameraSettings:
    """
    just a list of settings for the life cam 3000 that we are using

    note: every camera has a different interface changing the settings
    """
    def __init__(self,settingsMap):
        self.size = settingsMap["size"]

