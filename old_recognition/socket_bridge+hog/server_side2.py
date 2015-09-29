import socket
import sys
import cv2
import numpy
from hog_try import Hog_D

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


HOST='192.168.1.102'
PORT=8000
bytes_per_read = 2470990

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print 'Socket created'

s.bind((HOST,PORT))
print 'Socket bind complete'
s.listen(1)
print 'Socket now listening'

conn,addr=s.accept()
print "connected", addr
h = Hog_D()
while True:   
    length = recvall(conn,16)
    stringData = recvall(conn, int(length))
    data = numpy.fromstring(stringData, dtype='uint8')
    decimg=cv2.imdecode(data,1)
    h.hog_f(decimg)
    #cv2.imshow('SERVER',decimg)
    k = cv2.waitKey(1)
    if k == 27:
        break
s.close()
cv2.destroyAllWindows()
