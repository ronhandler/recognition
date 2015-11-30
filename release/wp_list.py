#! /usr/bin/python

import os
# Change dir the script's location.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.append("./calibrate")
import pickle
from WayPointClass import WayPoint
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('./config.txt')
CAL_SAVE_PATH = config.get("calibrate_paths","cal_save_up")

dest_points = [{}]

waypoints = pickle.load(open(CAL_SAVE_PATH, "rb"))
for w in waypoints:
    for i in w.keys():
        dest_points.append(w[i])
        break
for d in dest_points:
        print d, "\n"
