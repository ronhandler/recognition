#! /usr/bin/python
import os
import sys
import time
import datetime
import math
import cv2
import urllib
import numpy as np
import threading
import pickle
import ConfigParser
import socket

# Change dir the script's location.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("../calibrate")
sys.path.append("../")

from wp_list import wp_to_dp  # function to convert waypoints list

config = ConfigParser.RawConfigParser()
config.read('../config.txt')

DEBUG_LEVEL = config.getint("general", "debug_level")
URL = config.get("general", "url")
CAL_SAVE_PATH = config.get("calibrate_paths", "cal_save")
UPSIDE_DOWN_LIST = config.get("general", "upside_down_list")
CAMERA_LIST = config.get("odroid", "camera_list").split(",")
SECONDS = int(config.get("general", "seconds"))
POSITION_LOG_PATH = config.get("capture_paths", "position_log")
SOCKET_HOST = config.get("socket", "host")
SOCKET_PORT = int(config.get("socket", "port"))
FLOORMAP_PATH = config.get("capture_paths", "floormap")

# Load waypoints from file.
waypoints = pickle.load(open(CAL_SAVE_PATH, "rb"))
floormaps = {}
dest_points = wp_to_dp()  # for demo navigation

for w in waypoints:
    for i in w.keys():
        if w[i].floor not in floormaps.keys():
            floormaps[w[i].floor] = cv2.imread(FLOORMAP_PATH + str(w[i].floor) + ".png")


def send_location(host, port, wp):
    current_pos = "Current point is: " + str(wp.phys_pos[0]) + ", " + str(wp.phys_pos[1]) + ", " + str(wp.floor)
    next_pos = "WayPoint out of the route"
    for i in range(0,len(dest_points)):
        if dest_points[i].wp_id == wp.wp_id:
            if dest_points[i] == dest_points[-1]:  # if it's last one?
                next_pos = "Destination point"
            else:
                next_pos = "Next waypoint is: " + str(dest_points[i + 1].phys_pos[0]) + ", " + str(
                    dest_points[i + 1].phys_pos[1]) + ", " + str(dest_points[i + 1].floor)  # next waypoint in the route
    # function to send location string over the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print "\n Sending locations"
    data = current_pos +"\n" + next_pos
    s.send(data.encode())
    s.close()


def url_to_image(url):
    # Download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    try:
        resp = urllib.urlopen(url)
        img = np.asarray(bytearray(resp.read()), dtype="uint8")
        return cv2.imdecode(img, cv2.IMREAD_COLOR)
    except:
        return None


class PeopleDetector(object):
    def __init__(self):
        self.hog = cv2.HOGDescriptor()
        self.svm = cv2.SVM()
        self.hog.setSVMDetector(np.array(self.svm.load('SVM.xml')))
        self.hogParams = {'winStride': (4, 4), 'padding': (32, 32), 'scale': 1.05}

    def get(self, img):
        result = self.hog.detectMultiScale(img, **self.hogParams)
        r = None
        if len(result) > 0 and len(result[0]) > 0:
            r = result[0]
            # print("Results: " + str(r))
        return r


class WorkerThread(threading.Thread):
    def __init__(self, i, lock):
        threading.Thread.__init__(self)
        self.i = i
        self.lock = lock
        self.running = True
        self.h = PeopleDetector()
        self.hog = None
        self.image = None
        self.upside_down = False
        for j in UPSIDE_DOWN_LIST.split(","):
            if j == str(CAMERA_LIST[self.i]):
                self.upside_down = True
        # Blacklist is a list of known points that we want to ignore. This
        # is useful when we will later populate this list with points found
        # in the first few seconds when no people were present on screen.
        self.blacklist = []
        self.radius = 50

    def stop(self):
        self.running = False

    def getHog(self):
        return self.hog

    def getImage(self):
        img = self.image
        # Rotate image if it was recorded upside down.
        if self.upside_down:
            img = cv2.flip(img, 0)
            img = cv2.flip(img, 1)
        return img

    # Populate the blacklist with points we want to ignore.
    def populate_blacklist(self):
        seconds = SECONDS
        timeout = time.time() + seconds
        # Loop for a few seconds, and populate the blacklist.
        while time.time() < timeout and self.running is True:
            img = url_to_image(URL + CAMERA_LIST[self.i] + ":800" + CAMERA_LIST[self.i] + "/img.png")
            if img is not None:
                hog_list = self.h.get(img)
                if hog_list is not None:
                    for result in hog_list:
                        # If result is not in the blacklist:
                        if not np.any(self.blacklist == result[:2]):
                            pnt = [int(result[0] + (result[2]) / 2), int((result[1] + result[3]))]
                            # print("Adding to blacklist" + str(self.i) + ": " + str(point))
                            self.blacklist.append(pnt)

            if timeout - time.time() < seconds and self.i == 0:
                if seconds == 0:
                    print("Learning complete.")
                else:
                    print("Learning. " + str(seconds) + " seconds remaining . . .")
                seconds -= 5

    def run(self):

        # Learn a few seconds and populate the blacklist.
        self.populate_blacklist()

        # print(str(self.i) + " blacklist: " + str(self.blacklist))

        while self.running:
            self.lock.acquire()
            img = url_to_image(URL + CAMERA_LIST[self.i] + ":800" + CAMERA_LIST[self.i] + "/img.png")
            self.image = img
            self.lock.release()

            # Run the hog algorithm to find the location of the human being.
            found_flag = False
            if img is not None:
                # Try to find a person position that is not in blacklist.
                hog_list = self.h.get(img)
                if hog_list is not None:
                    for result in hog_list:
                        # If result is not in the blacklist:
                        near_radius_flag = False
                        for blpoint in self.blacklist:
                            pnt = [int(result[0] + (result[2]) / 2), int((result[1] + result[3]))]
                            if dist(pnt, blpoint) < self.radius:
                                near_radius_flag = True
                        # This means that none of the results are near a
                        # point in blacklist by self.radius distance.
                        if not near_radius_flag:
                            self.lock.acquire()
                            self.hog = result
                            self.lock.release()
                            found_flag = True
                            break
                            # else:
                            # print("Found a match near blacklist.")

            if not found_flag:
                self.lock.acquire()
                self.hog = None
                self.lock.release()


