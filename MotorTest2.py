import pigpio
from time import sleep
from drivingFunctions import *

pi2 = pigpio.pi('10.3.141.249')

M2Sp = 13				# set pwm2 pin on MD10-Hat
M1Sp = 12				# set pwm1 pin on MD10-hat
M2Dir = 24				# set dir2 pin on MD10-Hat
M1Dir = 26				# set dir1 pin on MD10-Hat

topSpeed = 200                               # set maximum motor speed
accel = 0
forward = 0
reverse = 1

accellerate(pi2, 0, topSpeed, rate=accel)
sleep(1.0)
decellerate(pi2, topSpeed, 0, rate=accel)

turnLeft(150, 2, rate=accel)
turnRight(150, 2, rate=accel)

sleep(2)
'''
'''
accellerate(0, topSpeed, rate=accel, direction=1)
sleep(1)
decellerate(topSpeed, 0, rate=accel, direction=1)
'''
'''
pi2.write(M1Dir, 1)
pi2.write(M2Dir, 1)
    
pi2.set_PWM_dutycycle(M1Sp, 50)
pi2.set_PWM_dutycycle(M2Sp, 50)
sleep(1)


#straight(50, 2, forward)
#circleRight(50, 100, forward, 3)
#circleRight(100, 50, forward, 3)

for j in range(1):
    straight(150, 2, forward)
    for i in range(1):
        spinRight(255, 1)
        #spinLeft(255, 1)
    straight(150, 2, forward)
    #time.sleep(2)
    stop()
'''
'''
straight(150, 2, forward)
spinRight(255, 1)
straight(150, 2, forward)

stop()

print("All Done!!")

    
