#! /usr/bin/python
import socket
import sys
import cv2
import numpy
import struct
#from hog_try import Hog_D

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


HOST='192.168.1.103'
PORT=11113
bytes_per_read = 2470990

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print 'Socket created'

s.bind((HOST,PORT))
print 'Socket bind complete'
s.listen(1)
print 'Socket now listening'

conn,addr=s.accept()
print "connected", addr
#h = Hog_D()
data = ""
payload_size = struct.calcsize("L") 
while True:   
    while len(data) < payload_size:
        data += conn.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    ###

    frame=pickle.loads(frame_data)
    print frame
    cv2.imshow('frame',frame)

s.close()
cv2.destroyAllWindows()
