#! /usr/bin/python

from threading import *
import os
#set up working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.append("./calibrate")
import pickle
from WayPointClass import WayPoint
import ConfigParser
import socket

config = ConfigParser.RawConfigParser()
config.read('./config.txt')
CAL_SAVE_PATH = config.get("calibrate_paths","cal_save_up")

Dest_string = "Destination is:"
Loc_string = "Current location is:"

class route(object):
    def __init__(self):
        self.name = None
        waypoints_list = []

    def get_next_wp(current_wp):
        for i in waypoint_list:
            if current_wp == waypoint_list[-1]: #get the last element
                print "Destination point"
                return current_wp 
            if current_wp == waypoint_list[i]:
                return waypoint_list[i+1]

class server(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()

    def run(self):
        while 1:
            data = self.sock.recv(1024).decode()
            print data
            #d = data.find(Dest_string)
            #l = data.find(Loc_string)
            #if (d is not -1):  #found destination substring
            #    print "Got destination"
            #    na = data[(len(Dest_string)):] #slising to name of destination only
            #    print str(na) #Ensuring got the right name.
                #got name for destination, TODO 
            #if (l is not -1):
            #    position = data[(len(Loc_string)):]
            #    next_p = get_next_wp(position)
            #    send_location(ST, PORT, next_p) #TODO not forget port and host
                #got position TODO
            #if not data:
            #    self.stop()
            #    break

            #self.sock.send(b'Oi you sent something to me')
            continue



def receive_data():
    ST = ''
    PORT = 8888 
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((ST, PORT))
    except socket.error as msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
        
    s.listen(1)
    print 'Listening on port ' + str(PORT)
     
    while True:
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
        server(conn, addr)
    print "Connection is closing"
    s.close()

def send_location(HOST, PORT, pos):
    #function to send location string over the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print "\n Sending locations"
    data = (str(pos.phys_pos[0])+","+ str(pos.phys_pos[1]) +" "+ str(pos.floor))
    s.send(data.encode())
    s.close()
    

#Main function:
if __name__ == "__main__":
    waypoints = pickle.load(open(CAL_SAVE_PATH, "rb"))
    for w in waypoints:
        for i in w:
            continue
            #TODO
    r = route()
    receive_data()
    

