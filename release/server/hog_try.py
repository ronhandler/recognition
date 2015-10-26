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
        result = self.hog.detectMultiScale(im, **(self.hogParams))
        if len(result) == 2:
            if result not in self.black_list:
                self.black_list.append(result)
        if len(result) > 3:
            for i in range(0, len(result),2): #step of two
                res = (result[i], result[i+1])
                if res not in self.black_list:
                    self.black_list.append(res)
        if len(result) == 0:
            return

    def get(self, im):
        result = self.hog.detectMultiScale(im, **(self.hogParams))
        r = None
        if len(result)>0 and len(result[0])>0:
            print len(result)
            #for res in result:
                #print type(self.black_list)
                #for b in self.black_list:
                    #print "for b in black_list"
                    #print dist(b, res)
                    #if dist(b, res) > 5:
            r = result[0][0]
        return r
