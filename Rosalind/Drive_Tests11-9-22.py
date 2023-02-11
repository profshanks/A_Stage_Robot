import pigpio
import pandas as pd
from matplotlib import pyplot as plt
    
from time import sleep
import sys
import time
import random

import Rosalind_Support_Functions as RSF
from Rosalind_Drive_Functions_2_5_2022 import *


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

speed = 50      # maximum motor speed
n = 0

################
# MAIN PROGRAM #
################

for x in range(500):
    Forward(pi, n*.5)
    print(n)
    n+=1

stop(pi)

print('All Done!')






