import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')
sys.path.append('/home/pi/git/kimuralab/Detection/Run_phase')
#--- must be installed module ---#
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
#--- default module ---#
import math
import time
import traceback
from threading import Thread
#--- original module ---#
import BMX055 
import pwm_control
import GPS
import gps_navigate

def get_data():        
	#--- get bmx055 data ---#
        try:
                BMX055.bmx055_setup()
                #time.sleep(0.2)
                bmxData = BMX055.bmx055_read()
                #time.sleep(0.2)

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

        #--- get magnet sensor data ---#
        global magx,magy,magz
        magx = bmxData[3]
        magy = bmxData[4]
        magz = bmxData[5]
        return magx , magy , magz , accx , accy , accz

def magdata_matrix():
        try:
                get_data()
                #--- initial GPS value ---#
                global magdata
                magdata = np.array([[magx,magy,magz]])
                #time.sleep(0.5)
'''
                #--- use Timer ---#
                global cond
                cond = True
                thread = Thread(target = timer,args=([10]))
                thread.start()

                while cond:
                        run = pwm_control.Run()
                        run.turn_right()
                        get_data()
                        #--- multi dimention matrix ---#
                        magdata = np.append(magdata , np.array([[magx,magy,magz]]) , axis = 0)
                        #time.sleep(0.1)
'''
                for i in range(50):
                        get_data()
                        #--- multi dimention matrix ---#
                        magdata = np.append(magdata , np.array([[magx,magy,magz]]) , axis = 0)

        except KeyboardInterrupt:
                print("stop")
                
        finally:
                print("finish")
                
        return magdata

def calculate_offset(magdata):
        global magx_array , magy_array , magz_array
        #--- manage each element sepalately ---#
        magx_array = magdata[:,0] 
        magy_array = magdata[:,1]
        magz_array = magdata[:,2]

        #--- find maximam GPS value and minimam GPS value respectively ---#
        magx_max = np.argmax(magx_array)
        magy_max = np.argmax(magy_array)
        magz_max = np.argmax(magz_array)

        magx_min = np.argmin(magx_array)
        magy_min = np.argmin(magy_array)
        magz_min = np.argmin(magz_array)            
        
        #--- calucurate offset ---#
        global magx_off , magy_off , magz_off
        magx_off = (magx_max + magx_min)/2
        magy_off = (magy_max + magy_min)/2
        magz_off = (magz_max + magz_min)/2
        print("magx_off = "+str(magx_off))
        print("magy_off = "+str(magy_off))
        print("magz_off = "+str(magz_off))

        return magx_array , magy_array , magz_array , magx_off , magy_off , magz_off

def plot_data_2D(magx_array,magy_array):
        plt.scatter(magx_array,magy_array,label ="Calibration")
        plt.legend()
        plt.show()

def plot_data_3D(magx_array,magy_array,magz_array):
        fig = plt.figure()
        ax = Axes3D(fig)
        #--- label name ---#
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.plot(magx_array , magy_array , magz_array , marker="o" , linestyle='None')
        plt.show()

def timer(t):
        global cond
        time.sleep(t)
        cond = False

if __name__ == "__main__":
        try:
                #--- calculate offset ---#
                magdata_matrix()        
                calculate_offset(magdata)
                time.sleep(0.1)
                #--- plot data ---#
                plot_data_2D(magx_array,magy_array)
                #plot_data_3D(magx_array,magy_array,magz_array)
                
                #--- calculate θ ---#
                get_data()
                calculate_angle_2D(magx,magy,magx_off,magy_off)
