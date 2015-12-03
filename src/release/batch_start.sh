#!/bin/bash

for i in `cat ./config.txt |grep camera_list |grep -oE "[0-9].*" |tr "," " "` ; do echo "Starting up $i . . ."; ssh odroid@192.168.1.20$i "cd recognition/node_server/; ./start_stream.sh > /dev/null 2>&1 &"; done

#for i in 4 ; do echo "Starting up $i . . ."; ssh odroid@192.168.1.20$i "cd recognition/node_server/; ./start_stream.sh > /dev/null 2>&1 &"; done
