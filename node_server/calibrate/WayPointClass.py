#! /usr/bin/python

class WayPoint(object):
    def __init__(self, i, p_x, p_y):
        self.cam_id = i
        self.cam_pos = None
        self.phys_pos = (p_x,p_y)
    
    def set_cam_position(self, c_x, c_y):
        self.cam_pos = (c_x, c_y)
