#!/usr/bin/env python
import cv2
import time
import os, sys
import numpy as np
from WayPointClass import WayPoint

CAM_QUANTITY = 8

def mouse_handler(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        images[param[0]] = np.copy(temp_images[param[0]])
        cv2.imshow("header"+str(param[0]),images[param[0]])
        cv2.circle(images[param[0]],(x,y),25,(255,0,0),3) 
        if param[1] is not None and param[2] is not None:
            wp = WayPoint(param[0], param[1], param[2])
            #print wp
            wp.set_cam_position(x,y)
            temp_WP[param[0]] = wp
    if event == cv2.EVENT_RBUTTONDOWN:
        images[param[0]] = np.copy(temp_images[param[0]])
        #cv2.imshow("header_x",images[param])

def enter_handler():
    x = raw_input("Please, enter the physical position:").split(',')
    return x


def pic_capture(phy_p_x, phy_p_y):
    #for i in range (0, CAM_QUANTITY):    
        #cv2.namedWindow("header"+str(i), cv2.WINDOW_OPENGL|cv2.WINDOW_AUTOSIZE)
        #cv2.setMouseCallback("header"+str(i), mouse_handler, i)

    for i in range (0, CAM_QUANTITY):
        for j in range (0,3):
            cap = cv2.VideoCapture("http://192.168.1.20"+str(i)+":800"+str(i)+"/img.png")
            if cap is not None:
                break
        ret, img = cap.read()
        if img is not None:
            temp_images[i] = np.copy(img)
            images[i] = np.copy(img)
        cap.release()

    for i in range (0, CAM_QUANTITY):
        if images[i] is None:
            continue
        cv2.imshow("header"+str(i), images[i])
        cv2.setMouseCallback("header"+str(i), mouse_handler, (i,phy_p_x,phy_p_y))

#?#wp_cam_pos_center = [None]*

temp_images = [None]*8
images = [None]*8
temp_WP = [None]*8
WP = [None]*8

pic_capture(None, None)

while True:
    for i in range (0, CAM_QUANTITY):
        if images[i] is None:
            continue
        cv2.imshow("header"+str(i), images[i])
    
    k = cv2.waitKey(33)
    if k==27:   # Esc key
        exit(0)
    # if k == Enter
    if k == 105:   # Return key

        cv2.destroyAllWindows()
        #for i in range (0,1000):
            #cv2.waitKey(10)

        coord = enter_handler()
        coord_x = int(coord[0])
        coord_y = int(coord[1])
        pic_capture(coord_x, coord_y)
        continue
    #if k == r
    if k == 114:
        print "R is pressed"
        pic_capture(None, None)
        continue
    #if k == s
    if k == 115:
        WP = temp_WP
        for i in WP:
            print i
        continue
    
    if k==-1:
        continue
    else:
        print k

cap.release()
