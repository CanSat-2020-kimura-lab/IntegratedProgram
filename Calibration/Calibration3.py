import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Wireless')
sys.path.append('/home/pi/git/kimuralab/Detection/Run_phase')
sys.path.append('/home/pi/git/kimuralab/Other')

#--- must be installed module ---#
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
#--- default module ---#
from math import cos,sin,atan,sqrt,degrees
import time
import traceback
from threading import Thread
#--- original module ---#
import BMX055 
import IM920
import pwm_control
import GPS
import gps_navigate
import Other

GPS_data = [0.0,0.0,0.0,0.0,0.0]
RX = 18

Calibration_rotate_controlLog = '/home/pi/log/Calibration_rotate_controlLog.txt'

def get_data():
	#--- get bmx055 data ---#
	try:
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
	magx = bmxData[6]
	magy = bmxData[7]
	magz = bmxData[8]
	
	#--- compensate magdata ---#
	θr = atan(accy/accx)
	θp = atan(accx/(sqrt(accy**2 + accz**2)))

	magx = magx*cos(θp) + magy*sin(θr)*sin(θp) + magz*cos(θr)*sin(θp)
	magy = magy*cos(θr) - magz*sin(θr)
	magz = magx*(-sin(θp)) + magy*sin(θr)*cos(θp) + magz*cos(θr)*cos(θp)

	return magx , magy , magz , accx , accy , accz

def get_magdata_average():
		#--- get bmx055 data ---#
	try:
		get_data()
		global magdata_average
		magdata_average = np.array([[magx,magy,magz]])
		for i in range(10):
			get_data()
			magdata_average = np.append(magdata_average , np.array([[magx,magy,magz]]) , axis = 0)
			time.sleep(0.05)

	except KeyboardInterrupt:
		print('Keyboard Intrrupt')
	
	except Exception as e:
		print()
		print(e)

	#--- manage each element sepalately ---#
	magx_array2 = magdata[:,0] 
	magy_array2 = magdata[:,1]

	global magx_average,magy_average
	magx_average = np.average(magx_array2)
	magy_average = np.average(magy_array2)

	return magx_average , magy_average

def calculate_offset():
	try:
		get_data()
		#--- initialize GPS value ---#
		global magdata
		magdata = np.array([[magx,magy,magz]])
		#time.sleep(0.5)
		for i in range(60):
			run = pwm_control.Run()
			run.turn_right()
			get_data()
			#--- multi dimention matrix ---#
			magdata = np.append(magdata , np.array([[magx,magy,magz]]) , axis = 0)
			time.sleep(0.1)

	except KeyboardInterrupt:
		run = pwm_control.Run()
		run.stop()
		
	finally:
		run = pwm_control.Run()
		run.stop()

	global magx_array , magy_array , magz_array
	#--- manage each element sepalately ---#
	magx_array = magdata[:,0] 
	magy_array = magdata[:,1]
	magz_array = magdata[:,2]

	#--- find maximam GPS value and minimam GPS value respectively ---#
	magx_max = magx_array[np.argmax(magx_array)]
	magy_max = magy_array[np.argmax(magy_array)]
	magz_max = magz_array[np.argmax(magz_array)]

	magx_min = magx_array[np.argmin(magx_array)]
	magy_min = magy_array[np.argmin(magy_array)]
	magz_min = magz_array[np.argmin(magz_array)]          
	
	#--- calucurate offset ---#
	global magx_off , magy_off , magz_off
	magx_off = (magx_max + magx_min)/2
	magy_off = (magy_max + magy_min)/2
	magz_off = (magz_max + magz_min)/2
	#print("magx_off = "+str(magx_off))
	#print("magy_off = "+str(magy_off))
	#print("magz_off = "+str(magz_off))

	return magx_array , magy_array , magz_array , magx_off , magy_off , magz_off , magdata

def calculate_angle_2D(magx,magy,magx_off,magy_off):
	#--- recognize rover's direction ---#
	#--- North = 0 , θ = (direction of sensor) ---#
	#--- -90 <= θ <= 90 ---#
	global θ
	θ = degrees(atan((magy-magy_off)/(magx-magx_off)))
	if θ >= 0:
		if magx-magx_off < 0 and magy-magy_off < 0: #Third quadrant
			θ = θ + 180 #180 <= θ <= 270
		if magx-magx_off > 0 and magy-magy_off > 0: #First quadrant
			pass #0 <= θ <= 90
	else:
		if magx-magx_off < 0 and magy-magy_off > 0: #Second quadrant
			θ = 180 + θ #90 <= θ <= 180
		if magx-magx_off > 0 and magy-magy_off < 0: #Fourth quadrant
			θ = 360 + θ #270 <= θ <= 360
	
	#--- Half turn  ---#
	θ += 180
	if θ >= 360:
		θ -= 360
	#print('magx-magx_off = '+str(magx-magx_off))
	#print('magy-magy_off = '+str(magy-magy_off))
	print('calculate:θ = '+str(θ))
	#--- 0 <= θ <= 360 ---#
	return θ

