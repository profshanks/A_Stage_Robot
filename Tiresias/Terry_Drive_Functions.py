from time import sleep
import sys

import pigpio

import Terry_Support_Functions as TSF


M2Sp = 13				# set pwm2 pin on MD10-Hat
M1Sp = 12				# set pwm1 pin on MD10-hat
M2Dir = 24				# set dir2 pin on MD10-Hat
M1Dir = 26				# set dir1 pin on MD10-Hat

forward = 0
reverse = 1

kP = 1
kI = 1
kD = 1

def stop(pi):
    pi.set_PWM_dutycycle(M1Sp, 0)
    pi.set_PWM_dutycycle(M2Sp, 0)

def spinRight(pi, speed):
    pi.write(M1Dir, forward)
    pi.set_PWM_dutycycle(M1Sp, speed)
    pi.write(M2Dir, reverse)
    pi.set_PWM_dutycycle(M2Sp, speed)

def spinLeft(pi, speed):
    pi.write(M1Dir, reverse)
    pi.set_PWM_dutycycle(M1Sp, speed)
    pi.write(M2Dir, forward)
    pi.set_PWM_dutycycle(M2Sp, speed)

def calibrateMe(pi, speed, lower):
    sensorData = {}
    r1,g1,b1,c1,r2,g2,b2,c2 = TSF.getSensorData(pi, mux, sensorList, sensor)
    key = 1

    spinRight(pi, speed)

    while c1 > lower or c2 > lower: # When both sensors go low
        r1,g1,b1,c1,r2,g2,b2,c2 = TSF.getSensorData(pi, mux, sensorList, sensor)
        sensorData[key] = [c1, c2]
        key += 1

    for i in range(5):  # Keep going for 5 more cycles
        r1,g1,b1,c1,r2,g2,b2,c2 = TSF.getSensorData(pi, mux, sensorList, sensor)
        sensorData[key] = [c1, c2]
        key += 1    

    spinLeft(pi, speed)

    for i in range(10): # Reverse for 10 cycles to re-engage line
        r1,g1,b1,c1,r2,g2,b2,c2 = TSF.getSensorData(pi, mux, sensorList, sensor)
        sensorData[key] = [c1, c2]
        key += 1

    while c1 > lower or c2 > lower: # When both sensors go low
        r1,g1,b1,c1,r2,g2,b2,c2 = TSF.getSensorData(pi, mux, sensorList, sensor)
        sensorData[key] = [c1, c2]
        key += 1

    for i in range(5):  # Keep going for 5 more cycles
        r1,g1,b1,c1,r2,g2,b2,c2 = TSF.getSensorData(pi, mux, sensorList, sensor)
        sensorData[key] = [c1, c2]
        key += 1  

    spinRight(pi, speed)

    for i in range(10): # Reverse for 10 cycles to re-engage line
        r1,g1,b1,c1,r2,g2,b2,c2 = TSF.getSensorData(pi, mux, sensorList, sensor)
        sensorData[key] = [c1, c2]
        key += 1

    while c1 > lower or c2 > lower: # When both sensors go low
        r1,g1,b1,c1,r2,g2,b2,c2 = TSF.getSensorData(pi, mux, sensorList, sensor)
        sensorData[key] = [c1, c2]
        key += 1

    for i in range(5):  # Keep going for 5 more cycles
        r1,g1,b1,c1,r2,g2,b2,c2 = TSF.getSensorData(pi, mux, sensorList, sensor)
        sensorData[key] = [c1, c2]
        key += 1
        
    stop(pi)
    return sensorData

'''
# This is the super-squiggly algorithm
while (b1/c1) < .4 :
    if c1 < 45:
        pi.set_PWM_dutycycle(M1Sp, speed * cut)
        pi.set_PWM_dutycycle(M2Sp, speed)

    else:
        pi.set_PWM_dutycycle(M1Sp, speed)
        pi.set_PWM_dutycycle(M2Sp, speed * cut)

    r1,g1,b1,c1,r2,g2,b2,c2 = TSF.getSensorData(pi, mux, sensorList, sensor)

'''
'''
# This is the proportional-cut algorithm
while (b1/c1) < .4:
    if c1 < 15:
        print('Did you pick me up!')
        pi.set_PWM_dutycycle(M1Sp, 0)
        pi.set_PWM_dutycycle(M2Sp, 0)

        # Put the sensor chips back to low power sleep/disabled.
        pi.i2c_write_byte(mux, sensor_1)
        tcs1.disable()
        pi.i2c_write_byte(mux, sensor_2)
        tcs2.disable()
        
        sys.exit()
    
    if c1 < threshold: # Turn Left
        i += 1
        offBy = (threshold - c1) * ko
        cut = (threshold-offBy)/threshold
        if (cut < clim):
            cut = .5
        if i > 5:
            cut = .45
        pi.set_PWM_dutycycle(M1Sp, speed * cut)
        pi.set_PWM_dutycycle(M2Sp, speed)

    else:  # Turn Right
        i = 0
        offBy = (c1 - threshold) * ko
        cut = abs((threshold-offBy)/threshold)
        if (cut < clim):
            cut = .5
        pi.set_PWM_dutycycle(M1Sp, speed)
        pi.set_PWM_dutycycle(M2Sp, speed * cut)

    r1,g1,b1,c1,r2,g2,b2,c2 = TSF.getSensorData(pi, mux, sensorList, sensor)

print('I see Blue!')
pi.set_PWM_dutycycle(M1Sp, 0)
pi.set_PWM_dutycycle(M2Sp, 0)
'''       
