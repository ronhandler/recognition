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
        print result
        if len(result[0])>0 :
            r = result[0][0]
            cv2.rectangle(im, (r[0],r[1]), (r[0]+r[2],r[1]+r[3]), (0,255,0), 5)
        cv2.imshow("people detector", im)
