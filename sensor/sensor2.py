#!/usr/bin/python

#Imported packages
from flask import Flask
import json
import sys
import RPi.GPIO as GPIO
import _thread

import time
import Adafruit_DHT
from Adafruit_CCS811 import Adafruit_CCS811

#Initial declarations
app = Flask(__name__)

#Run CCS811 configuration
global ccs
ccs =  Adafruit_CCS811()
while not ccs.available():
		pass
temp = ccs.calculateTemperature()
ccs.tempOffset = temp - 25.0


#Global variables

global sensor_info
sensor_info = {                   
  'TemperatureOut':		0,
  'TemperatureIn':		0,
  'Humidity': 			0,
  'PPM':				0,
  'TVOC':				0,
  'Distance':			0,
  'Timestamp':			time.time(),
}

global TRIG
global ECHO
TRIG = 23 
ECHO = 24

#Read from DHT sensor
def read_DHT():
	global sensor_info
	while True:
		humidity, temperature = Adafruit_DHT.read_retry(22, 4)
		if humidity is not None and temperature is not None:
			sensor_info['TemperatureIn'] = round(temperature,2)
			sensor_info['Humidity'] = round(humidity,2)

#Read from CCS811			
def read_CCS811():
	global ccs
	while True:
		sensor_info['TemperatureOut'] = ccs.calculateTemperature()
		if not ccs.readData():
			sensor_info['PPM'] = round(ccs.geteCO2(),2)
			sensor_info['TVOC'] = round(ccs.getTVOC(),2)
			
#Read from ultrasonic sensor			
def read_distance():
	while True:
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

		sensor_info['Distance'] = round(distance, 2)
		GPIO.cleanup()
		

#Dummy main node
@app.route('/')
def index():
    return 'Main node'

@app.route('/get_data', methods=['POST', 'GET'])
def get_sensor_data():
	global sensor_info
	sensor_info['Timestamp']=time.time()
	return json.dumps(sensor_info)
			
#Function opening flask server
def run_server():    
	if __name__ == '__main__':
		app.run(debug=True, host='0.0.0.0')

#Main function flow
try:
	_thread.start_new_thread(read_DHT, ())
	_thread.start_new_thread(read_distance, ())
	_thread.start_new_thread(read_CCS811, ())
	run_server()
except:
   print ("Error: unable to start thread")

while 1:
   pass		
