#! /usr/bin/python

import sys
import cv2
from multiprocessing import Process, Lock
import urllib
import numpy as np
from hog_try import Hog_D


def take_streams(lock, stream_url):
    h = Hog_D() 
    stream = urllib.urlopen(stream_url)
    bytes = ''
    while True:
        bytes+=stream.read(1024)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if a!=-1 and b!=-1:
            jpg = bytes[a:b+2]
            bytes= bytes[b+2:]
            img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
            #cv2.imwrite("trying"+str(num)+".jpg", img)
            if img is not None:
                #r = h.hog_f(img)
                #if r is not None:
                    #cv2.rectangle(img, (r[0],r[1]), (r[0]+r[2],r[1]+r[3]), (0,255,0), 5)
                cv2.imshow(stream_url, img)
        if cv2.waitKey(1) == 27:
            exit(0)
 

if __name__ == '__main__':
    process_list = []
    try:
        lock = Lock()
        for i in range(0,8):
            print i
            p = Process(target=take_streams, args=(lock,"http://192.168.1.20"+str(i)+":5000/video_feed"))
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
