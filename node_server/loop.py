#!/usr/bin/env python
import cv2
import time
import os, sys

cap = cv2.VideoCapture(0)
ret, new_image = cap.read()
cv2.imwrite('public/img.png', new_image)
while True:
    ret, new_image = cap.read()
    cv2.imwrite('public/img1.png', new_image)
    #time.sleep(0.5)
    os.remove('public/img.png')
    os.rename('public/img1.png', 'public/img.png')
