#!/usr/bin/env python
import cv2
import time
import os, sys
import numpy as np

CAM_QUANTITY = 8

def mouse_handler(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        images[param] = np.copy(temp_images[param])
        cv2.imshow("header"+str(param),images[param])
        cv2.circle(images[param],(x,y),25,(255,0,0),3) 
    if event == cv2.EVENT_RBUTTONDOWN:
        images[param] = np.copy(temp_images[param])
        cv2.imshow("header_x",images[param])

def enter_handler():
    x = raw_input("Please, enter the X!!!")
    return x

temp_images = [None]*8
images = [None]*8

for i in range (0, CAM_QUANTITY):    
    cv2.namedWindow("header"+str(i), cv2.WINDOW_OPENGL|cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback("header"+str(i), mouse_handler, i)

def pic_capture():
    for i in range (0, CAM_QUANTITY):
        cap = None
        while cap is None:
            print "Trying to capture"
            cap = cv2.VideoCapture("http://192.168.1.20"+str(i)+":800"+str(i)+"/img.png")
        ret, img = cap.read()
        temp_images[i] = img
        images[i] = img
        cap.release()
pic_capture()

while True:
    for i in range (0, CAM_QUANTITY):
        if images[i] is None:
            continue
        cv2.imshow("header"+str(i), images[i])
    
    k = cv2.waitKey(33)
    if k==27:   # Esc key
        exit(0)
    if k == 10 or k == 13:   # Return key
        print "Enter"

        y = enter_handler()
        print y
    if k == 114:
        #cv2.destroyAllWindows()
        pic_capture()
        continue
    if k==-1:
        continue
    #else:
        #print k
cv2.destroyAllWindows()
cap.release()
