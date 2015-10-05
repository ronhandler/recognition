#!/usr/bin/env python
import os
# Change dir the script's location.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
import time
import pickle
import sys
import numpy as np
from WayPointClass import WayPoint
import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('../config.txt')

CAM_QUANTITY = config.getint("general", "max_cam_number")
URL = config.get("general", "url")
CAL_SAVE_PATH = config.get("calibrate_paths","cal_save")
HEADER = "camera "

current_wp = 0
temp_images = [None]*8
images = [None]*8
coords = (None, None)
waypoints = [{}]

def mouse_handler(event, x, y, flags, cam_id):
    if event == cv2.EVENT_LBUTTONDOWN:
        images[cam_id] = np.copy(temp_images[cam_id])
        cv2.imshow(HEADER+str(cam_id),images[cam_id])
        cv2.circle(images[cam_id],(x,y),25,(255,0,0),3) 
        wp = WayPoint()
        wp.cam_id = cam_id
        wp.cam_pos = (x, y)
        wp.phys_pos = coords
        waypoints[current_wp][cam_id] = wp
    if event == cv2.EVENT_MBUTTONDOWN:
        images[cam_id] = np.copy(temp_images[cam_id])
        del(waypoints[current_wp][cam_id])

def enter_handler():
    while True:
        res = raw_input("WP " +str(current_wp)+ ": Please, enter the physical position x,y: ")
        both = res.split(',')
        if len(both) != 2:
            print("Need two numbers separated with comma")
            continue
        try:
            ret = (int(both[0]),int(both[1]))
            return ret
        except:
            print("Parameters need to be integers")
            continue


def pic_capture():
    for i in range (0, CAM_QUANTITY):
        for j in range (0,3):
            cap = cv2.VideoCapture(URL+str(i)+":800"+str(i)+"/img.png")
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
        cv2.imshow(HEADER+str(i), images[i])
        cv2.setMouseCallback(HEADER+str(i), mouse_handler, i)


# Main function:
if __name__ == "__main__":

    coords =  enter_handler()
    pic_capture()

    while True:
        for i in range (0, CAM_QUANTITY):
            if images[i] is None:
                continue
            cv2.imshow(HEADER+str(i), images[i])
        
        k = cv2.waitKey(33)
        if k==27 or k==113:         # Esc key
            print("Exiting...")
            exit(0)
        if k == 105 or k == 10:     # Return key

            cv2.destroyAllWindows()
            for i in range (0,100):
                cv2.waitKey(10)

            # Increment the current waypoint number, and allocate another
            # dictionary.
            current_wp = current_wp + 1
            waypoints.append({})

            # Get the coordinates of the next physical position of waypoint.
            coords =  enter_handler()

            pic_capture()
            continue
        if k == 114:                # 'R' key
            print "Refreshing captured images..."
            pic_capture()
            waypoints.pop()
            waypoints.append({})
            continue
        if k == 115:                # 'S' key
            for i in range(0,len(waypoints)):
                print("WP " + str(i) + ":")
                for k,v in waypoints[i].items():
                    #print(str(k) + ":")
                    print(str(v))
                print("\n")
            with open(CAL_SAVE_PATH, "wb") as f:
                pickle.dump(waypoints, f, 0)
                #pickle.dump(waypoints[0], f, pickle.HIGHEST_PROTOCOL)
            continue
        if k==-1:                   # No key
            continue
        #else:
            #print k

    cap.release()
