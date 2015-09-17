#!/usr/bin/env python
import os.path
import cv2
import numpy as np
import time


cap = cv2.VideoCapture(0)
ret, new_image = cap.read()
cv2.imwrite('public/img.png', new_image)
time.sleep(0.2)

#if cv2.waitKey(1000)==27:
	#cap.release()
	#break
