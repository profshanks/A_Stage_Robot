import pigpio
import pandas as pd
from matplotlib import pyplot as plt
    
from time import sleep
import sys
import time
import random

import Rosalind_Support_Functions as RSF
from Rosalind_Drive_Functions import *


#########
# sETUP #
#########

ip_Address = '10.3.141.1'
pi = pigpio.pi(ip_Address) # Sets up RPi as pigpio object

# mux = pi.i2c_open(1, 0x70) # Sets up multiplexer as pigpio object

#sensorList = RSF.sensorList
#sensor = RSF.setUpSensors(pi, mux, sensorList) # Sets up pigpio objects for each sensor

#r1,g1,b1,c1,r2,g2,b2,c2 = RSF.getSensorData(pi, mux, sensorList, sensor)
#print(c1,c2)

#############
# VARIABLES #
#############

speed = 100      # maximum motor speed
cut = 1
threshold = 70
ko = .2
clim = .5
i = 0
n = 0


RED = [0, 255, 255]
GREEN = [255, 0, 255]
BLUE = [255, 255, 0]
YELLOW = [0, 50, 255]
ORANGE = [0, 200, 255]
PURPLE = [225, 255, 0]
WHITE = [0, 0, 0]
TEST = [255, 255, 150]

arr = [RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, WHITE]
#sensorData = {}

################
# MAIN PROGRAM #
################

for x in range(255):
    TEST = [0, n, n]
    RSF.LED_on(pi, TEST)
    n+=1

RSF.LED_off(pi)

stop(pi)

print('All Done!')






