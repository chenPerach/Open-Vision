import cv2
import numpy as np
import math
import json
from pathlib import Path
class Sliders:
    '''
    this 'Sliders' is a simple class disgnd to
    abstarct the rigorous creation process of the trackbars away from the user

    this class also handles the saving of data to a json file
    '''
    def __init__(self,winName = "sliders",isGUI = False,path = Path.joinpath(Path.cwd(),"HSVdata.json") ):
        self.winName = winName
        self.isGUI = isGUI
        self.path = path
        try:
            self.vals = json.load(open(self.path)) #try opening the file
        except:
            with open(self.path,"w") as outFile: # if opening the file doesn't work then create it.
                json.dump({"H min": 0, "H max": 0, "S min": 0, "S max": 0, "V min": 0, "V max": 0},outFile)
            self.vals = json.load(open(self.path)) # and then open the file
        
        if self.isGUI:
            self.createTrackBars()
        
    def writeHSVvals(self):
        '''
        saves the trackbar data in the file
        '''
        #puts the json thingy in to a txt file
        with open(self.path,"w") as outFile:
            json.dump(self.vals,outFile)

    # returns the hsv values to the user
    def getHSV(self):
        if self.isGUI:
            self.vals = { 
                "H min": cv2.getTrackbarPos("H min", self.winName),
                "H max": cv2.getTrackbarPos("H max", self.winName),
                "S min": cv2.getTrackbarPos("S min", self.winName),
                "S max": cv2.getTrackbarPos("S max", self.winName),
                "V min": cv2.getTrackbarPos("V min", self.winName),
                "V max": cv2.getTrackbarPos("V max", self.winName),
            }
        Upper = np.array([
            self.vals["H max"],self.vals["S max"],self.vals["V max"]
            ])

        Lower = np.array([
            self.vals["H min"],self.vals["S min"],self.vals["V min"]
        ])
        return Upper,Lower
    #creates the trackbars sliders window
    def createTrackBars(self):
        # Create a black image, a window
        img = np.zeros((1 ,1, 3), np.uint8)
        cv2.namedWindow(self.winName)
        
        # create trackbars for color change
        cv2.createTrackbar('H min', self.winName, self.vals["H min"], 255,lambda a: None)
        cv2.createTrackbar('S min', self.winName, self.vals["S min"], 255,lambda a: None)
        cv2.createTrackbar('V min', self.winName, self.vals["V min"], 255,lambda a: None)
        cv2.createTrackbar('H max', self.winName, self.vals["H max"], 255,lambda a: None)
        cv2.createTrackbar('S max', self.winName, self.vals["S max"], 255,lambda a: None)
        cv2.createTrackbar('V max', self.winName, self.vals["V max"], 255,lambda a: None)
        #return img
    