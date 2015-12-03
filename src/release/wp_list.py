#! /usr/bin/python

import os
import sys
import pickle
import ConfigParser

# Change dir the script's location.
sys.path.append("../calibrate")

config = ConfigParser.RawConfigParser()
config.read('../config.txt')
CAL_SAVE_PATH = config.get("calibrate_paths", "cal_save")

def wp_to_dp():
    dest_points = []
    waypoints = pickle.load(open(CAL_SAVE_PATH, "rb"))

    for w in waypoints:
        for i in w:
            dest_points.append(w[i])
            break
    return dest_points
