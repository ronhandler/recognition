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

class Diff(object):
    def __init__(self):
        self.flag = False
        self.first = None
        pass

    def get(self, im):
        # Init the first image.
        if self.flag == False:
            self.first = im
            self.flag = True
            return None

        max_diff = 1000.0
        diff_x = None
        diff_y = None
        for x in range(0, WIDTH, 5):
            for y in range(HEIGHT-1, -1, -5):
                cropped_im    = im[y:y+5, x:x+5]
                cropped_first = self.first[y:y+5, x:x+5]
                current_diff = cv2.mean(cv2.sumElems(cv2.absdiff(cropped_first, cropped_im)))[0]
                if max_diff < current_diff:
                    max_diff = current_diff
                    diff_x = WIDTH-x
                    diff_y = HEIGHT-y
        #print("Diff: " + str(current_diff))

        if (diff_x != None):
            return (diff_x, diff_y)
        else:
            return None
