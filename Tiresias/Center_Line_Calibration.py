#!/usr/bin/python3

import pigpio

import time
from time import sleep
from time import time
import sys

#import Terry_Support_Functions as TSF
from Terry_Drive_Functions import *
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

def grab_y_data():
    '''This function grabs the y data from both sensors'''
    M1X, M1Y, M1Z = sensor1.magnetic
    M2X, M2Y, M2Z = sensor2.magnetic
    M1Y = round(M1Y, 1)
    M2Y = round(M2Y, 1)
    this_data = (M1Y, M2Y)
    data_log.append(this_data)
    #print(this_data)
    return this_data

################
# MAIN PROGRAM #
################

start_time = time()

speed = 25        # maximum motor speed
cut = 1
threshold = -20
ko = .2
clim = .5
i = 0

loops = 100
data_log = []
s1_high = False
s2_high = False
calibration_run = False

spinRight(pi, speed)
times = []

while True: #Turn left until sensor 2 reads high
    t = time()
    this_data = grab_y_data()
    if this_data[0] < threshold:
        s1_high = True
    if s1_high == True:
        #print('SWITCH')
        for i in range(5):
            this_data = grab_y_data()
        break
    elapsed = time() - t
    times.append(elapsed)

spinLeft(pi, speed)
'''
while True: #Turn right until sensor 1 reads high
    this_data = grab_y_data()
    if this_data[1] < threshold:
        s2_high = True
    if s2_high == True:
        print('SWITCH')
        for i in range(3):
            this_data = grab_y_data()
        break

spinRight(pi, speed)

while True: #Turn left until sensor 2 reads high
    this_data = grab_y_data()
    if this_data[0] < threshold:
        s1_high = True
    if s1_high == True:
        print('SWITCH')
        for i in range(5):
            this_data = grab_y_data()
        break

spinLeft(pi, speed)

while True: #Turn right until sensor 1 reads high
    this_data = grab_y_data()
    if this_data[1] < threshold:
        s2_high = True
    if s2_high == True:
        print('SWITCH')
        for i in range(3):
            this_data = grab_y_data()
        break

spinRight(pi, speed)

while True: #Turn left until sensor 2 reads high
    this_data = grab_y_data()
    if this_data[0] < threshold:
        s1_high = True
    if s1_high == True:
        for i in range(5):
            this_data = grab_y_data()
        break 
'''
stop(pi)
overall_time = time() - start_time
print(f'Total Time: {overall_time}')
print(f'Time log: {times}')

print()
print(len(data_log))
print(data_log)


###################
# SYSTEM SHUTDOWN #
###################

pi.i2c_close(sensor1.i2c_device)
pi.i2c_close(sensor2.i2c_device)


print('All done!')
