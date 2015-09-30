#!/usr/bin/env python
import cv2
import time
import os, sys

def mouse_handler(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(str(x) + "," + str(y))
    if event == cv2.EVENT_RBUTTONDOWN:
        print("Right button")

img = cv2.imread("img.png")
cv2.imshow("header", img)
cv2.setMouseCallback("header", mouse_handler)
while True:
    k = cv2.waitKey(33)
    if k==27:   # Esc key
        exit(0)
    if k==10:   # Return key
        pass
    if k==-1:
        continue
