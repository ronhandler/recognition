#! /usr/bin/bash

killall ./app.js
killall node
killall ./loop.py
killall python

./loop.py& ./app.js&

