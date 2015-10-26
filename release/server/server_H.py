#! /usr/bin/python
import os
# Change dir the script's location.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.append("../calibrate")
import math
import cv2
import urllib
import numpy as np
from hog_try import Hog_D
import time
import datetime
import signal
import threading
from threading import Lock
import pickle
from WayPointClass import WayPoint
import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('../config.txt')

LEARN_MODE = 1000
FROM_ODROID = True
DEBUG_LEVEL = config.getint("general", "debug_level")
URL = config.get("general", "url")
CAL_SAVE_PATH = config.get("calibrate_paths","cal_save")
UPSIDE_DOWN_LIST = config.get("general","upside_down_list")
CAMERA_LIST = config.get("odroid","camera_list").split(",")
#CAMERA_LIST = ["0"]
MAX_CAM_NUMBER = len(CAMERA_LIST)
#MAX_CAM_NUMBER = config.getint("general", "max_cam_number")

def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    try:
        resp = urllib.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        "npArray transformed"
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        return image
    except:
        return None

class capture(threading.Thread):

    def __init__(self, i, l):
        threading.Thread.__init__(self)
        self.i = i
        self.l = l
        self.running = True
        self.h = Hog_D()
        self.hog = None
        self.image = None
        self.upside_down = False
        for j in UPSIDE_DOWN_LIST.split(","):
            if j == str(self.i):
                self.upside_down = True

    def stop(self):
        self.running = False

    def getHog(self):
        r = self.hog
        return r

    def getImage(self):
        img = self.image
        # Rotate image if it was recorded upside down.
        if self.upside_down == True:
            img = cv2.flip(img, 0)
            img = cv2.flip(img, 1)
        return img

    def run(self):
        i = self.i
        while self.running == True:
            #print "Into"
            self.l.acquire()
            if FROM_ODROID == True:
                image = url_to_image(URL+ CAMERA_LIST[i] +":800" + CAMERA_LIST[i] +"/img.png")
            else:
                cap = cv2.VideoCapture(int(CAMERA_LIST[i]))
                cap.set(3,320)
                cap.set(4,240)
                _ret, image = cap.read()
                cap.release()
            self.image = image
            self.l.release()

            # Run the hog algorithm to find the location of the human being.
            if image is not None:
                self.l.acquire()
                hog = self.h.get(image)
                self.hog = hog
                self.l.release()

def dist(p1, p2):
    return math.sqrt( (p2[1] - p1[1])**2 + (p2[0] - p1[0])**2 )

def getPhysicalPosition(hog_results_list):
            mind = float('inf')
            min_hog = None
            for i in range(0, MAX_CAM_NUMBER):
                r = hog_results_list[i]
                dists = []
                if r == None: # If hog result is None we can skip.
                    continue
                for w in waypoints:
                    for k,v in w.items():
                        p1 = (r[0], r[1])
                        p2 = (v.cam_pos[0], v.cam_pos[1])
                        d = dist(p1, p2)
                        if d != None:
                            dists.append((v, d))
                            #print("Distance is: " + str(d))
                for j in range(0, len(dists)):
                    if mind > dists[j][1]:
                        mind = dists[j][1]
                        min_hog = dists[j][0]
            if min_hog != None:
                #print("Minimum distance found at physical position:" + str(min_hog.phys_pos) + " (wp:" + str(min_hog.wp_id) + ")")
                sys.stdout.write("\rPosition: " + str(min_hog.phys_pos))
                sys.stdout.flush()
                pass

if __name__ == '__main__':
    process_list = [None]*MAX_CAM_NUMBER

    waypoints = pickle.load(open(CAL_SAVE_PATH, "rb"))
    #for i in range(0,len(waypoints)):
        #print("WP " + str(i) + ":")
        #for k,v in waypoints[i].items():
            ##print(str(k) + ":")
            #print(str(v))
        #print("\n")
    #exit(-1)

    try:
        lock = Lock()
        for i in range(0, MAX_CAM_NUMBER):
            my_thread = capture(i, lock)
            my_thread.start()
            process_list[i] = my_thread
            print "Thread"+ str(i) + "started"

        while True:
            loop_results = [None]*MAX_CAM_NUMBER

           #for j in range(0, 50000):
           #    for i in range(0, MAX_CAM_NUMBER):
           #        print i
           #        image = process_list[i].getImage()
           #        #print type(image)
           #        if image is not None:
           #            hog = process_list[i].getHog()
           #            hog.build_black_list(image)
           #            print hog.black_list[i]
           #            cv2.waitKey(1)
           #print "Done"

            for i in range(0, MAX_CAM_NUMBER):
                image = process_list[i].getImage()
                hog = process_list[i].getHog()
                if hog is not None and LEARN_MODE > 0:
                    #hog.build_black_list(image)
                    #LEARN_MODE -= 1
                    #print LEARN_MODE
                    pass
                else:
                    loop_results[i] = hog
                if image is not None:
                    if hog is not None:
                        r = hog
                        cv2.rectangle(image, (r[0],r[1]), (r[0]+r[2],r[1]+r[3]), (0,255,0), 5)
                    if LEARN_MODE > 0:
                        cv2.putText(image,"Learning Mode", (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2) 
                    cv2.imshow("people detector "+CAMERA_LIST[i], image)
                    cv2.waitKey(1)
            # Now we have a loop_result list that contains tuples of image
            # and human position.
            # What is left to do is to find the closest waypoint that
            # matches them.
            getPhysicalPosition(loop_results)

    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        for i in range(0, MAX_CAM_NUMBER):
            print "Terminating process "+ str(i) + " with camera "+ CAMERA_LIST[i]
            process_list[i].stop()
        print "Exiting."
        sys.exit(0)