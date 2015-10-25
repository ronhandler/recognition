#! /usr/bin/python

import cv2
import numpy as np
import xml.etree.ElementTree as ET

from PIL import Image
import os, os.path

class StatModel(object):
    '''parent class - starting point to add abstraction'''    
    def load(self, fn):
        self.model.load(fn)
    def save(self, fn):
        self.model.save(fn)

class SVM(StatModel):
    '''wrapper for OpenCV SimpleVectorMachine algorithm'''
    def __init__(self):
        self.model = cv2.SVM()

    def train(self, samples, responses):
        #setting algorithm parameters
        params = dict( kernel_type = cv2.SVM_LINEAR, 
                       svm_type = cv2.SVM_C_SVC,
                       C = 1 )
        self.model.train(samples, responses, params = params)

    def predict(self, samples):
        return np.float32( [self.model.predict(s) for s in samples])


rDIR = './Neg'
dDIR = './Pos' 
descs = [None]*len([name for name in os.listdir(dDIR) if os.path.isfile(os.path.join(dDIR, name))])
resps = [None]*len([name for name in os.listdir(rDIR) if os.path.isfile(os.path.join(rDIR, name))])
for i in range(0,len([name for name in os.listdir(dDIR) if os.path.isfile(os.path.join(dDIR, name))])):
    png = Image.open("./Pos/pos"+str(i)+".png")
    descs[i] = np.array(png, dtype = np.float32)
    print type(descs)

for f in os.listdir(rDIR): 
    fullpath = os.path.join(rDIR, f)
    if os.path.isfile(fullpath):   
        png = Image.open(fullpath)
        resps.append(np.array(png, dtype = np.float32))

svm = SVM()
svm.train(descs, resps)

svm.save("svm.xml")
tree = ET.parse('svm.xml')
root = tree.getroot()
# now this is really dirty, but after ~3h of fighting OpenCV its what happens :-)
SVs = root.getchildren()[0].getchildren()[-2].getchildren()[0] 
rho = float( root.getchildren()[0].getchildren()[-1].getchildren()[0].getchildren()[1].text )
svmvec = [float(x) for x in re.sub( '\s+', ' ', SVs.text ).strip().split(' ')]
svmvec.append(-rho)
pickle.dump(svmvec, open("svm.pickle", 'w'))
