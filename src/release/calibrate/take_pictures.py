#!/usr/bin/env python

import os
import cv2
import ConfigParser

# Change dir the script's location.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

config = ConfigParser.RawConfigParser()
config.read('../config.txt')

WIDTH = config.getint("general", "width")
HEIGHT = config.getint("general", "height")
URL = config.get("general", "url")
CAL_SAVE_PATH = config.get("calibrate_paths", "cal_save")
UPSIDE_DOWN_LIST = config.get("general", "upside_down_list")
HEADER = "camera "
CAMERA_LIST = config.get("odroid", "camera_list").split(",")
CAM_QUANTITY = len(CAMERA_LIST)
# CAM_QUANTITY = config.getint("general", "max_cam_number")
path = '~/samples'
os.chdir(os.path.expanduser(path))


if __name__ == "__main__":
    for i in range(0, CAM_QUANTITY):
        # cap = cv2.VideoCapture(i)
        for j in range(0, 100):
            cap = cv2.VideoCapture(URL + CAMERA_LIST[i] + ":800" + CAMERA_LIST[i] + "/img.png")
            ret, img = cap.read()
            if img is not None:
                print j
                for k in UPSIDE_DOWN_LIST.split(","):
                    if k == CAMERA_LIST[i]:
                        img = cv2.flip(img, 0)
                        img = cv2.flip(img, 1)
                rval = cv2.imwrite("sample" + CAMERA_LIST[i] + str(j) + ".jpg", img)
            cap.release()

