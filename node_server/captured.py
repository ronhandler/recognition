#! /usr/bin/python

import cv2
#import numpy as np
import time
from hog_try import Hog_D

streams = [
"0"#,
#"1"#,
#"2",
#"3",
#"4",
#"5",
#"6",
#"7"
]
h = Hog_D()
while True:
    for i in streams:
        cap = cv2.VideoCapture("http://192.168.1.20"+ i +":800" + i +"/img.png")
        ret, image = cap.read()
        if image is not None:
            r = h.hog_f(image)
            if r is not None:
                cv2.rectangle(image, (r[0],r[1]), (r[0]+r[2],r[1]+r[3]), (0,255,0), 5)
            cv2.imshow("people detector "+str(i), image)
    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()
