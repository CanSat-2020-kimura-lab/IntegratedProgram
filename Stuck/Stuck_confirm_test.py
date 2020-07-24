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

def get_accdata():
        #--- get bmx055 data ---#
        try:
                BMX055.bmx055_setup()
                time.sleep(0.2)
                bmxData = BMX055.bmx055_read()
                time.sleep(0.2)

        except KeyboardInterrupt:
                print()
        
        except Exception as e:
                print()
                print(e)

        #--- get acceralate sensor data ---#
        global accx,accy,accz
        accx = bmxData[0]
        accy = bmxData[1]
        accz = bmxData[2]
        return accx , accy , accz

def stuck_confirm():
        accdata = np.array([[accx,accy,accz]])
        #--- use Timer ---#
        global cond
        cond = True
        thread = Thread(target = timer , args=([3]))
        thread.start()
        #--- note start time ---#
        start = time.time()
        time_base = start
        global time_array
        time_array = np.array([[0]])
        try:
                while cond:
                        #--- escape by run faster ---#
                        run = pwm_control.Run()
                        run.straight_h
                        time_count = time.time() - time_base 
                        if time_count >= 0.2:
                                get_accdata()
                                #--- multi dimention accdata matrix ---#
                                accdata = np.append(accdata , np.array([[accx,accy,accz]]))
                                #--- multi dimention time_array matrix ---#
                                passed_time = time.time() - start
                                time_array = np.append(time_array , np.array([[passed_time]]))
                                #--- initialize time_base ---#
                                time_base = time.time()

        except KeyboardInterrupt:
                run = pwm_control.Run()
                run.stop()

        finally:
                run = pwm_control.Run()
                run.stop()

        global accx_data
        accx_data = accdata[:,0]

        #--- escape detection ---#
        move_judge = cor(accx_data,time_array)
        return move_judge 

def plot_data(accx_data,time_array):
        plt.scatter(accx_data,time_array,label ="acc-time relation")
        plt.legend()
        plt.show()

#--- caluculate Covariance ---#
def covar(n,m):
        m1 = mean(n)
        m2 = mean(m)
        n1 = n - m1
        n2 = m - m2
        n3 = n1 * n2
        n4 = mean(n3)
        #print('共分散:{0:.2f}'.format(n4))
        return n4

#--- caluculate correlation coefficients ---#
def cor(n,m):
        i = covar(n,m)
        j = stdev(n)
        k = stdev(m)
        cor = i / (j * k)
        #print('相関係数:{0:.2f}'.format(cor))
        return cor

def timer(t):
        global cond
        time.sleep(t)
        cond = False

if __name__ == "__main__":
        try:
                stuck_confirm()

        except KeyboardInterrupt:
                run = pwm_control.Run()
                run.stop()
                print("stop")

        finally:
                run = pwm_control.Run()
                run.stop()
                print('end')
