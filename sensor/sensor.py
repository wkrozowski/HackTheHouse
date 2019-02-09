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
global TRIG
global ECHO
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
		return humidity
		
def readTemperatureIn():
	humidity, temperature = Adafruit_DHT.read_retry(22, 4)
	if temperature is not None:
		return temperature

def readPPM():
	if ccs.available():
		temp = ccs.calculateTemperature()
		if not ccs.readData():
			return ccs.geteCO2()
	      
def readTVOC():
	if ccs.available():
		temp = ccs.calculateTemperature()
		if not ccs.readData():
			return ccs.getTVOC()

def readTemperatureOut():
	temp = ccs.calculateTemperature()
	if not ccs.readData():
		return temp

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
		json_string = json.dumps(mydict)
		print (json_string)
		
def handle():
	global mydict
	while(1):
		json_string = json.dumps(mydict)
		print (json_string)
		sleep(2)
		
@app.route('/')
def index():
    return 'Hello world'

@app.route('/get_data', methods=['POST', 'GET']) 
def get_data():
    global mydict
    return jsonify(mydict)

def run_server():    
	if __name__ == '__main__':
		app.run(debug=True, host='0.0.0.0')
		
try:
	_thread.start_new_thread(measure, ())
	run_server()
except:
   print ("Error: unable to start thread")

while 1:
   pass

while 1:
   pass
