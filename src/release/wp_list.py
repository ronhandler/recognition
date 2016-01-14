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

def wp_to_dp(wp_list):
    if wp_list is None:
        return None
    dest_points = []
    waypoints = pickle.load(open(CAL_SAVE_PATH, "rb"))
    for num in wp_list:
        for w in waypoints:
            for cam in w:
                if int(num) == w[cam].wp_id:
                    dest_points.append(w[cam])
                    break
    return dest_points
