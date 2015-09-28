#!/bin/bash

for i in {0..7} ; do ssh odroid@192.168.1.20$i "echo 'Hey! I'm odroid:'; hostname; cd recognition/; git pull"; done
