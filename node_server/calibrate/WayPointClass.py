#! /usr/bin/python

def WayPoint(object):
    def __init__(self, i, x, y):
        self.cam_id = i
        self.cam_pos = (x,y)
        self.phys_pos = None
    
    def set_phys_position(self, p_x, p_y):
        self.phys_pos = (p_x, p_y)
