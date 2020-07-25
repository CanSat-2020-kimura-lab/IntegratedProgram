import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')
sys.path.append('/home/pi/git/kimuralab/Detection/Run_phase') 
#--- default module ---#
import time
#--- original module ---#
import pwm_control

def stuck_escape():

        #--- run back and change direction ---#
        try:
                #--- run back ---#
                run = pwm_control.Run()
                run.back()
                time.sleep(1.5)

        except KeyboardInterrupt:
                run = pwm_control.Run()
                run.stop()
                time.sleep(1)

        finally:
                run = pwm_control.Run()
                run.stop()
                time.sleep(1)

        try:
                #--- change direction ---#
                run = pwm_control.Run()
                run.turn_right()
                time.sleep(0.5)

        except KeyboardInterrupt:
                run = pwm_control.Run()
                run.stop()
                time.sleep(1)

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
