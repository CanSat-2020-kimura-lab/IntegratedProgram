import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Camera')
sys.path.append('/home/pi/git/kimuralab/Detection/Run_phase')
sys.path.append('/home/pi/git/kimuralab/Detection')
sys.path.append('/home/pi/git/kimuralab/Detection/ParachuteDetection')
sys.path.append('/home/pi/git/kimuralab/Other')

#--- default module ---#
import time
import traceback
#--- must be installed module ---#
import numpy as np
import cv2
#--- original module ---#
import Capture
import ParaDetection
import pwm_control
import Other

def Parachute_Avoidance(flug):
	#--- There is Parachute arround rover ---#
	if flug == 1:
		#--- Avoid parachute by back control ---#
		run = pwm_control.Run()
		run.back()
		time.sleep(1)
		run.stop()
		#--- Avoid parachute by rotate control ---#
		while flug == 1:
			run = pwm_control.Run()
			run.turn_right_l()
			time.sleep(1)
			#--- Parachute detect repeatedly and avoid it ---#
			flug, area, photoname = ParaDetection.ParaDetection("/home/pi/photo/photo",320,240,200,10,120)

	#--- There is not Parachute arround rover ---#
	if flug == 0:
		run = pwm_control.Run()
		run.straight_h()
		time.sleep(1)
		#--- finish ---#

if __name__ == '__main__':
	print("START: Judge covered by Parachute")
	t2 = time.time()
	t1 = t2
	#--- Paracute judge for 60 seconds ---#
	while t2 - t1 < 60:
		Luxflug = ParaDetection.ParaJudge(100)
		if Luxflug[0] == 1:
			break
		t1 =time.time()
	print("START: Parachute avoidance")
	try:
		#--- first parachute detection ---#
		flug, area, photoname = ParaDetection.ParaDetection("/home/pi/photo/photo",320,240,200,10,120)
		Parachute_Avoidance(flug)


	except KeyboardInterrupt:
		print("Emergency!")
		run = pwm_control.Run()
		run.stop()

	except:
		run = pwm_control.Run()
		run.stop()
		print(traceback.format_exc())
