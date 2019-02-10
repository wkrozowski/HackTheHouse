#!/usr/bin/python

#Imported packages
from flask import Flask
import json
import sys
import _thread
import serial
import time

#Initial declarations
app = Flask(__name__)
ser = serial.Serial('/dev/ttyACM0',9600)	#Open the serial port



#Global variables
global fingerprint_info
fingerprint_info = {
	'Message1':			"",
	'Timestamp1':	time.time(),
}

global TRIG
global ECHO
TRIG = 23 
ECHO = 24

#Function reading from serial port
def read_fingerprint():
	global fingerprint_info
	while True:
		read_serial=ser.readline()
		read_serial=bytes(read_serial)
		read_serial=read_serial[:-2]
		read_serial=read_serial.decode("utf-8") 
		if read_serial:
			fingerprint_info['Message1']=str(read_serial)
			fingerprint_info['Timestamp1']=time.time()

#Dummy main node
@app.route('/')
def index():
    return 'Main node'
    
@app.route('/get_fingerprint', methods=['POST', 'GET'])
def get_fingerprint():
	global fingerprint_info
	return json.dumps(fingerprint_info)
			
#Function opening flask server
def run_server():    
	if __name__ == '__main__':
		app.run(debug=True, host='0.0.0.0')

#Main function flow
try:

	_thread.start_new_thread(read_fingerprint, ())
	run_server()
except:
   print ("Error: unable to start thread")

while 1:
   pass		
