#!/bin/bash

for i in 2 4 ; do echo "Starting up $i . . ."; ssh odroid@192.168.1.20$i "cd recognition/node_server/;
./start_stream.sh > /dev/null 2>&1 &"; done
