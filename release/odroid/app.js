#!/usr/bin/node

var express = require('express');
var app = express();
var util  = require('util');
var exec = require('child_process').exec;

app.use(express.static(__dirname + '/public'));

var hostname = require('os').hostname();
var port = "800"+hostname.slice(-1);
port = parseInt(port);
console.log('hostname: %s', hostname);
console.log('port: %s', port);

var server = app.listen(port, function () {
  console.log('Example app listening at http://%s:%s', hostname, port);
});

