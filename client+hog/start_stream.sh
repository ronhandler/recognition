#!/bin/bash

for i in {0..7} ; do ssh odroid@192.168.1.20$i "cd recognition/temp_flask/;
./app.py > /dev/null 2>&1 &"; done

