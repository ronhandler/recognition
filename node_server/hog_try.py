#! /usr/bin/python

import cv2
import numpy as np

class Hog_D(object):
    def __init__(self):
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.hogParams = {'winStride': (4, 4), 'padding': (32, 32), 'scale': 1.05}


    def hog_f(self, im):
        result = self.hog.detectMultiScale(im, **(self.hogParams))
        r = None
        if len(result[0])>0 :
            r = result[0][0]
        return r
