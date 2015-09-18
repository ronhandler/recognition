#!/usr/bin/env python
import cv2
import time


cap = cv2.VideoCapture(0)
ret, new_image = cap.read()
cv2.imwrite('public/img.png', new_image)
#time.sleep(0.01)

#if cv2.waitKey(1000)==27:
	#cap.release()
	#break
