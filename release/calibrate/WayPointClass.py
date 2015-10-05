#! /usr/bin/python

class WayPoint(object):
    def __init__(self):
        self.wp_id = -1
        self.cam_id = -1
        self.cam_pos = None
        self.phys_pos = None
    def __str__(self):
        s = ""
        s += "    cam_id:" + str(self.cam_id) + "\n" 
        s += "    cam_pos:" + str(self.cam_pos) + "\n"
        s += "    phys_pos:" + str(self.phys_pos)
        return s
