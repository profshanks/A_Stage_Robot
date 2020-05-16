#########################
#                       #
#    Line Clamp 1.6     #
#      profshanks       #
#  Started: 08.04.2018  #
#  This Version: 11/12  #
#  Useful:              #
#                       #
#########################

import time
from time import sleep
import sys
import struct

import pigpio

start8 = time.time()


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
'''
def calibrateSensors(color='clear'):
    """ Calibrates sensors by running the sensor array back and forth
        across the line. Also centers the array over the line.

        The color to be followed (red/green/blue/clear) can be set by
        keyword; 'color=clear' is the default.

        Returns the hi/lo values for each sensor and the number of times
        the data is pulled from the sensor array.
        """
    low = 200
    mid = 400
    speed = 160
    hiVals = [0,0,0,0,0,0,0,0,0,0,0,0]
    loVals = [50,50,50,50,50,50,50,50,50,50,50,50]
    tests = 0
    if color == 'red':
        c = 0
    elif color == 'green':
        c = 1
    elif color == 'blue':
        c = 2
    else:
        c = 3
    data = getSensorData()
    tests += 1
    
    # Move to the left side of the line...
    while data[c] < mid:
        print(data[c], data[c+4], data[c+8])
        pi.write(M1Dir, 0)
        pi.write(M2Dir, 1)
        pi.set_PWM_dutycycle(M1Sp, speed)
        pi.set_PWM_dutycycle(M2Sp, speed)
        data = getSensorData()
        tests += 1
    while data[c] > low or data[c+4] > low or data[c+8] > low:
        print(data[c], data[c+4], data[c+8])
        pi.write(M1Dir, 0)
        pi.write(M2Dir, 1)
        pi.set_PWM_dutycycle(M1Sp, speed)
        pi.set_PWM_dutycycle(M2Sp, speed)
        data = getSensorData()
        tests += 1
    print(data[c], data[c+4], data[c+8])
    print("On the Left")
    pi.set_PWM_dutycycle(M1Sp, 0)
    pi.set_PWM_dutycycle(M2Sp, 0)
    sleep(1)
    
    
    # Move array right to find the line.
    while data[c] < mid:
        pi.write(M1Dir, 1)
        pi.write(M2Dir, 0)
        pi.set_PWM_dutycycle(M1Sp, speed)
        pi.set_PWM_dutycycle(M2Sp, speed)
        data = getSensorData()
        tests += 1
        for i in range(0,12):
            if data[i] > hiVals[i]:
                hiVals[i] = data[i]
            if data[i] < loVals[i]:
                loVals[i] = data[i]

    # Move array fully to right side of the line.
    while data[c] > low or data[c+4] > low or data[c+8] > low:
        pi.set_PWM_dutycycle(M1Sp, speed)
        pi.set_PWM_dutycycle(M2Sp, speed)
        data = getSensorData()
        tests += 1
        for i in range(0,12):
            if data[i] > hiVals[i]:
                hiVals[i] = data[i]
            if data[i] < loVals[i]:
                loVals[i] = data[i]
    pi.set_PWM_dutycycle(M1Sp, 0)
    pi.set_PWM_dutycycle(M2Sp, 0)
    sleep(1)
    
    # Balance left and right sensors
    variance = loVals[c] - loVals[c+8] 
    
    # Start heading left again until centered.           
    while data[c] < (hiVals[c]/2): 
        pi.write(M1Dir, 0)
        pi.write(M2Dir, 1)
        pi.set_PWM_dutycycle(M1Sp, speed*.75)
        pi.set_PWM_dutycycle(M2Sp, speed*.75)
        data = getSensorData()
        tests += 1
    while True:
        if data[c] <= (data[c+8] + variance):
            pi.set_PWM_dutycycle(M1Sp, 0)
            pi.set_PWM_dutycycle(M2Sp, 0)
            return hiVals, loVals, tests
        elif data[c] and data[c+4] and data[c+8] < (loVals[c] + 10):
            print("Calibration sequence failed. Line center not found. Program ending... :(")
            sys.exit()
'''
def driveForward(hiVals, loVals, topSpeed, color='clear'):
    """ Drive forward while "clamped" to the tape line. Runs until stop
        signal is encountered.
        """
    iSawRed = False
    eTotal = 0
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
    variance = 5
    #variance = loVals[c] - loVals[c+8]
    kp = 1.2
    ki = 0
    kd = 0
    sumOfErr = 0
    lastErr = 0
    start = time.time()
    data = getSensorData()
    end = time.time()
    elapsed = round((end-start), 5)
    print('That function took ' + str(elapsed) + ' seconds!')
    eTotal =  elapsed
    print(data[c+12], data[c+8], data[c+4], data[c])
    total = (data[c] + data[c+4] + data[c+8] + data[c+12])
    i = 1
    elapsed = 0
    
    while ((data[0] < (data[1]*2.5)) & (data[4] < (data[5]*2.5)) &
           (data[8] < (data[9]*2.5)) & (data[12] < (data[13]*2.5))):
        iSawRed = False
        if total < 250:
            print('I am lost...')
            print(data[c+12], data[c+8], data[c+4], data[c])
            break
        elif data[c] > (data[c+4]*2): # Too far right; make a hard left!
            print('Hard left!')
            print(data[c+12], data[c+8], data[c+4], data[c])
            #print(i)
            while data[c+4] < (hiVals * .8):
                pi.set_PWM_dutycycle(M2Sp, 0)
                pi.set_PWM_dutycycle(M1Sp, (topSpeed * .8))
                start = time.time()
                data = getSensorData()
                end = time.time()
                elapsed = round((end-start), 5)
                eTotal += elapsed
                print('That function took ' + str(elapsed) + ' seconds!')
                total = (data[c] + data[c+4] + data[c+8] + data[c+12])
                if total < 250:
                    print('I am lost...')
                    print(data[c+12], data[c+8], data[c+4], data[c])
                    break
                i += 1
            #print(i)
        elif data[c+12] > (data[c+8]*2): # Too far left; make a hard right!
            print('Hard right!')
            print(data[c+12], data[c+8], data[c+4], data[c])
            #print(i)
            while data[c+8] < (hiVals * .8):
                pi.set_PWM_dutycycle(M2Sp, (topSpeed * .8))
                pi.set_PWM_dutycycle(M1Sp, 0)
                start = time.time()
                data = getSensorData()
                end = time.time()
                elapsed = round((end-start), 5)
                eTotal += elapsed
                print('That function took ' + str(elapsed) + ' seconds!')
                total = (data[c] + data[c+4] + data[c+8] + data[c+12])
                if total < 250:
                    print('I am lost...')
                    print(data[c+12], data[c+8], data[c+4], data[c])
                    break
                i += 1
            #print(i)
        else:
            error = data[c+4] - data[c+8]
            #print('Error: ' + str(error))
            proportion = abs(error/hiV) * kp
            #print('Proportion: ' + str(proportion))
            turn = topSpeed-proportion
            if turn < 0:
                turn = 0
            elif turn > 255:
                turn=255
            #print('Turn: ' + str(turn))
          
            if error > 0: # A little too far right; proportional turn left
                #print('Left...')
                pi.set_PWM_dutycycle(M2Sp, turn)
                pi.set_PWM_dutycycle(M1Sp, topSpeed)
            else: # A little too far left; proportional turn right
                #print('Right...')
                pi.set_PWM_dutycycle(M2Sp, topSpeed)
                pi.set_PWM_dutycycle(M1Sp, turn)
                
                
        start = time.time()
        data = getSensorData()
        end = time.time()
        elapsed = round((end-start), 5)
        eTotal += elapsed
        print('That function took ' + str(elapsed) + ' seconds!')
        
        total = (data[c] + data[c+4] + data[c+8] + data[c+12])
        #print(total)
        i += 1
        iSawRed = True
    pi.set_PWM_dutycycle(M1Sp, 0)
    pi.set_PWM_dutycycle(M2Sp, 0)
    print(total)
    if iSawRed == True:
        print('I saw RED!')
    print('I stopped!')
    print(data[c+12], data[c+8], data[c+4], data[c])
    print('We read the sensors ' + str(i) + ' times!')
    eAverage = round((eTotal/i), 5)
    print('The average time to read the sensors was ' + str(eAverage) + ' seconds.')
    
    return eTotal                 
    '''
    while data[4] < (data[6]*1.5): # Looking out for red tape signal
        # Calculate centering error & turn correction via PID method.
        
        error = abs(data[c] - data[c+8])
        proportional = error * kp
        integral = sumOfErr * ki
        differential = lastErr * kd
        pid = int(proportional + differential)              # Just PD control
        #pid = int(proportional + integral + differential)   # Full PID
        sumOfErr += error
        error = lastErr
        turn = topSpeed - pid
        if turn <= 0:
            turn = 0

        # Make speed adjustments.
        if data[c] > data[c+8]: # Need to adjust left.
            pi.set_PWM_dutycycle(M1Sp, topSpeed)
            pi.set_PWM_dutycycle(M2Sp, turn)
        else:
            pi.set_PWM_dutycycle(M1Sp, turn)
            pi.set_PWM_dutycycle(M2Sp, topSpeed)
            
        data = getSensorData()
    '''
    

    
################
# MAIN PROGRAM #
################

topSpeed = 180  # Speed values range from 0-255.
hiV = 250
col = 'clear'   # Color options include 'red'/'green'/'blue'/'clear'.
c = 3

#(hiV,loV,tests) = calibrateSensors(color=col)
#print(tests)
#driveForward(hiV,loV,topSpeed,color=col)
eTotal = driveForward(hiV, 60, topSpeed)

data = getSensorData()
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
'''
end8 = time.time()
elapsed8 = round((end8-start8), 1)
sensorTime = round(((eTotal/elapsed8)*100), 1)
print('That run took ' + str(elapsed8) + ' seconds!')
print(str(sensorTime) + '% of that time was spent reading the sensors.')
'''
