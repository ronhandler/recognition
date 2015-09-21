#! /bin/bash

killall app.js
killall node
killall nodejs
killall loop.py
killall python

./loop.py& ./app.js&

