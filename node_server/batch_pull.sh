#!/bin/bash

for i in {0..7} ; do ssh odroid@192.168.1.20$i "cd recognition/;
git pull"; done
