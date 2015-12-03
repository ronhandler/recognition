#!/usr/bin/env python
import cv2
import os
import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('../config.txt')

WIDTH = config.getint("general", "width")
HEIGHT = config.getint("general", "height")
IMG1_PATH = config.get("capture_paths", "temp_image")
IMG_PATH = config.get("capture_paths", "final_image")

cap = cv2.VideoCapture(0)
cap.set(3, WIDTH)
cap.set(4, HEIGHT)

ret, new_image = cap.read()
cv2.imwrite(IMG_PATH, new_image)
while True:
    ret, new_image = cap.read()
    #new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(IMG1_PATH, new_image)
    #time.sleep(0.5)
    os.remove(IMG_PATH)
    os.rename(IMG1_PATH, IMG_PATH)