def calculate_angle_3D(accx,accy,accz,magx,magy,magz,magx_off,magy_off,magz_off):
	#--- recognize rover's direction ---#
	#--- calculate roll angle ---#
	Φ = degrees(atan(accy/accx))
	#--- calculate pitch angle ---#
	ψ = degrees(atan((-accx)/(accy*sin(Φ) + accz*cos(Φ))))
	#-- North = 0 , θ = (direction of sensor) ---#
	global θ
	θ = degrees(atan((magz - magz_off)*sin(Φ) - (magy - magy_off)*cos(Φ))/((magx - magx_off)*cos(ψ) + (magy - magy_off)*sin(ψ)*sin(Φ) +(magz - magz_off)*sin(ψ)*cos(Φ)))
	if θ >= 0:
		if magx-magx_off < 0 and magy-magy_off < 0: #Third quadrant
			θ = θ + 180 #180 <= θ <= 270
	else:
		if magx-magx_off < 0 and magy-magy_off > 0: #Second quadrant
			θ = 180 + θ #90 <= θ <= 180
		if magx-magx_off > 0 and magy-magy_off < 0: #Fourth quadrant
			θ = 360 + θ #270 <= θ <= 360
	
	print('magx-magx_off = '+str(magx-magx_off))
	print('magy-magy_off = '+str(magy-magy_off))
	print('magz-magz_off = '+str(magz-magz_off))
	return θ

def calculate_direction(lon2,lat2):
	#--- read GPS data ---#
	try:
		while True:
			GPS_data = GPS.readGPS()
			lat1 = GPS_data[1]
			lon1 = GPS_data[2]
			#print(GPS_data)
			IM920.Send(str(GPS_data))
			#print("lat1 = "+str(lat1))
			#print("lon1 = "+str(lon1))
			#time.sleep(1)
			if lat1 != -1.0 and lat1 != 0.0 :
				break

	except KeyboardInterrupt:
		GPS.closeGPS()
		print("\r\nKeyboard Intruppted, Serial Closed")

	except:
		GPS.closeGPS()
		print (traceback.format_exc())
		
	#--- calculate angle to goal ---#
	direction = gps_navigate.vincenty_inverse(lat1,lon1,lat2,lon2)
	return direction

def rotate_control(θ,azimuth,t_start):
	try:
		timeout_count = time.time()
		while azimuth - 30 > θ  or θ > azimuth + 30:
			if 0 <= azimuth < 30:
				if azimuth - 30 + 360 <= θ <= 360:
					break
			if 330 <= azimuth <= 360:
				if 0 <= θ <= azimuth + 30 - 360:
					break
			if azimuth < 180:
				if azimuth < θ < azimuth + 180:
					run = pwm_control.Run()
					run.turn_right()
					time.sleep(1)
				else: #-- 0 < θ < azimuth or azimuth + 180 < θ < 360 --#
					run = pwm_control.Run()
					run.turn_left()
					time.sleep(1)
			else: #-- 180 < azimuth  --#
				if azimuth - 180 < θ < azimuth:
					run = pwm_control.Run()
					run.turn_left()
					time.sleep(1)
				else: #-- 0 < θ < azimuth - 180 or azimuth < θ < 360 --#
					run = pwm_control.Run()
					run.turn_right()
					time.sleep(1)

			#run = pwm_control.Run()
			#run.stop()
			#time.sleep(0.5)

			get_magdata_average()
			θ = calculate_angle_2D(magx_average,magy_average,magx_off,magy_off)
			Other.saveLog(Calibration_rotate_controlLog, 'Calibration_rotate_control', time.time() - t_start, θ, azimuth)

			if time.time() - timeout_count >= 60:
				print('rotate control timeout')
				break
		print("rotate control finished")
		#print(θ)
			

	except KeyboardInterrupt:
		run = pwm_control.Run()
		run.stop()
		print("faulted to rotate control to goal direction")                
		
	finally:
		run = pwm_control.Run()
		run.stop()

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
		#--- difine goal latitude and longitude ---#
		lon2 = 139.5430
		lat2 = 35.553
		#--- setup ---#
		BMX055.bmx055_setup()
		GPS.openGPS()
		t_start = time.time()
		#------------------ calibration -------------------#
		#--- calculate offset ---#       
		calculate_offset()
		time.sleep(0.1)
		#--- plot data ---#
		plot_data_2D(magx_array,magy_array)
		#plot_data_3D(magx_array,magy_array,magz_array)
		
		#--- calculate θ ---#
		get_data()
		calculate_angle_2D(magx,magy,magx_off,magy_off)
		#calculate_angle_3D(accx,accy,accz,magx,magy,magz,magx_off,magy_off,magz_off)

		direction = calculate_direction(lon2,lat2)
		azimuth = direction["azimuth1"]
		#--- 0 <= azimuth <= 360 ---#
		print('goal azimuth = '+str(azimuth))
		#print('θ = '+str(θ))

		#--- rotate contorol ---#
		rotate_control(θ,azimuth,t_start)
	
	except KeyboardInterrupt:
		print("ERROR")
	
	finally:
		print("End")
		run = pwm_control.Run()
		run.stop()

#------ 修正点 -----#
# rotate cotrol で地磁気センサの平均値を用いるようにした。
# 地磁気センサの値を傾いていることを考慮した補正処理を行った。(get_data)
# rotate control で停止動作をコメントした。
# rotate control のゴールの方位角算出を組み込まなくした。 
#
# 2020/08/26/am0:26
