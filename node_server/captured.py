#! /usr/bin/python

import cv2
#import numpy as np
import time
from hog_try import Hog_D

streams = [
#"0",
#"1",
#"2",
"3"
]
h = Hog_D()
while True:
    for i in streams:
        cap = cv2.VideoCapture("http://192.168.1.20"+ i +":8000/img.png")
        ret, image = cap.read()
        if image is not None:
            h.hog_f(image)
            #cv2.imshow(i,image)
    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()
