#!/usr/bin/python3

import pigpio

import time
from time import sleep
import sys

#import Terry_Support_Functions as TSF
#from Terry_Drive_Functions import *
import adafruit_MLX90393_pigpio as MLX90393


#########
# SETUP #
#########

ip_Address = '10.3.141.139'
pi = pigpio.pi(ip_Address) # Sets up RPi as pigpio object

sensor1 = MLX90393.MLX90393(pi, address=0x0C,
                            gain=MLX90393.GAIN_1X,
                            debug=False)
sensor2 = MLX90393.MLX90393(pi, address=0x0D,
                            gain=MLX90393.GAIN_1X,
                            debug=False)

loops = 3

while loops > 0:
    M1X, M1Y, M1Z = sensor1.magnetic
    M1X = round(M1X, 1)
    M1Y = round(M1Y, 1)
    M1Z = round(M1Z, 1)
    print('SENSOR 1:')
    #print("[{}]".format(time.monotonic()))
    print("X1: {} uT".format(M1X))
    print("Y1: {} uT".format(M1Y))
    print("Z1: {} uT".format(M1Z))
    # Display the status field if an error occured, etc.
    if sensor1.last_status > MLX90393.STATUS_OK:
        sensor1.display_status()
    print()
        
    M2X, M2Y, M2Z = sensor2.magnetic
    M2X = round(M2X, 1)
    M2Y = round(M2Y, 1)
    M2Z = round(M2Z, 1)
    print('SENSOR 2:')
    #print("[{}]".format(time.monotonic()))
    print("X2: {} uT".format(M2X))
    print("Y2: {} uT".format(M2Y))
    print("Z2: {} uT".format(M2Z))
    # Display the status field if an error occured, etc.
    if sensor2.last_status > MLX90393.STATUS_OK:
        sensor2.display_status()
    print()
    print()
    time.sleep(0.5)

    loops -= 1


pi.i2c_close(sensor1.i2c_device)
pi.i2c_close(sensor2.i2c_device)


print('All done!')
