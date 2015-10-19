#! /usr/bin/python

import cv2
import numpy as np
import xml.etree.ElementTree as ET

from PIL import Image
import os, os.path

DIR = './Neg' 
images = []
for i in range(0,len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])):
    png = Image.open("./Neg/neg"+str(i)+".png")
    images.append(np.array(png))


svm_params = dict( kernel_type = cv2.SVM_LINEAR, 
                       svm_type = cv2.SVM_C_SVC,
                       C = 1 )

descs = np.copy(images)
resps = np.copy(images)

svm = cv2.SVM()
svm.train_auto(descs, resps, None, None, params=svm_params, k_fold=5)

svm.save("svm.xml")
tree = ET.parse('svm.xml')
root = tree.getroot()
# now this is really dirty, but after ~3h of fighting OpenCV its what happens :-)
SVs = root.getchildren()[0].getchildren()[-2].getchildren()[0] 
rho = float( root.getchildren()[0].getchildren()[-1].getchildren()[0].getchildren()[1].text )
svmvec = [float(x) for x in re.sub( '\s+', ' ', SVs.text ).strip().split(' ')]
svmvec.append(-rho)
pickle.dump(svmvec, open("svm.pickle", 'w'))
