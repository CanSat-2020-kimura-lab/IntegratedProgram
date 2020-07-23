import time 
import pigpio
from threading import Thread

#-- GPIO connection --#
Ena1 = 13
Pha1 = 19
Ena2 = 12
Pha2 = 25
LARGE = 10
MODE = 9
STBY = 11

pi = pigpio.pi()

#-- Set the GPIO_mode --#
pi.set_mode(Ena1, pigpio.OUTPUT)
pi.set_mode(Pha1,pigpio.OUTPUT)
pi.set_mode(Ena2, pigpio.OUTPUT)
pi.set_mode(Pha2,pigpio.OUTPUT)
pi.set_mode(MODE,pigpio.OUTPUT)
pi.set_mode(LARGE,pigpio.OUTPUT)
pi.set_mode(STBY,pigpio.OUTPUT)

#-- frequency --#
freq = 50
#-- frequency range --#
range =255   # 25 ~ 40000

pi.set_PWM_frequency(Ena1,freq)
pi.set_PWM_frequency(Pha1,freq)
pi.set_PWM_frequency(Ena2,freq)
pi.set_PWM_frequency(Pha2,freq)

pi.set_PWM_range(Ena1,range)
pi.set_PWM_range(Pha1,range)
pi.set_PWM_range(Ena2,range)
pi.set_PWM_range(Pha2,range)

#--- motor mode control definition ---#
def setup_mode(a,b,c):
        pi.write(MODE,a)
        pi.write(LARGE,b)
        pi.write(STBY,c)

def setup_IN(d,e,f,g,t):
        pi.write(Ena1,d)
        pi.write(Pha1,e)
        pi.write(Ena2,f)
        pi.write(Pha2,g)
        time.sleep(t)

def straight_h():
        d = 255
        setup_mode(1,0,1)

        pi.set_PWM_dutycycle(Ena1, d)
        pi.set_PWM_dutycycle(Pha1, d)
        pi.set_PWM_dutycycle(Ena2, d)
        pi.set_PWM_dutycycle(Pha2, d)

def stop():
        setup_mode(1,0,1)
        setup_IN(0,0,0,0,1.0)

if __name__ == "__main__":
        try:
                straight_h()
                #time.sleep(1)
        
        except KeyboardInterrupt:
                stop()
        '''        
        finally:
                stop()
        '''
