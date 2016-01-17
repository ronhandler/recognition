#! /usr/bin/python

import socket

HOST, PORT = "localhost", 8888


def enter_handler():
    while True:
        res = raw_input("Enter the destination:\n")
        try:
            ret ="Destination is: " + str(res)
            return ret
        except:
            print("It must to be characters")
            continue

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))
while True:
    message = enter_handler()
    s.send(message.encode())
    # print(s.recv(1024).decode())
s.close()
