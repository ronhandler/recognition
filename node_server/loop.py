#!/usr/bin/env python
import cv2
import time
import os, sys

cap = cv2.VideoCapture(0)
cap.set(3,320)
cap.set(4,240)
ret, new_image = cap.read()
cv2.imwrite('public/img.png', new_image)
while True:
    ret, new_image = cap.read()
    new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('public/img1.png', new_image)
    #time.sleep(0.5)
    os.remove('public/img.png')
    os.rename('public/img1.png', 'public/img.png')
