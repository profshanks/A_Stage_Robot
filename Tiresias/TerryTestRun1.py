#!/usr/bin/python3

import pigpio

import time
from time import sleep
import sys

#import Terry_Support_Functions as TSF
#from Terry_Drive_Functions import *
import adafruit_MLX90393_pigpio as MLX90393


#########
# sETUP #
#########

ip_Address = '10.3.141.139'
pi = pigpio.pi(ip_Address) # Sets up RPi as pigpio object

#sen1 = pi.i2c_open(1, 0x0c) # Sets up sensor as pigpio object
#sen2 = pi.i2c_open(1, 0x0d) # Sets up sensor as pigpio object

sensor1 = MLX90393.MLX90393(pi, address=0x0C,
                            gain=MLX90393.GAIN_1X,
                            debug=False)
sensor2 = MLX90393.MLX90393(pi, address=0x0D,
                            gain=MLX90393.GAIN_1X,
                            debug=False)

while True:
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
    time.sleep(3.0)


'''
r1,g1,b1,c1,r2,g2,b2,c2 = TSF.getSensorData(pi, mux, sensorList, sensor)
print(r1,g1,b1,c1,r2,g2,b2,c2)
'''

################
# MAIN PROGRAM #
################

speed = 100         # maximum motor speed
cut = 1
threshold = 70
ko = .2
clim = .5
i = 0
'''
spinRight(pi, 50)
sleep(2)
spinLeft(pi,50)
sleep(2)
stop(pi)
'''

###################
# SYSTEM SHUTDOWN #
###################
'''
TSF.shutdownSensors(pi, mux, sensorList, sensor)
'''
pi.i2c_close(sensor1.i2c_device)
#pi.i2c_close(sensor2)


print('All done!')
