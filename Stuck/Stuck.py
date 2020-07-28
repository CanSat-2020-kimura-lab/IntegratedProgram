import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')
sys.path.append('/home/pi/git/kimuralab/Detection/Run_phase') 
#--- default module ---#
import math
import time
import traceback
from threading import Thread
from statistics import mean, median, variance, stdev
#--- must be installed module ---#
import numpy as np
import matplotlib.pyplot as plt
#--- original module ---#
import BMX055
import gps_navigate
import pwm_control
import GPS

GPS_data = [0.0,0.0,0.0,0.0,0.0]

def stuck_detection1():
	GPS.openGPS()
	try:
		while True:
			value = GPS.readGPS()
			latitude_past = value[1]
			longitude_past = value[2]
			time.sleep(1)
			if latitude_past != -1.0 and longitude_past != 0.0 :
				break
	except KeyboardInterrupt:
		GPS.closeGPS()
		print("\r\nKeyboard Intruppted, Serial Closed")

	except:
		GPS.closeGPS()
		print (traceback.format_exc())
	return longitude_past,latitude_past

def stuck_detection2(longitude_past,latitude_past):
	try:
		GPS.openGPS()
		while True:
			value = GPS.readGPS()
			latitude_new = value[1]
			longitude_new = value[2]
			print(value)
			print('longitude = '+str(longitude_new))
			print('latitude = '+str(latitude_new))
			time.sleep(1)
			if latitude_new != -1.0 and longitude_new != 0.0 :
				break
	except KeyboardInterrupt:
		GPS.closeGPS()
		print("\r\nKeyboard Intruppted, Serial Closed")

	except:
		GPS.closeGPS()
		print (traceback.format_exc())
	direction = gps_navigate.vincenty_inverse(longitude_past,latitude_past,longitude_new,latitude_new)
	distance = direction["distance"]        
	return distance


def stuck_escape():
	#--- run back and change direction ---#
	#--- run back and change direction ---#
	try:
		#--- run back ---#
		run = pwm_control.Run()
		run.back()
		time.sleep(2)

	except KeyboardInterrupt:
		run = pwm_control.Run()
		run.stop()
		time.sleep(2)

	finally:
		run = pwm_control.Run()
		run.stop()
		time.sleep(2)

	try:
		#--- change direction ---#
		run = pwm_control.Run()
		run.turn_right()
		time.sleep(1)

	except KeyboardInterrupt:
		run = pwm_control.Run()
		run.stop()
		time.sleep(2)

	finally:
		run = pwm_control.Run()
		run.stop()
		time.sleep(2)

def timer(t):
	global cond
	time.sleep(t)
	cond = False

if __name__ == "__main__":
	while True:
		#--- note GPS data first ---#
		location = stuck_detection1()
		longitude_past = location[0]
		latitude_past = location[1]
		print('longitude_past = '+str(longitude_past))
		print('latitude_past = '+str(latitude_past))
		try:
			#--- use Timer ---#
			cond = True
			thread = Thread(target = timer , args=([5]))
			thread.start()
			while cond:
				#--- run 5s ---#
				run = pwm_control.Run()
				run.straight_h
			run = pwm_control.Run()
			run.stop()
			time.sleep(2)
			#--- compare GPS data and calcurate distance ---#
			distance = stuck_detection2(longitude_past,latitude_past)
			print('distance = '+str(distance))
			if distance >= 20:
				print("rover moved!")                                        
			else:
				#--- if rover didn't move 5m,carry out stuck cofirm ---#
				stuck_escape()
				print("stuck escape")

		except KeyboardInterrupt:
			run = pwm_control.Run()
			run.stop()
			break

		finally:
			run = pwm_control.Run()
			run.stop()
			break
