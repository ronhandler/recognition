## Setup and Pre-installation
### Camera Unit Installation
Repeat the following instructions per camera unit.
Each camera unit is assembled from the following:
1. Odroid u3.
2. Sony PsEye camera.
3. USB Wifi dongel.
4. MicroSD card formatted to Ubunto Odroid image.

The following should be installed on the Odroid as well:

1. OpenCV for python.
2. npm.
3. nodejs.
4. git.

The following should be installed on the server:

1. OpenCV for python.
2. git

#### Installation Instructions
1. Download and install all the software above on the odroid.
2. Clone the git repository, using the command: `git clone https://github.com/ronhandler/recognition.git`
3. In the repository directory, enter "node_server" folder (using terminal), and execute the commands:
  * `npm init`
  * `npm install express`
4. Set a serial number to the Odroid using: `sudo echo "odroid20x" > /etc/hostname`. Replace x with any unique number.
5. Connect the Odroid to your wifi LAN.
6. Reboot the Odroid.

###Router Configuration
After we configured all Odroids, and connected them to the wireless network (Don't use wired connection), we'd like to configure the router.

1. Set a static IP address for each wireless connected odroid, by the following template: 192.168.1.20x. Replace x with the corresponding serial number you set to the odroid.
2. Make sure that the DHCP serves IP addresses in the range 192.168.1.0 - 192.168.1.255.
3. Restart the router and each odroid (important!).

### Server Installation
The server can be any machine, even another Odroid.

1. Download and install all the software above on the server machine.
2. Clone the git repository, using the command: `git clone https://github.com/ronhandler/recognition.git`
3. Edit the file: `recognition/src/release/config.txt` and make sure that the `camera_list` setting lists the connected camera unit's serial number (only the last number of each serial number).
4. Run: `recognition/src/release/batch_start.sh` and watch each one of the cameras start recording (a red led will turn on).
5. Run: `recognition/location_receive_server`.
6. Run: `recognition/src/release/calibrate/cal.py` and [generate a calibration map](#generate-a-calibration-map).
7. Edit the file: `recognition/src/release/config.txt` and make sure that the setting for route1, and route2 have a list of waypoints separated with `,`.
8. Run: `recognition/src/release/route_manager/routes_manager.py`.
9. Enter `route1` or `route2` in the console of the running `routes_manager.py` process.
10. Run: `recognition/src/release/server/server.py` to start the system.

## Generate a calibration map.
1. After executing `cal.py`, follow the on-screen instructions and enter floor number and location.
2. Wait for all the camera outputs to appear on the screen.
3. Click ,with the left mouse button, on the first waypoint location, as shown in the photos. Repeat until you've chosen all your waypoints.
4. Press "S" to save the map.
5. Press "Q" to quit.
* Note: When pressing "S" or "Q", focus should be on one of the GUI windows (photos or map).

## Receiver Server Integration
In order to connect our API to an external receiving server that, for instance, can use the coordinates to direct a quad-copter, you should reference the example program written in `location_receive_server.cpp` file.


