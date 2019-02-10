#!/usr/bin/python

from flask import Flask, jsonify
from time import sleep
from Adafruit_CCS811 import Adafruit_CCS811
app = Flask(__name__)
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import _thread
import json
import RPi.GPIO as GPIO
import datetime
global TRIG
global ECHO
global finger_print
finger_print = str("")
import serial
ser = serial.Serial('/dev/ttyACM0',9600)
TRIG = 23 
ECHO = 24

global mydict
mydict = {                   
  'TemperatureOut':		0,
  'TemperatureIn':		0,
  'Humidity': 			0,
  'PPM':				0,
  'TVOC':				0,
  'Distance':			0,
  'Timestamp':			time.time(),
}

global fingerprint_info

fingerprint_info = {
	'Message1':			"",
	'Timestamp1':	time.time(),
}
ccs =  Adafruit_CCS811()

while not ccs.available():
		pass
temp = ccs.calculateTemperature()
ccs.tempOffset = temp - 25.0


def readDistance():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(TRIG,GPIO.OUT)
	GPIO.setup(ECHO,GPIO.IN)
	GPIO.output(TRIG, False)

	time.sleep(2)

	GPIO.output(TRIG, True)
	time.sleep(0.00001)
	GPIO.output(TRIG, False)

	while GPIO.input(ECHO)==0:
		pulse_start = time.time()

	while GPIO.input(ECHO)==1:
		pulse_end = time.time()

	pulse_duration = pulse_end - pulse_start

	distance = pulse_duration * 17150

	distance = round(distance, 2)
	GPIO.cleanup()
	return distance

def readHumidity():
	humidity, temperature = Adafruit_DHT.read_retry(22, 4)
	if humidity is not None:
		return round(humidity,2)
		
def readTemperatureIn():
	humidity, temperature = Adafruit_DHT.read_retry(22, 4)
	if temperature is not None:
		return round(temperature,2)

def readPPM():
	if ccs.available():
		temp = ccs.calculateTemperature()
		if not ccs.readData():
			return round(ccs.geteCO2(),2)
	      
def readTVOC():
	if ccs.available():
		temp = ccs.calculateTemperature()
		if not ccs.readData():
			return round(ccs.getTVOC(),2)

def readTemperatureOut():
	temp = ccs.calculateTemperature()
	if not ccs.readData():
		return round(temp,2)

global temperatureInside
global temperatureOutside
global PPMValue
global TVOCValue
global i

temperatureInside = readTemperatureIn()
humidityValue = readHumidity()
PPMValue = readPPM()
TVOCValue = readTVOC()
temperatureOutside = readTemperatureOut()
i = 0
					     
def measure():
	global mydict
	while(1):
		mydict['TemperatureIn'] = readTemperatureIn()
		mydict['Humidity'] = readHumidity()
		mydict['PPM'] = readPPM()
		mydict['TVOC'] = readTVOC()
		mydict['TemperatureOut'] = readTemperatureOut()
		mydict['Distance']=readDistance()
		mydict['Timestamp']=time.time()
		#json_string = json.dumps(mydict)
		#print (json_string)
		
def handle():
	global mydict
	while(1):
		json_string = json.dumps(mydict)
		print (json_string)
		sleep(2)
		
def read_fingerprint():
	global finger_print
	global fingerprint_info
	while True:
		read_serial=ser.readline()
		read_serial=bytes(read_serial)
		read_serial=read_serial[:-2]
		read_serial=read_serial.decode("utf-8") 
		if read_serial:
			finger_print=read_serial
			fingerprint_info['Message1']=str(finger_print)
			fingerprint_info['Timestamp1']=time.time()

@app.route('/')
def index():
    return 'Hello world'

@app.route('/get_data', methods=['POST', 'GET']) 
def get_data():
    global mydict
    return jsonify(mydict)
    
@app.route('/get_fingerprint', methods=['POST', 'GET'])
def get_fingerprint():
	global finger_print
	global fingerprint_info
	return jsonify(fingerprint_info)

def run_server():    
	if __name__ == '__main__':
		app.run(debug=True, host='0.0.0.0')
		
try:
	_thread.start_new_thread(measure, ())
	_thread.start_new_thread(read_fingerprint, ())
	run_server()
except:
   print ("Error: unable to start thread")

while 1:
   pass

while 1:
   pass
