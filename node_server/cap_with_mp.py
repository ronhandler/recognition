#! /usr/bin/python

import cv2
from multiprocessing import Process, Lock
from hog_try import Hog_D

def capture(l,i):
    h = Hog_D()
    while True:
        l.acquire()
        cap = cv2.VideoCapture("http://192.168.1.20"+ str(i) +":800" + str(i) +"/img.png")
        l.release()
        #print "Capture on", i
        ret, image = cap.read()
        if image is not None:
            #r = h.hog_f(image)
            #if r is not None:
                #cv2.rectangle(image, (r[0],r[1]), (r[0]+r[2],r[1]+r[3]), (0,255,0), 5)
            #cv2.imshow("people detector "+str(i), image)
            print "Got image from caera", i
        if cv2.waitKey(1) == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    lock = Lock()
    for i in range(0,4):
        print i
        Process(target=capture, args=(lock, i)).start()
