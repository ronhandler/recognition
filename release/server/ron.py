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
import threading
import pickle
from WayPointClass import WayPoint
import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('../config.txt')

DEBUG_LEVEL = config.getint("general", "debug_level")
URL = config.get("general", "url")
CAL_SAVE_PATH = config.get("calibrate_paths","cal_save")
UPSIDE_DOWN_LIST = config.get("general","upside_down_list")
CAMERA_LIST = config.get("odroid","camera_list").split(",")

def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    try:
        resp = urllib.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        return cv2.imdecode(image, cv2.IMREAD_COLOR)
    except:
        return None

class PeopleDetector(object):
    def __init__(self):
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.hogParams = {'winStride': (4, 4), 'padding': (32, 32), 'scale': 1.05}
    def get(self, im):
        result = self.hog.detectMultiScale(im, **(self.hogParams))
        r = None
        if len(result)>0 and len(result[0])>0:
            r = result[0][0]
            print("Result: " + str(r))
        return r

class WorkerThread(threading.Thread):
    def __init__(self, i, lock):
        threading.Thread.__init__(self)
        self.i = i
        self.lock = lock
        self.running = True
        self.h = PeopleDetector()
        self.hog = None
        self.image = None
        self.upside_down = False
        for j in UPSIDE_DOWN_LIST.split(","):
            if j == str(self.i):
                self.upside_down = True

    def stop(self):
        self.running = False

    def getHog(self):
        return self.hog

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
            self.lock.acquire()
            image = url_to_image(URL+ CAMERA_LIST[i] +":800" + CAMERA_LIST[i] +"/img.png")
            self.image = image
            self.lock.release()

            # Run the hog algorithm to find the location of the human being.
            if image is not None:
                self.lock.acquire()
                hog = self.h.get(image)
                self.hog = hog
                self.lock.release()

def dist(p1, p2):
    return math.sqrt( (p2[1] - p1[1])**2 + (p2[0] - p1[0])**2 )

def getPhysicalPosition(hog_results_list):
            mind = float('inf')
            min_hog = None
            for i,cam in enumerate(CAMERA_LIST):
                r = hog_results_list[i]
                dists = []
                if r is None: # If hog result is None we can skip.
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
                #sys.stdout.write("\rPosition: " + str(min_hog.phys_pos))
                #sys.stdout.flush()
                pass

if __name__ == '__main__':


    # Load waypoints from file.
    waypoints = pickle.load(open(CAL_SAVE_PATH, "rb"))

    thread_list = [None]*len(CAMERA_LIST)

    try:
        lock = threading.Lock()
        for i,cam in enumerate(CAMERA_LIST):
            thread_list[i] = WorkerThread(i, lock)
            thread_list[i].start()
            print str(i) + ": WorkerThread started for camera " + cam

        while True:
            loop_results = [None]*len(CAMERA_LIST)

            for i,cam in enumerate(CAMERA_LIST):
                image = (thread_list[i].getImage())
                hog = thread_list[i].getHog()
                loop_results[i] = hog
                if image is not None:
                    if hog is not None:
                        r = hog
                        im = np.copy(image)
                        cv2.rectangle(im, (r[0],r[1]), (r[0]+r[2],r[1]+r[3]), (0,255,0), 5)
                        cv2.imshow("people detector " + cam, im)
                    else:
                        cv2.imshow("people detector " + cam, image)
                    cv2.waitKey(1)
            # Now we have a loop_result list that contains tuples of image
            # and human position.
            # What is left to do is to find the closest waypoint that
            # matches them.
            getPhysicalPosition(loop_results)

    except KeyboardInterrupt:
        # If keyboard interrupt has occurred, we need to terminate the
        # threads one by one.
        cv2.destroyAllWindows()
        print ""
        for i,cam in enumerate(CAMERA_LIST):
            print str(i) + ": Terminating WorkerThread for camera " + cam
            thread_list[i].stop()
        print "Exiting."
        sys.exit(0)
