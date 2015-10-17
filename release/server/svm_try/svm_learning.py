#! /usr/bin/python

import cv2
import numpy as np
import xml.etree.ElementTree as ET

descs = None
resps = None

svm = cv2.SVM()
svm.train_auto(descs, resps, None, None, params=cv2.svm_params, k_fold=5)

svm.save("svm.xml")
tree = ET.parse('svm.xml')
root = tree.getroot()
# now this is really dirty, but after ~3h of fighting OpenCV its what happens :-)
SVs = root.getchildren()[0].getchildren()[-2].getchildren()[0] 
rho = float( root.getchildren()[0].getchildren()[-1].getchildren()[0].getchildren()[1].text )
svmvec = [float(x) for x in re.sub( '\s+', ' ', SVs.text ).strip().split(' ')]
svmvec.append(-rho)
pickle.dump(svmvec, open("svm.pickle", 'w'))
