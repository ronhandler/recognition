#! /usr/bin/python

import cv2
import urllib 
import numpy as np

def decode_stream(stream1, bytes1, num):
    
    bytes1+=stream1.read(1024)
    a1 = bytes1.find('\xff\xd8')
    b1 = bytes1.find('\xff\xd9')
    if a1!=-1 and b1!=-1:
        jpg1 = bytes1[a1:b1+2]
        bytes1= bytes1[b1+2:]
        img = cv2.imdecode(np.fromstring(jpg1, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
        cv2.imwrite("trying"+str(num)+".jpg", img)
        cv2.imshow(str(num), img)
    return bytes1

def take_streams(stream_url):
    streams=[]
    bytes_x = []
    for j in range (0, len(stream_url)):
        streams.append(urllib.urlopen(stream_url[j]))
        bytes_x.append('')
    while True:
        for i in range (0, len(streams)):
            bytes_x[i] =  decode_stream(streams[i], bytes_x[i], i)
        if cv2.waitKey(1) == 27:
            exit(0)
 

take_streams(['http://192.168.1.58:5000/video_feed','http://192.168.1.60:5000/video_feed'])
