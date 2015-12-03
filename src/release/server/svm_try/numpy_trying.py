#! /usr/bin/python

import numpy as np
import cv2
from PIL import Image
import os, os.path

DIR = './Neg'
images = []
for i in range(0,len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])):
    png = Image.open("./Neg/neg"+str(i)+".png")
    images.append(np.array(png))
    #cv2.imshow("test", images[i])
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
print len(images)
