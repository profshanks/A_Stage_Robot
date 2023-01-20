import pigpio
import pandas as pd
from matplotlib import pyplot as plt
    
from time import sleep
import sys
import time
import random
import numpy as np

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

c1,c2 = RSF.fastSensorData(pi, mux, sensorList, sensor)
print(c1,c2)

#############
# VARIABLES #
#############

loopTimes = 201

        # Motor variables
speed = 80      # maximum motor speed
cut = .1
topSpeed = 200
threshold = 100
kp = .6

        # Sensor variable
sensorData = {}
hi1 = 0  #the highest
low1 = 1000
hi2 = 0
low2 = 1000

        # time variables
timeData = {}
maxTime = 0
maxAt = 0
minTime = 1000
minAt = 0
timeTot = 0

maxCutTime = 0
maxCutAt = 0
minCutTime = 1000
minCutAt = 0
cutTot = 0

maxSenseTime = 0
maxSenseAt = 0
minSenseTime = 1000
minSenseAt = 0
senseTot = 0

senseTime = 0
setTime = 0


################
# MAIN PROGRAM #
################
key = 1
while key < loopTimes:
    #starting the timer for this run of the algorithm

    start = time.time()
    
    #Setting up the sensor data
    
    c1,c2 = RSF.fastSensorData(pi, mux, sensorList, sensor)
    sensorData[key] = [c1, c2]
    if c1 > hi1:
        hi1 = c1
    if c1 < low1:
        low1 = c1
    if c2 > hi2:
        hi2 = c2
    if c2 < low2:
        low2 = c2
    senseTime = time.time() - start
    
    #The cut algorithm

    if c1 < threshold:
        offBy = threshold - c1
        cut = (threshold-offBy)/threshold
        setSpeed(pi, speed * kp * cut, speed)

    else:
        offBy = c1 - threshold
        cut = (threshold-offBy)/threshold
        
        setSpeed(pi, speed, speed * kp * cut)
    
    cutTime = time.time() - (start+senseTime)
    
    
    # ends the timer for this round
    end = time.time()
    timeVal = end-start
    if  timeVal > maxTime:
        maxTime = timeVal
        maxAt = key
    if  timeVal < minTime:
        minTime = timeVal
        minAt = key

    if  cutTime > maxCutTime:
        maxCutTime = cutTime
        maxCutAt = key
    if  cutTime < minCutTime:
        minCutTime = cutTime
        minCutAt = key

    if  senseTime > maxSenseTime:
        senseTime = senseTime
        maxSenseAt = key
    if  senseTime < minSenseTime:
        minSenseTime = senseTime
        minSenseAt = key

    timeTot += timeVal
    cutTot += cutTime
    senseTot += senseTime
    timeData[key] = [timeVal, senseTime, cutTime]
    key += 1

stop(pi)

#calculate the mean time and cycles per second
meanTime = timeTot/len(timeData)
cyclesPerSecond = 1/meanTime

meanCutTime = cutTot/len(timeData)
cutCyclesPerSecond = 1/meanCutTime

meanSenseTime = senseTot/len(timeData)
senseCyclesPerSecond = 1/meanSenseTime

'''
# prints the graph data
print('--------------- Graph Data ---------------')
print ('last sensor values')
print(c1,c2)
print('hi and low sensor values for sensor 1')
print(hi1,low1)
print('hi and low sensor values for sensor 2')
print(hi2,low2)
#print('all sensor data')
print()
#print(sensorData)
'''

# prints the time data
print('--------------- Overall Time data ---------------')
print (f'hi time value: {maxTime}')
print (f'the max time was on cycle {maxAt}')
print (f'low time value: {minTime}')
print (f'the min time was on cycle {minAt}')
print (f'average time value: {meanTime}')
print (f'cycles per second: {cyclesPerSecond}')
print ('all time data')
print ()

print('--------------- Sensor Time data ---------------')
print (f'hi sensor time value: {maxSenseTime}')
print (f'the max time was on cycle {maxSenseAt}')
print (f'low time value: {minSenseTime}')
print (f'the min time was on cycle {minSenseAt}')
print (f'average time value: {meanSenseTime}')
print (f'cycles per second: {senseCyclesPerSecond}')
print()

print('--------------- Cut Time data ---------------')
print (f'hi sensor time value: {maxCutTime}')
print (f'the max time was on cycle {maxCutAt}')
print (f'low time value: {minCutTime}')
print (f'the min time was on cycle {minCutAt}')
print (f'average time value: {meanCutTime}')
print (f'cycles per second: {cutCyclesPerSecond}')

'''
a = 1
print ('all time data')
while a < loopTimes:
    print (timeData[a])
    a+=1
print ('all time data')
'''

###################
# SYSTEM SHUTDOWN #
###################

RSF.shutdownSensors(pi, mux, sensorList, sensor)
pi.i2c_close(mux)

data = sensorData
df = pd.DataFrame.from_dict(data, orient='index', columns=['c1', 'c2'])

'''
plt.plot(df.c1)
plt.plot(df.c2)
plt.show()
'''
print('All done!')


