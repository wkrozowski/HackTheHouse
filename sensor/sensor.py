#!/usr/bin/python

from time import sleep
from Adafruit_CCS811 import Adafruit_CCS811
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import thread
import json


global mydict
mydict = {                   
  'TemperatureOut':		0,
  'TemperatureIn':		0,
  'Humidity': 			0,
  'PPM':				0,
  'TVOC':				0,
}
ccs =  Adafruit_CCS811()

while not ccs.available():
		pass
temp = ccs.calculateTemperature()
ccs.tempOffset = temp - 25.0

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
		
def handle():
	global mydict
	while(1):
		json_string = json.dumps(mydict)
		print json_string
		sleep(2)
		
try:
   thread.start_new_thread(measure, ())
   thread.start_new_thread(handle, ())
except:
   print "Error: unable to start thread"

while 1:
   pass
	
		
