import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')
sys.path.append('/home/pi/git/kimuralab/Detection/Run_phase') 
#--- default module ---#
import math
import time
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

def stuck_escape():

        #--- run back and change direction ---#
        #--- use Timer ---#
        global cond
        cond = True
        thread = Thread(target = timer , args=([2]))
        thread.start()
        try:
                while cond:
                        #--- run back ---#
                        run = pwm_control.Run()
                        run.back()

        except KeyboardInterrupt:
                run = pwm_control.Run()
                run.stop()

        finally:
                run = pwm_control.Run()
                run.stop()
                time.sleep(1)
        #--- use Timer ---#
        cond = True
        thread = Thread(target = timer , args=([1]))
        thread.start()
        try:
                while cond:
                        #--- change direction ---#
                        run = pwm_control.Run()
                        run.turn_right()

        except KeyboardInterrupt:
                run = pwm_control.Run()
                run.stop()

        finally:
                run = pwm_control.Run()
                run.stop()
                time.sleep(1)

def timer(t):
        global cond
        time.sleep(t)
        cond = False

if __name__ == "__main__":
        try:
                stuck_escape()
        
        except KeyboardInterrupt:
                run = pwm_control.Run()
                run.stop()

        finally:
                run = pwm_control.Run()
                run.stop()
        
        try:
                run = pwm_control.Run()
                run.straight_h()
                time.sleep(1)

        except KeyboardInterrupt:
                run = pwm_control.Run()
                run.stop()

        finally:
                run = pwm_control.Run()
                run.stop()
