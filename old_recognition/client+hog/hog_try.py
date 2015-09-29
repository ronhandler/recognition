#! /usr/bin/python

import cv2
import numpy as np

def hog_f(im):
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    hogParams = {'winStride': (8, 8), 'padding': (32, 32), 'scale': 1.05}

    #im = cv2.imread("img2.jpg")
    result = hog.detectMultiScale(im, **hogParams)
    r = result[0][0]

    cv2.rectangle(im, (r[0],r[1]), (r[0]+r[2],r[1]+r[3]), (0,255,0), 5)

    #cv2.namedWindow("people detector", 1)
    cv2.imshow("people detector", im)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    #h = hog.compute(im)
    #print type(h) 
