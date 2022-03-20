#!/usr/bin/python3

import pigpio

import time
from time import sleep
import sys

#import Terry_Support_Functions as TSF
from Terry_Drive_Functions import *
import adafruit_MLX90393_pigpio as MLX90393


#########
# SETUP #
#########

print('Setting up...')
ip_Address = '10.3.141.139'
pi = pigpio.pi(ip_Address) # Sets up RPi as pigpio object

sensor1 = MLX90393.MLX90393(pi, address=0x0C,
                            gain=MLX90393.GAIN_1X,
                            debug=False)
'''
sensor2 = MLX90393.MLX90393(pi, address=0x0D,
                            gain=MLX90393.GAIN_1X,
                            debug=False)
'''


################
# MAIN PROGRAM #
################

speed = 30         # maximum motor speed
cut = .2
threshold = -70
data = []

loops = 50

print('Starting loops...')
while loops > 0:
    M1X, M1Y, M1Z = sensor1.magnetic
    M1X = round(M1X, 1)
    data.append(M1X)
    '''
    # This is the super-squiggly algorithm
    if M1X > threshold:
        pi.set_PWM_dutycycle(M1Sp, speed * cut)  # Turn right
        pi.set_PWM_dutycycle(M2Sp, speed)

    else:
        pi.set_PWM_dutycycle(M1Sp, speed)        # Turn left
        pi.set_PWM_dutycycle(M2Sp, speed * cut)
    '''
    loops -= 1

stop(pi)

print(data)


###################
# SYSTEM SHUTDOWN #
###################
try:
    pi.i2c_close(sensor1.i2c_device)
    #pi.i2c_close(sensor2.i2c_device)
except:
    pass

print('All done!')
