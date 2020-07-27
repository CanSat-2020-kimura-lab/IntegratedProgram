import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')
sys.path.append('/home/pi/git/kimuralab/Detection/Run_phase') 
#--- default module ---#
import time
import traceback
#--- original module ---#
import gps_navigate
import GPS

def stuck_detection1():
	GPS.openGPS()
	try:
		while True:
			value = GPS.readGPS()
			latitude_past = value[1]
			longitude_past = value[2]
			time.sleep(1)
			if latitude_past != -1.0 and longitude_past != 0.0 :
				break
	except KeyboardInterrupt:
		GPS.closeGPS()
		print("\r\nKeyboard Intruppted, Serial Closed")

	except:
		GPS.closeGPS()
		print (traceback.format_exc())
	return longitude_past,latitude_past

def stuck_detection2(longitude_past,latitude_past):
	GPS.openGPS()
	try:
		GPS.openGPS()
		while True:
			value = GPS.readGPS()
			latitude_new = value[1]
			longitude_new = value[2]
			print(value)
			print('longitude = '+str(longitude_new))
			print('latitude = '+str(latitude_new))
			time.sleep(1)
			if latitude_new != -1.0 and longitude_new != 0.0 :
				break
	except KeyboardInterrupt:
		GPS.closeGPS()
		print("\r\nKeyboard Intruppted, Serial Closed")

	except:
		GPS.closeGPS()
		print (traceback.format_exc())
	direction = gps_navigate.vincenty_inverse(longitude_past,latitude_past,longitude_new,latitude_new)
	distance = direction["distance"]        
	return distance

if __name__ == "__main__":
	#--- note GPS data first ---#
	location = stuck_detection1()
	longitude_past = location[0]
	latitude_past = location[1]
	print('longitude_past = '+str(longitude_past))
	print('latitude_past = '+str(latitude_past))
	#--- Keyboard input ---#
	while True:
		print()
		print('GPSを取得したい場合は、"aaa"と入力してください')
		print('終了する場合は"end"と入力してください')
		input_data = input()
		print()
		if input_data == 'aaa':
			try:
				#--- compare GPS data and calcurate distance ---#
				distance = stuck_detection2(longitude_past,latitude_past)
				print('distance = '+str(distance))
				if distance >= 5:
					print("rover moved!")                           
				else:
					#--- if rover didn't move 5m,carry out stuck cofirm ---#
					print("There's a possibility that rover has stucked")

			except KeyboardInterrupt:
				print('stop')
				break

		elif input_data == 'end'or'End':
			print('End')
			break
		else:
			print()
			print('Fault')
			break
