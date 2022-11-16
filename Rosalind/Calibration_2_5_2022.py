#!/usr/bin/python3

import pigpio
import pandas as pd
from matplotlib import pyplot as plt
    
from time import sleep
import sys

import Rosalind_Support_Functions as RSF
from Rosalind_Drive_Functions import *


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

speed = 60        # maximum motor speed
cut = 1
threshold = 70
ko = .2
clim = .5
i = 0
diff = 0

sensorData = {}

################
# MAIN PROGRAM #
################

key = 1

spinRight(pi, speed)

while c1 > 20 or c2 > 20: # When both sensors go low
    r1,g1,b1,c1,r2,g2,b2,c2 = RSF.getSensorData(pi, mux, sensorList, sensor)
    diff = c1 - c2
    sensorData[key] = [c1, c2, diff]
    key += 1

for i in range(5):  # Keep going for 5 more cycles
    r1,g1,b1,c1,r2,g2,b2,c2 = RSF.getSensorData(pi, mux, sensorList, sensor)
    diff = c1 - c2
    sensorData[key] = [c1, c2, diff]
    key += 1    

spinLeft(pi, speed)

for i in range(10): # Reverse for 10 cycles to re-engage line
    r1,g1,b1,c1,r2,g2,b2,c2 = RSF.getSensorData(pi, mux, sensorList, sensor)
    diff = c1 - c2
    sensorData[key] = [c1, c2, diff]
    key += 1

while c1 > 20 or c2 > 20: # When both sensors go low
    r1,g1,b1,c1,r2,g2,b2,c2 = RSF.getSensorData(pi, mux, sensorList, sensor)
    diff = c1 - c2
    sensorData[key] = [c1, c2, diff]
    key += 1

for i in range(5):  # Keep going for 5 more cycles
    r1,g1,b1,c1,r2,g2,b2,c2 = RSF.getSensorData(pi, mux, sensorList, sensor)
    diff = c1 - c2
    sensorData[key] = [c1, c2, diff]
    key += 1  

spinRight(pi, speed)

for i in range(10): # Reverse for 10 cycles to re-engage line
    r1,g1,b1,c1,r2,g2,b2,c2 = RSF.getSensorData(pi, mux, sensorList, sensor)
    diff = c1 - c2
    sensorData[key] = [c1, c2, diff]
    key += 1

while c1 > 20 or c2 > 20: # When both sensors go low
    r1,g1,b1,c1,r2,g2,b2,c2 = RSF.getSensorData(pi, mux, sensorList, sensor)
    diff = c1 - c2
    sensorData[key] = [c1, c2, diff]
    key += 1

for i in range(5):  # Keep going for 5 more cycles
    r1,g1,b1,c1,r2,g2,b2,c2 = RSF.getSensorData(pi, mux, sensorList, sensor)
    diff = c1 - c2
    sensorData[key] = [c1, c2, diff]
    key += 1
    
stop(pi)
print(c1,c2)
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
