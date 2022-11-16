#!/usr/bin/python3

import pigpio
import pandas as pd
from matplotlib import pyplot as plt
    
from time import sleep
import sys

import Rosalind_Support_Functions as RSF
from Rosalind_Drive_Functions_2_5_2022 import *


#########
# sETUP #
#########

ip_Address = '10.3.141.1'
pi = pigpio.pi(ip_Address) # Sets up RPi as pigpio object

mux = pi.i2c_open(1, 0x70) # Sets up multiplexer as pigpio object

sensorList = RSF.sensorList
sensor = RSF.setUpSensors(pi, mux, sensorList) # Sets up pigpio objects for each sensor

r1,g1,b1,c1,r2,g2,b2,c2 = RSF.getSensorData(pi, mux, sensorList, sensor)
print(c1,c2)

#############
# VARIABLES #
#############

# The variables I can change

speed = 60     # maximum motor speed
kp = .5
ki = .02
kd = .08
diff = 0
hi1 = 0
low1 = 1000
hi2 = 0
low2 = 1000
zone = True

# calculated variable

    # error variables
error = 0
prevError = 0
totalError = 0

    # PID variables
P = 0
I = 0
D = 0

    # Wheel control variable
LSpeed = 0
RSpeed = 0

    # Sensor variable
sensorData = {}

    # Colors
RED = [0, 255, 255]
GREEN = [255, 0, 255]
YELLOW = [0, 50, 255]


################
# MAIN PROGRAM #
################

key = 1
while key < 10:
    r1,g1,b1,c1,r2,g2,b2,c2 = RSF.getSensorData(pi, mux, sensorList, sensor)
    sensorData[key] = [c1, c2]
    key += 1
    if c1 > hi1:
        hi1 = c1
    if c1 < low1:
        low1 = c1
    if c2 > hi2:
        hi2 = c2
    if c2 < low2:
        low2 = c2


while c1 > 15:
    prevDiff = diff
    r1,g1,b1,c1,r2,g2,b2,c2 = RSF.getSensorData(pi, mux, sensorList, sensor)
    diff = c1 - (c2+2)
    sensorData[key] = [c1, c2]
    key += 1
    if c1 > hi1:
        hi1 = c1
    if c1 < low1:
        low1 = c1
    if c2 > hi2:
        hi2 = c2
    if c2 < low2:
        low2 = c2

    if diff > 10:
        zone = True
    elif diff < -10:
        zone = False
    
    if c1 > 19 and c2 > 18:
        # The actual algorythm part
        prevDiff = diff;
        #P
        P = diff*kp
        #I
        totalError +=  diff
        I = ki*totalError
        #D
        errDiff = diff - prevDiff
        D = kd*errDiff
    
        LSpeed = speed-(P+I+D)
        print(LSpeed)
        RSpeed = speed+(P+I+D)
        print(RSpeed)
    
        if LSpeed < 10:
            LSpeed = 10

        if RSpeed < 10:
            RSpeed = 10

        if LSpeed > 200:
            LSpeed = 200

        if RSpeed > 200:
            RSpeed = 200
        setSpeed(pi, LSpeed, RSpeed)
        print('---------------------------------------')

        if diff > 50 or diff < -50:
            RSF.LED_on(pi, RED)
        elif (diff < 50 and diff > 15) or (diff > -50 and diff < -15):
            RSF.LED_on(pi, YELLOW)
        else:
            RSF.LED_on(pi, GREEN)

    elif zone:
        setSpeed(pi, speed*.75, speed*1.25)
    else:
        setSpeed(pi, speed*1.25, speed*.75)
        

'''
spinRight(pi, speed)

while c1 > 20 or c2 > 20: # When both sensors go low
    r1,g1,b1,c1,r2,g2,b2,c2 = RSF.getSensorData(pi, mux, sensorList, sensor)
    sensorData[key] = [c1, c2]
    key += 1

for i in range(5):  # Keep going for 5 more cycles
    r1,g1,b1,c1,r2,g2,b2,c2 = RSF.getSensorData(pi, mux, sensorList, sensor)
    sensorData[key] = [c1, c2]
    key += 1    

spinLeft(pi, speed)

for i in range(10): # Reverse for 10 cycles to re-engage line
    r1,g1,b1,c1,r2,g2,b2,c2 = RSF.getSensorData(pi, mux, sensorList, sensor)
    sensorData[key] = [c1, c2]
    key += 1

while c1 > 20 or c2 > 20: # When both sensors go low
    r1,g1,b1,c1,r2,g2,b2,c2 = RSF.getSensorData(pi, mux, sensorList, sensor)
    sensorData[key] = [c1, c2]
    key += 1

for i in range(5):  # Keep going for 5 more cycles
    r1,g1,b1,c1,r2,g2,b2,c2 = RSF.getSensorData(pi, mux, sensorList, sensor)
    sensorData[key] = [c1, c2]
    key += 1  

spinRight(pi, speed)

for i in range(10): # Reverse for 10 cycles to re-engage line
    r1,g1,b1,c1,r2,g2,b2,c2 = RSF.getSensorData(pi, mux, sensorList, sensor)
    sensorData[key] = [c1, c2]
    key += 1

while c1 > 20 or c2 > 20: # When both sensors go low
    r1,g1,b1,c1,r2,g2,b2,c2 = RSF.getSensorData(pi, mux, sensorList, sensor)
    sensorData[key] = [c1, c2]
    key += 1

for i in range(5):  # Keep going for 5 more cycles
    r1,g1,b1,c1,r2,g2,b2,c2 = RSF.getSensorData(pi, mux, sensorList, sensor)
    sensorData[key] = [c1, c2]
    key += 1
  '''

stop(pi)
RSF.LED_off(pi)
print(c1,c2)
print(hi1,low1)
print(hi2,low2)
print()
print(sensorData)
                



###################
# SYSTEM SHUTDOWN #
###################

RSF.shutdownSensors(pi, mux, sensorList, sensor)
pi.i2c_close(mux)


data = sensorData
df = pd.DataFrame.from_dict(data, orient='index', columns=['c1', 'c2'])
df


plt.plot(df.c1)
plt.plot(df.c2)
plt.show()


print('All done!')
