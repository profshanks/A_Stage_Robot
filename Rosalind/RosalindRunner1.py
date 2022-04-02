#!/usr/bin/python3

try:
    import pigpio
except:
    import pip
    pip.main(['install', 'pigpio'])
    
from time import sleep
import sys

import Rosalind_Support_Functions as RSF
from Rosalind_Drive_Functions import *


#########
# sETUP #
#########

ip_Address = '10.3.141.249'
pi = pigpio.pi(ip_Address) # Sets up RPi as pigpio object

mux = pi.i2c_open(1, 0x70) # Sets up multiplexer as pigpio object

sensorList = RSF.sensorList
sensor = RSF.setUpSensors(pi, mux, sensorList) # Sets up pigpio objects for each sensor

r1,g1,b1,c1,r2,g2,b2,c2 = RSF.getSensorData(pi, mux, sensorList, sensor)
print(r1,g1,b1,c1,r2,g2,b2,c2)


################
# MAIN PROGRAM #
################

speed = 100         # maximum motor speed
cut = 1
threshold = 70
ko = .2
clim = .5
i = 0

#RSF.LED_on(pi, RSF.RED)
#sleep(1)
#RSF.LED_off(pi)
#sleep(0.1)
RSF.LED_on(pi, RSF.RED, intensity=10)
sleep(1)
RSF.LED_off(pi)
sleep(0.1)
RSF.LED_on(pi, RSF.ORANGE, intensity=10)
sleep(1)
RSF.LED_off(pi)
sleep(0.1)
RSF.LED_on(pi, RSF.YELLOW, intensity=10)
sleep(1)
RSF.LED_off(pi)
sleep(0.1)
RSF.LED_on(pi, RSF.GREEN, intensity=10)
sleep(1)
RSF.LED_off(pi)
sleep(0.1)
RSF.LED_on(pi, RSF.BLUE, intensity=10)
sleep(1)
RSF.LED_off(pi)
sleep(0.1)
RSF.LED_on(pi, RSF.PURPLE, intensity=10)
sleep(1)
RSF.LED_off(pi)
sleep(0.1)

'''
#RSF.LED_on(pi, RSF.GREEN)
sleep(0.5)
RSF.LED_on(pi, RSF.GREEN, intensity=50)
sleep(0.5)
RSF.LED_off(pi)
sleep(0.5)

#RSF.LED_on(pi, RSF.BLUE)
sleep(0.5)
RSF.LED_on(pi, RSF.BLUE, intensity=50)
sleep(0.5)
RSF.LED_off(pi)
sleep(0.5)

'''
###################
# SYSTEM SHUTDOWN #
###################

RSF.shutdownSensors(pi, mux, sensorList, sensor)
pi.i2c_close(mux)

print('All done!')
