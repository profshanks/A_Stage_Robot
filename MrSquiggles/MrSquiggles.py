#########################
#                       #
#     MrSquiggles       #
#      profshanks       #
#  Started: 01.13.2020  #
#                       #
#########################

import time
from time import sleep
import sys

import pigpio

from Squiggles_FunVar import *


#################
# System Set-Up #
#################

# Set up PIGPIO connection & multiplexer
pi = pigpio.pi('10.3.141.1')
mux = pi.i2c_open(1, 0x77)
print('Mux: ' + str(mux))

# Set up the 4 sensors
for sen in sensorList:
    pi.i2c_write_byte(mux, sen)
    sensor= pi.i2c_open(1, 0x29)

    # Set Integration Time
    pi.i2c_write_byte_data(sensor, (COMMAND | ATIME), ITIME)

    # Set Gain
    pi.i2c_write_byte_data(sensor, (COMMAND | CONTROL), GAIN)

    # Enable sensor
    pi.i2c_write_byte_data(sensor, (COMMAND | ENABLE), ENABLE_PON)
    time.sleep(0.01)
    pi.i2c_write_byte_data(sensor, (COMMAND | ENABLE), (ENABLE_PON | ENABLE_AEN))

# Set up variables for Motor Driver Hat
M2Sp = 13		        # Set pwm2 pin on MD10-Hat
M1Sp = 12			# Set pwm1 pin on MD10-hat
M2Dir = 24			# Set dir2 pin on MD10-Hat
M1Dir = 26			# Set dir1 pin on MD10-Hat



################
# MAIN PROGRAM #
################

topSpeed = 80  # Speed values range from 0-255.
lowSpeed = 35
c = 3
''' Which sensor are we listening to?
           (0=red; 1=green; 2=blue; 3=clear)
'''

pi.write(M1Dir, 0) # Sets motor direction 0=fwd, 1=rev
pi.write(M2Dir, 0)

while True:
    data = getSensorData(pi, mux, sensor)
    print(data[c], data[c+4], data[c+8], data[c+12])
    allPhotons = (data[c] + data[c+4] + data[c+8] + data[c+12])

    if allPhotons < 200: # Check for "Lost" condition (no tape detected)
        pi.set_PWM_dutycycle(M1Sp, 0)
        pi.set_PWM_dutycycle(M2Sp, 0)
        print("I'm lost!")

        for sen in sensorList:  # Shut down i2c objects
            pi.i2c_write_byte(mux, sen)
            pi.i2c_close(sensor)
            sensor -=1
        pi.i2c_close(mux)
        sys.exit()  # Quit program

    if data[c+12] < 80:
        pi.set_PWM_dutycycle(M1Sp, lowSpeed)
        pi.set_PWM_dutycycle(M2Sp, topSpeed)

    else:
        pi.set_PWM_dutycycle(M1Sp, topSpeed)
        pi.set_PWM_dutycycle(M2Sp, lowSpeed)
