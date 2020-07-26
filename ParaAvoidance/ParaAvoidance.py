import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Camera')
sys.path.append('/home/pi/git/kimuralab/Detection/Run_phase')
sys.path.append('/home/pi/git/kimuralab/Detection')
sys.path.append('/home/pi/git/kimuralab/Detection/ParachuteDetection')
sys.path.append('/home/pi/git/kimuralab/Other')
import time
import cv2
import numpy as np
import Capture
import ParaDetection
import pwm_control
import runtest
import Other

if __name__ == '__main__':
	print("START: Judge covered by Parachute")
	t2 = time.time()
	t1 = t2
	while t2 - t1 < 60:
		Luxflug = ParaJudge(100)
		if Luxflug[0] == 1:
			break
		t1 =time.time()
	print("START: Parachute avoidance")
	try:
		for i in range(2):
			pwm_control.run = Run()
			pwm_control.run.straight_n()
      
			flug, area, photoname = ParaDetection.ParaDetection(photo)

			if flug == 1:
			runtest.run = Run()
			runtest.run.back()
        

			if flug == 0:
			runtest.run = Run()
			runtest.run.straight_h()

	except KeyboardInterrupt:
		print("Emergency!")
		runtest.run.stop()

	except:
		runtest.run.stop()
		print(traceback.format_exc())
