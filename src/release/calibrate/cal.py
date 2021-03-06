#!/usr/bin/env python
import os
import cv2
import pickle
import numpy as np
from WayPointClass import WayPoint
import ConfigParser

# Change dir the script's location.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

config = ConfigParser.RawConfigParser()
config.read('../config.txt')

WIDTH = config.getint("general", "width")
HEIGHT = config.getint("general", "height")
COLOR_DETECT_THRESHOLD = 0.2
URL = config.get("general", "url")
CAL_SAVE_PATH = config.get("calibrate_paths", "cal_save")
UPSIDE_DOWN_LIST = config.get("general", "upside_down_list")
HEADER = "camera "
CAMERA_LIST = config.get("odroid", "camera_list").split(",")
CAM_QUANTITY = len(CAMERA_LIST)
# CAM_QUANTITY = config.getint("general", "max_cam_number")

current_wp = 0
temp_images = [None] * CAM_QUANTITY
images = [None] * CAM_QUANTITY
coords = (None, None, None)
waypoints = [{}]


def mouse_handler(event, x, y, flags, cam_id):   # removed flags,event, x, y, flags, cam_id
    if event == cv2.EVENT_LBUTTONDOWN:
        images[cam_id] = np.copy(temp_images[cam_id])
        cv2.imshow(HEADER + CAMERA_LIST[cam_id], images[cam_id])
        cv2.circle(images[cam_id], (x, y), 25, (255, 0, 0), 3)
        wp = WayPoint()
        wp.wp_id = current_wp
        wp.cam_id = cam_id
        wp.cam_pos = (x, y)
        wp.floor = coords[0]
        wp.phys_pos = (coords[1], coords[2])
        waypoints[current_wp][cam_id] = wp
    if event == cv2.EVENT_MBUTTONDOWN:
        images[cam_id] = np.copy(temp_images[cam_id])
        del (waypoints[current_wp][cam_id])


def enter_handler():
    while True:
        res = raw_input("WP " + str(current_wp) + ": Please, enter the physical position floor,x,y: ")
        floor_and_pos = res.split(',')
        if len(floor_and_pos) != 3:
            print("Need three numbers separated with comma")
            continue
        try:
            ret = (int(floor_and_pos[0]), int(floor_and_pos[1]), int(floor_and_pos[2]))
            return ret
        except:
            print("Parameters need to be integers")
            continue


def pic_capture():
    for i in range(0, CAM_QUANTITY):
        # Attempt to capture an image 3 times.
        for j in range(0, 3):
            cap = cv2.VideoCapture(URL + CAMERA_LIST[i] + ":80" + CAMERA_LIST[i] + "/img.png")
            # cap = cv2.VideoCapture(i)
            if cap is not None:
                break
        ret, img = cap.read()
        if img is not None:
            for k in UPSIDE_DOWN_LIST.split(","):
                if k == CAMERA_LIST[i]:
                    img = cv2.flip(img, 0)
                    img = cv2.flip(img, 1)
            temp_images[i] = np.copy(img)
            images[i] = np.copy(img)
        cap.release()

    for i in range(0, CAM_QUANTITY):
        if images[i] is None:
            continue
        cv2.imshow(HEADER + CAMERA_LIST[i], images[i])
        cv2.setMouseCallback(HEADER + CAMERA_LIST[i], mouse_handler, i)


def find_color():
    lower_color = np.array([38, 50, 50], np.uint8)
    upper_color = np.array([75, 255, 255], np.uint8)
    found_flag = False
    for i in range(0, CAM_QUANTITY):
        if temp_images[i] is None:
            continue
        for x in range(0, WIDTH, 5):
            for y in range(0, HEIGHT, 5):
                cropped_image = temp_images[i][y:y + 5, x:x + 5]

                img_hsv = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2HSV)

                mask = cv2.inRange(img_hsv, lower_color, upper_color)
                amount_not_zero = cv2.countNonZero(mask)
                # If found:
                if amount_not_zero > (5 * 5) * COLOR_DETECT_THRESHOLD:
                    # print "Found the color on image " + str(i) + " at (" +str(x*5)+","+str(y*5)+")"
                    images[i] = np.copy(temp_images[i])
                    cv2.imshow(HEADER + CAMERA_LIST[i], images[i])
                    cv2.circle(images[i], (x, y), 25, (255, 0, 255), 3)
                    wp = WayPoint()
                    wp.cam_id = i
                    wp.cam_pos = (x, y)
                    wp.floor = coords[0]
                    wp.phys_pos = (coords[1], coords[2])
                    waypoints[current_wp][i] = wp

                    found_flag = True
                    break
            if found_flag is True:
                found_flag = False
                break


# Main function:
if __name__ == "__main__":

    coords = enter_handler()
    pic_capture()
    # find_color()

    while True:
        for i in range(0, CAM_QUANTITY):
            if images[i] is None:
                continue
            cv2.imshow(HEADER + CAMERA_LIST[i], images[i])

        k = cv2.waitKey(33)
        if k == 27 or k == 113:  # Esc key
            print("Exiting...")
            exit(0)
        if k == 105 or k == 10 or k == 13:  # Return(Enter) key

            cv2.destroyAllWindows()
            for i in range(0, 100):
                cv2.waitKey(10)

            # Increment the current waypoint number, and allocate another
            # dictionary.
            current_wp += 1
            waypoints.append({})

            # Get the coordinates of the next physical position of waypoint.
            coords = enter_handler()

            pic_capture()
            # find_color()
            continue
        if k == 114:  # 'R' key
            print "Refreshing captured images..."
            pic_capture()
            waypoints.pop()
            waypoints.append({})
            # find_color()
            continue
        if k == 115:  # 'S' key
            for i in range(0, len(waypoints)):
                print("WP " + str(i) + ":")
                for k, v in waypoints[i].items():
                    # print(str(k) + ":" )
                    print(str(v))
                print("\n")
            with open(CAL_SAVE_PATH, "wb") as f:
                pickle.dump(waypoints, f, 0)
                # pickle.dump(waypoints[0], f, pickle.HIGHEST_PROTOCOL)
            continue
        if k == -1:  # No key
            continue
        else:
            print k  # Print the pressed key code
