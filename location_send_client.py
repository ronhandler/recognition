#! /usr/bin/python

import socket
import sys

HOST, PORT = "localhost", 11112

def enter_handler():
    while True:
        res = raw_input("Enter the message")
        try:
            ret = str(res)
            return ret
        except:
            print("Parameters need to be integers")
            continue


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))
while True:
    message = enter_handler()
    s.send(message.encode())
s.close()
