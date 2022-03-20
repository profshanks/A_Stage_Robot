#########################
#                       #
#       SenseTest       #
#                       #
#########################

import time
from time import sleep
import sys
import struct

import pigpio

#################
# System Set-Up #
#################

# Sensor Variables
COMMAND = 0x80
ATIME = 0x01
ITIME = 0xFF
GAIN = 0x01
CONTROL = 0x0F
ENABLE = 0x00
ENABLE_AEN = 0x02
ENABLE_PON = 0x01

#sensorList = [4, 8, 16, 32]
sensorList = [4, 8, 16 ,32]
colorRegisters = [0x16, 0x18, 0x1A, 0x14]

# Set up PIGPIO connection & multiplexer
pi = pigpio.pi('10.3.141.163')
mux = pi.i2c_open(1, 0x77)
print('Mux: ' + str(mux))

# This gets the sensors rolling...
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

#############
# Functions #
#############

def getSensorData():
    """ Pulls sensor data from the registers on the chip.

        Returns a list ('data') with readings for r/g/b/c on all
                three sensors.

        data[0] = r1    data[4] = r2    data[8] = r3    data[12] = r4
        data[1] = g1    data[5] = g2    data[9] = g3    data[13] = g4
        data[2] = b1    data[6] = b2    data[10] = b3   data[14] = b4
        data[3] = c1    data[7] = c2    data[11] = c3   data[15] = c4
        """
    data = []
    for s in sensorList:
        pi.i2c_write_byte(mux, s)
        for reg in colorRegisters:
            (c, d) = pi.i2c_read_i2c_block_data(sensor,
                                                (COMMAND | reg), 2)
            #print(c, d)
            neat = struct.unpack('H'*1, d)
            data.append(neat[0])
    return data


################
# MAIN PROGRAM #
################

c = 3

data = getSensorData()
#print(data)
print(data[c], data[c+4], data[c+8], data[c+12])



###################
# System Shutdown #
###################

# Put the sensor chips back to low power sleep/disabled.
for sen in sensorList:
    pi.i2c_write_byte(mux, sen)
    pi.i2c_close(sensor)
    sensor -=1

#tcs4.disable()

pi.i2c_close(mux)
