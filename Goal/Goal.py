#   --- path ---   #
import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Camera')
sys.path.append('/home/pi/git/kimuralab/Detection/Run_phase')
sys.path.append('/home/pi/git/kimuralab/Detection/GoalDetection')

import time
import pigpio
import traceback
from threading import Thread
import math

#   --- original moduule ---   #
import GPS
import Capture
import gps_navigate
import pwm_control
import goaldetection

#   --- path of photo ---   #
photo_path = '/home/pi/photo'

pi = pi.pigpio()

#   --- longitude and latitude of goal ---   #
lon_goal = 0
lat_goal = 0

#   --- Calculate the distance to the goal ---   #
def distance_detection(lon_goal,lat_goal):
	try:
		#   --- output GPS data every 1 second --- #
		while 1:
			value = GPS.readGPS()   #value = [utc, Lat, Lon, sHeight, gHeight]
			lat_now = value[1]
			lon_now = value[2]
			#print(value)
			print('longitude = ' + str(lon_now))
			print('latitude = ' + str(lat_now))
			time.sleep(1)
			#   --- break if the value is successfully acquired   --- #
			if lat_new != -1.0 and lon_new != 0.0 :
				break

	except KeyboardInterrupt:
		print("\r\n KeyboardInterrupt, Serial Closed")

	except:
		print (traceback.format_exc())

	direction = gps_navigate.vincenty_inverse(lon_goal,lat_goal,lon_now,lat_now)
	distance = direction["distance"]
     
	return distance

if __name__ == '__main__':
	GPS.openGPS()
	try:
		distance = distance_detection(lon_goal,lat_goal)
		while distance <= 5:
			Capture.Capture(photo_path,320,240)
			while color_area <= Thd1:
				while color_area <= Thd2:
					run = pwm_control.Run()
					run.turn_right_l()
					time.sleep(1.0)
					Capture.Capture(photo_path340,320,240)
				run = pwm_control.Run()
				run.straight_h()
				time.sleep(2.0)
			run = pwm_control.Run()
			run.stop()
			print('Goal')

	except KeyboardInterrupt:
		run = Run()
		run.stop()
		print('\r\t KeyboardInterrupt, Run stop')

	except:
		run = Run()
		run.stop()
		print('\r\t except, Run stop')

	finally:
		run = Run()
		run.stop()
		GPS.colseGPS()
