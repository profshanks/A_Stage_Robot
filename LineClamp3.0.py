#########################
#                       #
#    Line Clamp 3.0     #
#      profshanks       #
#  Started: 9/28/19     #
#  Updated: 9/28/19     #
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
pi = pigpio.pi('10.3.141.1')
mux = pi.i2c_open(1, 0x77)
print('Mux: ' + str(mux))

# Set the multiplexer channels for the different sensors. 
    # For channel 0 use "1"         # For channel 4 use "16"
    # For channel 1 use "2"         # For channel 5 use "32"
    # For channel 2 use "4"         # For channel 6 use "64"
    # For channel 3 use "8"         # For channel 7 use "128"
'''
sensor_1 = 4 
sensor_2 = 8
sensor_3 = 16
sensor_4 = 32
'''
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

# Set up variables for Motor Driver Hat
M2Sp = 13		        # Set pwm2 pin on MD10-Hat
M1Sp = 12			# Set pwm1 pin on MD10-hat
M2Dir = 24			# Set dir2 pin on MD10-Hat
M1Dir = 26			# Set dir1 pin on MD10-Hat

Min = 50                        # Set minimum motor speed
Max = 255                       # Set maximum motor speed


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

def driveForward(topSpeed, color='clear'):
    """ Drive forward while "clamped" to the tape line. Runs until stop
        signal is encountered.
        """

    kp = 1  # 
    hiV = 240
    
    print('Drive Forward')
    #  Establish Motor Direction (0 = Forward; 1 = Reverse)
    pi.write(M1Dir, 0)
    pi.write(M2Dir, 0)
    
    if color == 'red':
        c = 0
    elif color == 'green':
        c = 1
    elif color == 'blue':
        c = 2
    else:
        c = 3

    data = getSensorData()
    print(data[c+12], data[c+8], data[c+4], data[c])
    total = (data[c] + data[c+4] + data[c+8] + data[c+12])
    print('total: ' + str(total))
    global turnLow
    global turnHigh

    #while (total > 250):
    for i in range(0, 20):
        if total < 250:  # Not over the line at all
            print('I am lost...')
            print(data[c+12], data[c+8], data[c+4], data[c])
            break
        
        elif data[c] > (data[c+4*2]): # Too far right; make a hard left!
            print('Hard left!')
            while (data[c]*2) > data[c+4]:
                pi.set_PWM_dutycycle(M2Sp, 0)
                pi.set_PWM_dutycycle(M1Sp, (topSpeed * .8))
                
                data = getSensorData()
                print(data[c+12], data[c+8], data[c+4], data[c])
                total = (data[c] + data[c+4] + data[c+8] + data[c+12])
                if total < 250:
                    break

        elif data[c+12] > (data[c+8]*2): # Too far left; make a hard right!
            print('Hard right!')
            while (data[c+12]*2) > data[c+8]:
                pi.set_PWM_dutycycle(M2Sp, (topSpeed * .8))
                pi.set_PWM_dutycycle(M1Sp, 0)
                
                data = getSensorData()
                print(data[c+12], data[c+8], data[c+4], data[c])
                total = (data[c] + data[c+4] + data[c+8] + data[c+12])
                if total < 250:
                    break

        else:
            error = (data[c]+ data[c+4]) - (data[c+8] + data[c+12])
            print('error: ' + str(error))
            foo = error/hiV
            print('foo: ' + str(foo))
            bar = abs(foo)
            print('bar: ' + str(bar))
            proportion = int(bar * kp)
            print('proportion: ' + str(proportion))
            turn = topSpeed-proportion
            print('turn: ' + str(turn))

            if turn < 0:
                turn = 0
            elif turn > hiV:
                turn=hiV
            if turn < turnLow:
                turnLow = turn
            if turn > turnHigh:
                turnHigh = turn

            if error > 0: # A little too far right; proportional turn left
                print('Left...')
                pi.set_PWM_dutycycle(M2Sp, turn)
                pi.set_PWM_dutycycle(M1Sp, topSpeed)
            else: # A little too far left; proportional turn right
                print('Right...')
                pi.set_PWM_dutycycle(M2Sp, topSpeed)
                pi.set_PWM_dutycycle(M1Sp, turn)
            
        data = getSensorData()
        print(data[c+12], data[c+8], data[c+4], data[c])
        total = (data[c] + data[c+4] + data[c+8] + data[c+12])
    
    print('I am so lost...')
    print(data[c+12], data[c+8], data[c+4], data[c])
    pi.set_PWM_dutycycle(M1Sp, 0)
    pi.set_PWM_dutycycle(M2Sp, 0)

    

################
# MAIN PROGRAM #
################

topSpeed = 80  # Speed values range from 0-255.

col = 'clear'   # Color options include 'red'/'green'/'blue'/'clear'.
c = 3

turnLow = 255
turnHigh = 0

#(hiV,loV,tests) = calibrateSensors(color=col)
#print(tests)
#driveForward(hiV,loV,topSpeed,color=col)
#eTotal = driveForward(hiV, 60, topSpeed)
driveForward(topSpeed)

data = getSensorData()
print(data[c], data[c+4], data[c+8], data[c+12])

print('Lowest turn value: ' + str(turnLow))
print('Highest turn value: ' + str(turnHigh))



###################
# System Shutdown #
###################

# Put the sensor chips back to low power sleep/disabled.
for sen in sensorList:
    pi.i2c_write_byte(mux, sen)
    pi.i2c_close(sensor)
    sensor -=1

pi.i2c_close(mux)
