#!/usr/bin/python

from time import sleep
from Adafruit_CCS811 import Adafruit_CCS811
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import thread

ccs =  Adafruit_CCS811()

while not ccs.available():
		pass
temp = ccs.calculateTemperature()
ccs.tempOffset = temp - 25.0

def readHumidity():
	humidity, temperature = Adafruit_DHT.read_retry(22, 4)
	if humidity is not None:
		#make json tag - currently just print
		print('Humidity={1:0.1f}%'.format(temperature, humidity))
	else:
		print('Failed to get reading. Try again!')
		sys.exit(1)
		
def readTemperatureIn():
	humidity, temperature = Adafruit_DHT.read_retry(22, 4)
	if temperature is not None:
		#make json tag - currently just print
		print('Temp In={0:0.1f}*'.format(temperature))
	else:
		print('Failed to get reading. Try again!')
		sys.exit(1)

def readPPM():
	if ccs.available():
		temp = ccs.calculateTemperature()
		if not ccs.readData():
			print "CO2=", ccs.geteCO2(), "ppm"
	      
def readTVOC():
	if ccs.available():
		temp = ccs.calculateTemperature()
		if not ccs.readData():
			print "TVOC=", ccs.getTVOC()

def readTemperatureOut():
	temp = ccs.calculateTemperature()
	if not ccs.readData():
		print "temp2=", temp		
	     
def measure():
	while(1):
		readTemperatureIn()
		readHumidity()
		readPPM()
		readTVOC()
		readTemperatureOut()
		
def handle():
	while(1):
		print "waiting"
		
try:
   thread.start_new_thread(measure, ())
   thread.start_new_thread(handle, ())
except:
   print "Error: unable to start thread"

while 1:
   pass
	
		
