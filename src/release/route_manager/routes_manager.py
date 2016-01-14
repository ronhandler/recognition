#! /usr/bin/python
import threading
import os
import sys
import ConfigParser
import socket

# set up working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("../calibrate")

from wp_list import wp_to_dp

config = ConfigParser.RawConfigParser()
config.read('../config.txt')
CAL_SAVE_PATH = config.get("calibrate_paths", "cal_save")

Dest_string = "Destination is:"
Loc_string = "Current location is:"

class Route(object):
    def __init__(self):
        self.name = None
        self.waypoints_list = []

    def get_next_wp(self, current_wp):
        for i in range(0, len(self.waypoints_list)):
            if self.waypoints_list[i].equal(int(current_wp[2]), int(current_wp[0]), int(current_wp[1])):
                if i == len(self.waypoints_list) - 1:
                    return None
                else:
                    return self.waypoints_list[i + 1]
        return None


class Server(threading.Thread):
    def __init__(self, socket, address, r):
        super(Server, self).__init__()
        self._stop = threading.Event()
        self.sock = socket
        self.addr = address
        self.route = r
        self.start()

    def stop(self):
        self._stop.set()

    def run(self):
        while 1:
            data = self.sock.recv(1024).decode()
            print data
            d = data.find(Dest_string)
            l = data.find(Loc_string)
            if d is not -1:  # found destination substring
                print "Got destination"
                na = data[(len(Dest_string))+1:]  # slising to name of destination only
                print str(na)  # Ensuring got the right name.
                self.route.name = na
                wplist = None
                try:
                    wplist = config.get("routes", self.route.name).split(",")
                except:
                    pass
                self.route.waypoints_list = wp_to_dp(wplist)
            # got name for destination, TODO
            if l is not -1:
                print "Got position\n"
                position = data[(len(Loc_string)):]
                pos_array = position.split(",")
                next_p = self.route.get_next_wp(pos_array)
                # print next_p
                send_location('', 11112, position ,next_p)  # TODO not forget port and host
            # got position TODO
            if not data:
                print "Connection lost"
                self.stop()
                break
                # self.sock.send(b'Oi you sent something to me')

def listener(route):
    st = ''
    port = 8888

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((st, port))
    except socket.error as msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    s.listen(1)
    print 'Listening on port ' + str(port)

    while True:
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
        Server(conn, addr, route)
    print "Connection is closing"
    s.close()


def send_location(host, port, c_pos, pos):
    # function to send location string over the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print "\n Sending locations"
    if pos:
        data = (str(pos.phys_pos[0]) + "," + str(pos.phys_pos[1]) + " " + str(pos.floor))
    else:
        data = "Waypoint out of the route"
    s.send(data.encode())
    s.close()


# Main function:
if __name__ == "__main__":
    r = Route()
    listener(r)
