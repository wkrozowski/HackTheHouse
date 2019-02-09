#!/usr/bin/python

from time import sleep
from Adafruit_CCS811 import Adafruit_CCS811
import sys
import Adafruit_DHT

ccs =  Adafruit_CCS811()

while not ccs.available():
	pass
temp = ccs.calculateTemperature()
ccs.tempOffset = temp - 25.0

while(1):
	humidity, temperature = Adafruit_DHT.read_retry(22, 4)
	if ccs.available():
	    temp = ccs.calculateTemperature()
	    if not ccs.readData():
	      print "sensor1: CO2: ", ccs.geteCO2(), "ppm, TVOC: ", ccs.getTVOC(), " temp: ", temp

	    else:
	      print "ERROR!"
	      while(1):
	      	pass
	if humidity is not None and temperature is not None:
		print('sensor2: Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
	else:
		print('Failed to get reading. Try again!')
		sys.exit(1)
	sleep(2)
