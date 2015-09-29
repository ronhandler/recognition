#! /usr/bin/python

import sys
import cv2
from multiprocessing import Process, Lock
import urllib
import numpy as np
from hog_try import Hog_D
import time
import datetime
import signal
import threading

DEBUG_LEVEL = 1

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

    def __init__(self, i, images, hogs):
        threading.Thread.__init__(self)
        self.i = i
        self.h = Hog_D()
        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        i = self.i
        h = self.h

        while self.running == True:
            #l.acquire()
            image = url_to_image("http://192.168.1.20"+ str(i) +":800" + str(i) +"/img.png")
            #l.release()

            images[i] = image


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
                hogs[i] = h.hog_f(image)
                
            if cv2.waitKey(1) == 27:
                break

        cv2.destroyAllWindows()

if __name__ == '__main__':
    process_list = []
    images = [None]*8
    hogs = [None]*8

    try:
        lock = Lock()
        for i in range(0,8):
            print i
            my_thread = capture(i, images, hogs)
            my_thread.start()
            process_list.append(my_thread)
            #p = Process(target=capture, args=(lock, i))
            #p.start()
            #process_list.append(p)
        while True:
            for i in range(0,8):
                if images[i] is not None:
                    if hogs[i] is not None:
                        r = hogs[i]
                        cv2.rectangle(images[i], (r[0],r[1]), (r[0]+r[2],r[1]+r[3]), (0,255,0), 5)
                    cv2.imshow("people detector "+str(i), images[i])
            pass
    except KeyboardInterrupt:
        for i in range(0,8):
            print "Terminating process "+str(i)
            process_list[i].stop()
            #process_list[i].terminate()
        print "Exiting."
        sys.exit(1)