def dist(p1, p2):
    return math.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)


def getPhysicalPosition(hog_results_list):
    min_dist = float('inf')
    min_hog = None
    for i, cam in enumerate(CAMERA_LIST):
        r = hog_results_list[i]
        dists = []
        if r is None:  # If hog result is None we can skip.
            continue
        for w in waypoints:
            if i not in w.keys():
                continue
            # The hog result from camera i.
            p1 = (r[0], r[1])
            # The hog result from each waypoint.
            p2 = (w[i].cam_pos[0], w[i].cam_pos[1])
            d = dist(p1, p2)
            if d is not None:
                dists.append((w[i], d))

                # for w in waypoints:
                # for k,v in w.items():
                # p1 = (r[0], r[1]) # The hog result from camera i.
                # p2 = (v.cam_pos[0], v.cam_pos[1])
                # d = dist(p1, p2)
                # if d != None:
                # dists.append((v, d))
                ##print("Distance is: " + str(d))
        for j in range(0, len(dists)):
            if min_dist > dists[j][1]:
                min_dist = dists[j][1]
                min_hog = dists[j][0]
    if min_hog is not None:
        sys.stdout.write("\rFloor: " + str(min_hog.floor) + ", Position: " + str(min_hog.phys_pos))
        sys.stdout.flush()

    return min_hog


if __name__ == "__main__":

    thread_list = [None] * len(CAMERA_LIST)

    old_locations = {}
    try:
        # Create threads
        lock = threading.Lock()
        for i, cam in enumerate(CAMERA_LIST):
            thread_list[i] = WorkerThread(i, lock)
            thread_list[i].start()
            print(str(i) + ": WorkerThread started for camera " + cam)

        while True:
            loop_results = [None] * len(CAMERA_LIST)

            # Create a window for the floormaps.
            for i in floormaps.keys():
                cv2.imshow("floor map " + str(i), floormaps[i])

            for i, cam in enumerate(CAMERA_LIST):
                loop_results[i] = None
                image = (thread_list[i].getImage())
                hog = thread_list[i].getHog()
                if image is not None:
                    im = np.copy(image)
                    for x, y in thread_list[i].blacklist:
                        cv2.circle(im, (x, y), thread_list[i].radius, (255, 0, 0), 2)
                    if hog is not None:
                        loop_results[i] = hog
                        point = [int(hog[0] + (hog[2]) / 2), int((hog[1] + hog[3]))]
                        cv2.circle(im, (point[0], point[1]), 10, (0, 0, 255), 3)
                        cv2.rectangle(im, (hog[0], hog[1]), (hog[0] + hog[2], hog[1] + hog[3]), (0, 255, 0), 5)
                    cv2.imshow("people detector " + cam, im)
                    cv2.waitKey(1)

            # Now we have a loop_result list that contains tuples of image
            # and human position.
            # What is left to do is to find the closest waypoint that
            # matches them.
            pos = getPhysicalPosition(loop_results)
            # Write to log.
            if pos is not None:
                floor = pos.floor
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                if floor in old_locations.keys() and (pos != old_locations[floor] or old_locations[floor] is None) :
                    # send location to listener
                    send_location(SOCKET_HOST, SOCKET_PORT, pos)
                    # Write to log.
                    with open(POSITION_LOG_PATH, "a") as f:
                        f.write(st + ": " + str(pos.phys_pos) + " " + str(pos.floor) + "\n")
                    # Update the floormap with the newly found wp.
                    if floor in old_locations.keys() and old_locations[floor] is not None:
                        p1 = (old_locations[floor].phys_pos[0] * 10, old_locations[floor].phys_pos[1] * 10)
                        p2 = (pos.phys_pos[0] * 10, pos.phys_pos[1] * 10)
                        cv2.line(floormaps[floor], p1, p2, (255, 0, 0), 2)

                old_locations[floor] = pos

    except KeyboardInterrupt:
        # If keyboard interrupt has occurred, we need to terminate the
        # threads one by one.
        cv2.destroyAllWindows()
        print("")
        for i, cam in enumerate(CAMERA_LIST):
            print(str(i) + ": Terminating WorkerThread for camera " + cam)
            thread_list[i].stop()
        print("Exiting.")
        sys.exit(0)
