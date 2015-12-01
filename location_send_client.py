#! /usr/bin/python

import socket
from src.release.wp_list import wp_to_dp

HOST, PORT = "localhost", 11112


def enter_handler():
    while True:
        res = raw_input("Enter the message:\n")
        try:
            ret = str(res)
            return ret
        except:
            print("Parameters need to be integers")
            continue


def getNextwp(wp_id):
    dp = wp_to_dp()
    msg = "Waypoint out of the route"
    for i in range(0, len(dp)):
        if dp[i].wp_id == int(wp_id):
            if dp[i] == dp[-1]:
                msg = "Destination point"
            else:
                msg = str(dp[i+1].phys_pos[0])+ ", " + str(dp[i+1].phys_pos[1])
    return msg

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))
while True:
    message = getNextwp(enter_handler())
    s.send(message.encode())
    #print(s.recv(1024).decode())
s.close()
