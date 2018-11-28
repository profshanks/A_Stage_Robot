#########################
#                       #
#    Line Clamp 2.0     #
#      profshanks       #
#  Started: 08.04.2018  #
#  This Version: 10/30  #
#  Useful:              #
#                       #
#########################

import time
import sys
from time import sleep
import pigpio
import readTCS34725 as TCS
print('Done importing!')


#################
# System Set-Up #
#################
start8 = time.time()
pi = pigpio.pi('10.3.141.1')    # Define remote RPi
mux = pi.i2c_open(1, 0x77)      # Define multiplexer (Adafruit TCA9548A)
print('Mux: ' + str(mux))

# Set the multiplexer channels for the different sensors. 
    # For channel 0 use "1"         # For channel 4 use "16"
    # For channel 1 use "2"         # For channel 5 use "32"
    # For channel 2 use "4"         # For channel 6 use "64"
    # For channel 3 use "8"         # For channel 7 use "128"

sensor_1 = 4 
sensor_2 = 8
sensor_3 = 16
sensor_4 = 32

# Create separate objects for each sensor.
pi.i2c_write_byte(mux, sensor_1)
tcs1 = TCS.TCS34725()

pi.i2c_write_byte(mux, sensor_2)
tcs2 = TCS.TCS34725()

pi.i2c_write_byte(mux, sensor_3)
tcs3 = TCS.TCS34725()

pi.i2c_write_byte(mux, sensor_4)
tcs4 = TCS.TCS34725()

M2Sp = 13		        # Set pwm2 pin on MD10-Hat
M1Sp = 12			# Set pwm1 pin on MD10-hat
M2Dir = 24			# Set dir2 pin on MD10-Hat
M1Dir = 26			# Set dir1 pin on MD10-Hat

Min = 50                        # Set minimum motor speed
Max = 255                       # Set maximum motor speed



#############
# Functions #
#############

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
    elapsed = 0
    eTotal = 0
    pi.write(M1Dir, 1)
    pi.write(M2Dir, 1)
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
    kp = topSpeed * .5
    ki = 0
    kd = 0
    sumOfErr = 0
    lastErr = 0
    start = time.time()
    data = TCS.getSensorData(pi, tcs1, tcs2, tcs3, tcs4, mux,
                  sensor_1, sensor_2, sensor_3, sensor_4)
    end = time.time()
    elapsed = round((end-start), 5)
    print('That function took ' + str(elapsed) + ' seconds!')
    #print(data)
    eTotal += elapsed
    print(data[c+12], data[c+8], data[c+4], data[c])
    total = (data[c] + data[c+4] + data[c+8] + data[c+12])
    i = 1
       
    while ((data[0] < (data[1]*2.5)) & (data[4] < (data[5]*2.5)) &
           (data[8] < (data[9]*2.5)) & (data[12] < (data[13]*2.5))):
    #while i <100:
        #print(data[c+12], data[c+8], data[c+4], data[c])
        iSawRed = False
        if total < 250:
            pi.set_PWM_dutycycle(M1Sp, 0)
            pi.set_PWM_dutycycle(M2Sp, 0)
            print('I am lost...')
            print(data[c+12], data[c+8], data[c+4], data[c])
            break
        elif data[c] > (hiVals * .75): # Too far right; make a hard left!
            print('Hard left!')
            print(data[c+12], data[c+8], data[c+4], data[c])
            #print(i)
            while data[c+4] < (hiVals * .6):
                pi.set_PWM_dutycycle(M2Sp, 0)
                pi.set_PWM_dutycycle(M1Sp, (topSpeed*.60))
                start = time.time()
                data = TCS.getSensorData(pi, tcs1, tcs2, tcs3, tcs4, mux,
                  sensor_1, sensor_2, sensor_3, sensor_4)
                end = time.time()
                elapsed = round((end-start), 5)
                eTotal += elapsed
                print('That function took ' + str(elapsed) + ' seconds!')
                i += 1
            #print(i)
        elif data[c+12] > hiVals: # Too far left; make a hard right!
            print('Hard right!')
            print(data[c+12], data[c+8], data[c+4], data[c])
            #print(i)
            while data[c+8] < hiVals:
                pi.set_PWM_dutycycle(M2Sp, (topSpeed*.6))
                pi.set_PWM_dutycycle(M1Sp, 0)
                start = time.time()
                data = TCS.getSensorData(pi, tcs1, tcs2, tcs3, tcs4, mux,
                  sensor_1, sensor_2, sensor_3, sensor_4)
                end = time.time()
                elapsed = round((end-start), 5)
                eTotal += elapsed
                print('That function took ' + str(elapsed) + ' seconds!')
                i += 1
            #print(i)
        else:
            error = data[c+4] - data[c+8]
            #print('Error: ' + str(error))
            proportion = abs(error/hiVals) * kp
            #print('Proportion: ' + str(proportion))
            turn = topSpeed-proportion
            #print('Turn: ' + str(turn))
          
            if error > 0: # A little too far right; proportional turn left
                #print('Left...')
                pi.set_PWM_dutycycle(M2Sp, (topSpeed-proportion))
                pi.set_PWM_dutycycle(M1Sp, topSpeed)
            else: # A little too far left; proportional turn right
                #print('Right...')
                pi.set_PWM_dutycycle(M2Sp, topSpeed)
                pi.set_PWM_dutycycle(M1Sp, (topSpeed-proportion))
                
                
        start = time.time()
        data = TCS.getSensorData(pi, tcs1, tcs2, tcs3, tcs4, mux,
                  sensor_1, sensor_2, sensor_3, sensor_4)
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

topSpeed = 100  # Speed values range from 0-255.
col = 'clear'   # Color options include 'red'/'green'/'blue'/'clear'.

#(hiV,loV,tests) = calibrateSensors(color=col)
#print(tests)
#driveForward(hiV,loV,topSpeed,color=col)
eTotal = driveForward(180, 60, 150)



###################
# System Shutdown #
###################

# Put the sensor chips back to low power sleep/disabled.
pi.i2c_write_byte(mux, sensor_1)
tcs1.disable()
pi.i2c_close(tcs1._device)

pi.i2c_write_byte(mux, sensor_2)
tcs2.disable()
pi.i2c_close(tcs2._device)

pi.i2c_write_byte(mux, sensor_3)
tcs3.disable()
pi.i2c_close(tcs3._device)

pi.i2c_write_byte(mux, sensor_4)
tcs4.disable()
pi.i2c_close(tcs4._device)

pi.i2c_close(mux)

end8 = time.time()
elapsed8 = round((end8-start8), 1)
sensorTime = round(((eTotal/elapsed8)*100), 1)
print('That run took ' + str(elapsed8) + ' seconds!')
print(str(sensorTime) + '% of that time was spent reading the sensors.')

