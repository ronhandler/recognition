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
        self.first = None
        pass

    def get(self, im):
        # Init the first image.
        if self.first == None:
            self.first = im
            return None

        max_diff = 0
        diff_x = None
        diff_y = None
        for x in range(0, WIDTH, 5):
            for y in range(0, HEIGHT, 5):
                cropped_im    = self.im[y:y+5, x:x+5]
                cropped_first = self.first[y:y+5, x:x+5]
                current_diff = abs(cropped_first - cropped_im)
                if max_diff < current_diff:
                    current_diff = max_diff
                    diff_x = x
                    diff_y = y

        if (diff_x != None):
            return (x,y)
        else:
            return None
