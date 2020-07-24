import sys
sys.path.append('/home/pi/git/kimuralab/SensormoduleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/SensormoduleTest/GPS')
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
'''        
def stuck_detection_past(stuck_count):
        get_accdata()
        global stuck_count
        if accx < 0:
                stuck_count += 1
        return stuck_count
'''
def stuck_detection1():
        GPS.openGPS()
        value = GPS.readGPS()
        latitude_past = value[1]
        longitude_past = value[2]
        return longitude_past,latitude_past

def stuck_detection2(longitude_past,latitude_past):
        GPS.openGPS()
        value = GPS.readGPS()
        latitude_new = value[1]
        longitude_new = value[2]
        direction = gps_navigate.vincenty_inverse(longitude_past,latitude_past,longitude_new,latitude_new)
        distance = direction["distance"]        
        return distance 

def stuck_confirm():
        accdata = np.array([[accx,accy,accz]])
        #--- use Timer ---#
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

def stuck_escape(move_judge):
        if move_judge >= 0.5:
                print("Successed to escape")
        else:
                print("Failed to escape")
                #--- run back and change direction ---#
                #--- use Timer ---#
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
                        #--- compare GPS data and calcurate distance ---#
                        distance = stuck_detection2(longitude_past,latitude_past)
                        print('distance = '+str(distance))
                        if distance >= 5:
                                print("rover moved!")                                        
                        else:
                                #--- if rover didn't move 5m,carry out stuck cofirm ---#
                                move_judge = stuck_confirm()
                                print(move_judge)
                                stuck_escape(move_judge)

                except KeyboardInterrupt:
                        run = pwm_control.Run()
                        run.stop()
                        break

                finally:
                        run = pwm_control.Run()
                        run.stop()
                        break

        plot_data(accx_data,time_array)
