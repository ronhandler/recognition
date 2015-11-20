#!/usr/bin/python

import numpy as np
import time
import cv2
import sys

img = cv2.imread("map.png")

i = 0
try:
    while True:
        cv2.line(img,(0+i,0),(50,110),(255,0,0),2)
        cv2.line(img,(50+i,110),(200,100),(255,255,0),2)
        cv2.imshow("title", img)
        k = cv2.waitKey(500)


except KeyboardInterrupt:
    cv2.destroyAllWindows()
    sys.exit(0)
