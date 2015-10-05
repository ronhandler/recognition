#! /usr/bin/python

import sys
import cv2
import urllib
import numpy as np
from hog_try import Hog_D
import time
import datetime
import signal
import threading
from threading import Lock
import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('../config.txt')

DEBUG_LEVEL = config.getint("general", "debug_level")
MAX_CAM_NUMBER = config.getint("general", "max_cam_number")
URL = config.get("general", "url")

def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    try:
        resp = urllib.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
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

    def stop(self):
        self.running = False

    def getHog(self):
        r = None
        r = self.hog
        return r

    def getImage(self):
        img = None
        img = self.image
        return img

    def run(self):
        i = self.i

        while self.running == True:
            image = url_to_image(URL+ str(i) +":800" + str(i) +"/img.png")

            self.l.acquire()
            self.image = image
            self.l.release()

            # Run the hog algorithm to find the location of the human being.
            if image is not None:
                hog = self.h.hog_f(image)
                self.l.acquire()
                self.hog = hog
                self.l.release()

if __name__ == '__main__':
    process_list = []

    try:
        lock = Lock()
        for i in range(0, MAX_CAM_NUMBER):
            print i
            my_thread = capture(i, lock)
            my_thread.start()
            process_list.append(my_thread)
        while True:
            loop_results = []
            for i in range(0, MAX_CAM_NUMBER):
                image = process_list[i].getImage()
                hog = process_list[i].getHog()
                loop_results.append((image, hog))
                if image is not None:
                    if hog is not None:
                        r = hog
                        cv2.rectangle(image, (r[0],r[1]), (r[0]+r[2],r[1]+r[3]), (0,255,0), 5)
                    cv2.imshow("people detector "+str(i), image)
                    cv2.waitKey(1)
    except KeyboardInterrupt:
        for i in range(0, MAX_CAM_NUMBER):
            print "Terminating process "+str(i)
            cv2.destroyAllWindows()
            process_list[i].stop()
        print "Exiting."
        sys.exit(1)
