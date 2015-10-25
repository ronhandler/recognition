#! /usr/bin/python

import cv2
import numpy as np
#from ron_cap import dist

class Hog_D(object):
    def __init__(self):
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.hogParams = {'winStride': (4, 4), 'padding': (32, 32), 'scale': 1.05}
        self.black_list = []

    def build_black_list(self, im):
        result, w = self.hog.detectMultiScale(im, **(self.hogParams))
        for res in result:
            if res not in black_list:
                self.black_list.append(res) 

    def get(self, im):
        result, w = self.hog.detectMultiScale(im, **(self.hogParams))
        r = None
        if len(result[0])>0:
            for res in result:
                for b in black_list:
                    if dist(b, res) > 5:
                        r = res
        return r
