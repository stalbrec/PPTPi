import os
import glob
import time
import re
import numpy as np

#Inspired by Tutorial-ebook from AZ-delivery
#https://www.az-delivery.de/products/ds18b20-kostenfreies-e-book?_pos=1&_sid=557a3d6f6&_ss=r
class TemperaturSensoren():
	
	def __init__(self):
		#setup 1-wire sensors
		os.system('sudo modprobe w1-gpio')
		os.system('sudo modprobe w1-therm')
		
		self._w1_dir = '/sys/bus/w1/devices/'
		devices_dirs = glob.glob(self._w1_dir+'/28*')
		
		self._n_devices = len(devices_dirs)
		self._devices = [device_dir+'/w1_slave' for device_dir in devices_dirs]
		
	def device_names(self):
		def extract_name(path):
			sensor_name_pattern = re.compile(self._w1_dir+'(?P<sense_name>[0-9]*-[0-9a-zA-Z]+)/w1_slave')
			if(sensor_name_pattern.match(path) is None):
				raise BaseException("Could not extract sensor name from w1-slave dir")
			return sensor_name_pattern.match(path).groupdict()['sense_name']
		return np.array([extract_name(path) for path in self._devices])

	def read_w1_slave(self,device_index):
		w1_slave = open(self._devices[device_index],'r')
		lines = w1_slave.readlines()
		w1_slave.close()
		return lines


	def tempC(self, device_index=0, retries = 5):
		lines = self.read_w1_slave(device_index)
		while (lines[0].strip()[-3:]!="YES") and (retries>0):
			time.sleep(0.1)
			lines = self.read_w1_slave(device_index)
			retries -= 1
		if retries == 0:
			return -999
		
		temperatur_pattern = re.compile(r"([0-9a-zA-Z]{2} )+t=(?P<temp>[0-9]+)")
		if(temperatur_pattern.match(lines[1]) is None):
			return -999
		return float(temperatur_pattern.match(lines[1]).groupdict()['temp'])/1000.
	
	def temps(self):
		return np.array([self.tempC(i) for i in range(self._n_devices)])
			
	
if(__name__ == '__main__'):
	
	ts = TemperaturSensoren()
	
	print(ts.device_names())
	
	print(ts.temps())	
			
		
