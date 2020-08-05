#   --- path ---   #
import sys
#sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Camera')
sys.path.append('/home/pi/git/kimuralab/Detection/Run_phase')
sys.path.append('/home/pi/git/kimuralab/Detection/GoalDetection')

import time
import pigpio
import traceback
from threading import Thread
import math

#   --- original moduule ---   #
import Capture
import pwm_control
import goaldetection

#   --- path of photo ---   #
photo_path = '/home/pi/photo/phto'

pi = pigpio.pi()

if __name__ == '__main__':
	try:
		while 1:
			goalflug = 1
			while goalflug != 0:
				goalflug, goalarea, goalGAP, photoname = goaldetection.GoalDetection("/home/pi/photo/photo",200 ,20, 80, 7000)
				print("goalflug", goalflug, "goalarea",goalarea, "goalGAP", goalGAP, "name", photoname)
				if goalGAP <= -30.0:
					print('Turn left')
					run = pwm_control.Run()
					run.turn_left_l()
					time.sleep(0.5)
				
				elif 30 <= goalGAP:
					print('Turn right')
					run = pwm_control.Run()
					run.turn_right_l()
					time.sleep(0.5)
				
				else:
					print('Go straight')
					run = pwm_control.Run()
					run.straight_h()
					time.sleep(1.0)
				
			run = pwm_control.Run()
			run.stop()
			print('Rover has reached the Goal !')
			break

	except KeyboardInterrupt:
		run = pwm_control.Run()
		run.stop()
		print('\r\t except, Run stop')

	finally:
		run = pwm_control.Run()
		run.stop()
		print('Finnish !')
