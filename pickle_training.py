#! /usr/bin/python

import pickle
import random
import numpy as np
import cv2
from PIL import Image
import os, os.path

class Hog_D(object):
    def __init__(self):
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.hogParams = {'winStride': (4, 4), 'padding': (32, 32), 'scale': 1.05}
        self.black_list = []
    
    def build_black_list(self, im):
        result = self.hog.detectMultiScale(im, **(self.hogParams))
        if all(result) and len(result) == 2:
            print len(result), result
            if result[0][0] not in self.black_list:
                self.black_list.append(result)
        if all(result) and len(result) > 3:
            print len(result), result
            for i in range(0, len(result)):
                res = (result[i][i])
                if res not in self.black_list:
                    self.black_list.append(res)
        if len(result) == 0:
            return


DIR = './release/server/svm_try/Neg'
images = []
for i in range(0,len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]    )):
    png = Image.open("./release/server/svm_try/Neg/neg"+str(i)+".png")
    images.append(np.array(png))
     #cv2.imshow("test", images[i])
      #cv2.waitKey(0)
      #cv2.destroyAllWindows()

h = Hog_D()
print "finished loading images"
for im in images:
    for i in range(0, 3):
        h.build_black_list(im)
print h.black_list

with open("pickle_test.txt", "wb") as f:
    pickle.dump(h.black_list, f, 0)

loaded_list = pickle.load(open("pickle_test.txt", "rb"))

#for im in loaded_list:
    #cv2.imshow("test", im)
    #cv2.waitKey(100)
    #cv2.destroyAllWindows()
