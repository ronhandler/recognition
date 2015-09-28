#! /usr/bin/python

import sys
import cv2
from multiprocessing import Process, Lock
import urllib
import numpy as np
from hog_try import Hog_D
import time
import datetime

def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urllib.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

def capture(l,i):
    h = Hog_D()
    while True:
        #l.acquire()
        image = url_to_image("http://192.168.1.20"+ str(i) +":800" + str(i) +"/img.png")
        #l.release()


        # Print a message saying we received the image.
        sys.stdout.write("Received image " + str(i) + " ")
        for j in range(0,i):
            sys.stdout.write(".")
        sys.stdout.write("x")
        for j in range(i,7):
            sys.stdout.write(".")
        sys.stdout.write("\n")

        a = datetime.datetime.now()
        b = datetime.datetime.now()
        c = b - a
        print "Time took " + str(c.microseconds/1000000.0)
        # Run the hog algorithm to find the location of the human being.
        if image is not None:
            r = h.hog_f(image)
            if r is not None:
                cv2.rectangle(image, (r[0],r[1]), (r[0]+r[2],r[1]+r[3]), (0,255,0), 5)
            cv2.imshow("people detector "+str(i), image)
        if cv2.waitKey(1) == 27:
            break
    cv2.destroyAllWindows()

if __name__ == '__main__':
    process_list = []
    try:
        lock = Lock()
        for i in range(0,8):
            print i
            p = Process(target=capture, args=(lock, i))
            p.start()
            process_list.append(p)
        while True:
            pass
    except KeyboardInterrupt:
        for i in range(0,8):
            print "Terminating process "+str(i)
            process_list[i].terminate()
        print "Exiting."
        sys.exit(1)
