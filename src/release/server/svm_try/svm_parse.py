#! /usr/bin/python
import xml.etree.ElementTree as ET

tree = ET.parse('SVM.xml')
root = tree.getroot()
# now this is really dirty, but after ~3h of fighting OpenCV its what happens :-)
SVs = root.getchildren()[0].getchildren()[-2].getchildren()[0] 
rho = float( root.getchildren()[0].getchildren()[-1].getchildren()[0].getchildren()[1].text )
svmvec = [float(x) for x in re.sub( '\s+', ' ', SVs.text ).strip().split(' ')]
svmvec.append(-rho)
pickle.dump(svmvec, open("svm.pickle", 'w'))
