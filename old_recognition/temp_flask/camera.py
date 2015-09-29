from time import time
import cv2

class Camera(object):

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3,320)
        self.cap.set(4,240)

    def __del__(self):
        self.cap.release()

    def get_frame(self):
        success, image = self.cap.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tostring()
