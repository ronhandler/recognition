#! /usr/bin/python

import os
import sys
import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('../config.txt')
import cv2
import numpy as np

WIDTH = config.getint("general", "width")
HEIGHT = config.getint("general", "height")
THRESHOLD = 600.0

class Diff(object):
    def __init__(self):
        self.first = None
        pass

    def get(self, im):
        # Init the first image.
        if self.first == None:
            self.first = im
            return None

        max_diff = THRESHOLD
        diff_x = None
        diff_y = None
        for x in range(0, WIDTH, 5):
            for y in range(HEIGHT-1, -1, -5):
                cropped_im    = im[y:y+5, x:x+5]
                cropped_first = self.first[y:y+5, x:x+5]
                current_diff = cv2.sumElems(cv2.sumElems(cv2.absdiff(cropped_first, cropped_im)))[0]
                if max_diff < current_diff:
                    max_diff = current_diff
                    diff_x = x
                    diff_y = y

        #print("Diff: " + str(current_diff))
        if (diff_x != None):
            return (diff_x, diff_y)
        else:
            return None
