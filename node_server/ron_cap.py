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

DEBUG_LEVEL = 0

def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urllib.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

#def my_sig(signum, frame):
    #print "### Received a signal"


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
        self.l.acquire()
        r = self.hog
        self.l.release()
        return r

    def getImage(self):
        img = None
        self.l.acquire()
        img = self.image
        self.l.release()
        return img

    def run(self):
        i = self.i

        while self.running == True:
            image = url_to_image("http://192.168.1.20"+ str(i) +":800" + str(i) +"/img.png")

            self.l.acquire()
            self.image = image
            self.l.release()

            # Print a message saying we received the image.
            if DEBUG_LEVEL >= 1:
                sys.stdout.write("Received image " + str(i) + " ")
                for j in range(0,i):
                    sys.stdout.write(".")
                sys.stdout.write("x")
                for j in range(i,7):
                    sys.stdout.write(".")
                sys.stdout.write("\n")

            # Run the hog algorithm to find the location of the human being.
            if image is not None:
                #print "Image is not none", self.i
                hog = self.h.hog_f(image)
                self.l.acquire()
                self.hog = hog
                self.l.release()
                


if __name__ == '__main__':
    process_list = []

    try:
        lock = Lock()
        for i in range(0,8):
            print i
            my_thread = capture(i, lock)
            my_thread.start()
            process_list.append(my_thread)
        while True:
            for i in range(0,8):
                #image = None
                #hog = None
                image = process_list[i].getImage()
                if image is not None:
                    hog = process_list[i].getHog()
                    lock.acquire()
                    if hog is not None:
                        r = hog
                        cv2.rectangle(image, (r[0],r[1]), (r[0]+r[2],r[1]+r[3]), (0,255,0), 5)
                        #print "Found", i
                    cv2.imshow("people detector "+str(i), image)
                    lock.release()
            pass
    except KeyboardInterrupt:
        for i in range(0,8):
            print "Terminating process "+str(i)
            cv2.destroyAllWindows()
            process_list[i].stop()
            #process_list[i].terminate()
        print "Exiting."
        sys.exit(1)
