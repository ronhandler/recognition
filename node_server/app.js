#!/usr/bin/node

var express = require('express');
var app = express();
var util  = require('util');
var exec = require('child_process').exec;

app.use(express.static(__dirname + '/public'));

//app.get('/blah.png', function (req, res) {
  //console.log('Capturing image');
  //exec('./ron.py', function callback(error, stdout, stderr){
    //console.log('Serving image');
    //res.sendFile(__dirname + '/public/img.png');
  //});
//});

var server = app.listen(8000, function () {
  var host = server.address().address;
  var port = server.address().port;

  console.log('Example app listening at http://%s:%s', host, port);
});
