import pigpio
from time import sleep

def accellerate(startSpeed, endSpeed, rate=0.01, direction=0):
    print("Accellerate")
    pi2.write(M1Dir, direction)
    pi2.write(M2Dir, direction)
    for pwm in range(startSpeed, endSpeed):
        pi2.set_PWM_dutycycle(M1Sp, pwm)
        pi2.set_PWM_dutycycle(M2Sp, pwm)
        sleep(rate)

def decellerate(startSpeed, endSpeed, rate=0.01, direction=0):
    print("Decellerate")
    pi2.write(M1Dir, direction)
    pi2.write(M2Dir, direction)
    for pwm in range(endSpeed, startSpeed):
        invPWM = startSpeed - pwm
        pi2.set_PWM_dutycycle(M1Sp, invPWM)
        pi2.set_PWM_dutycycle(M2Sp, invPWM)
        sleep(rate)

def straight(speed, time, direction):
    pi2.write(M1Dir, direction)
    pi2.write(M2Dir, direction)
    pi2.set_PWM_dutycycle(M1Sp, speed)
    pi2.set_PWM_dutycycle(M2Sp, speed)
    sleep(time)

def circleRight(rightSpeed, leftSpeed, direction, time):
    pi2.write(M1Dir, direction)
    pi2.write(M2Dir, direction)
    pi2.set_PWM_dutycycle(M1Sp, rightSpeed)
    pi2.set_PWM_dutycycle(M2Sp, leftSpeed)
    sleep(time)

def circleLeft(rightSpeed, leftSpeed, direction, time):
    pi2.write(M1Dir, direction)
    pi2.write(M2Dir, direction)
    pi2.set_PWM_dutycycle(M1Sp, rightSpeed)
    pi2.set_PWM_dutycycle(M2Sp, leftSpeed)
    sleep(time)   

def spinLeft(topSpeed, time, rate=0.003):
    print("turnLeft")
    pi2.write(M1Dir, 0)
    pi2.write(M2Dir, 1)
    for pwm in range(topSpeed):
        pi2.set_PWM_dutycycle(M1Sp, pwm)
        pi2.set_PWM_dutycycle(M2Sp, pwm)
        sleep(rate)
    sleep(time)
    for pwm in range(topSpeed):
        invPWM = topSpeed - pwm
        pi2.set_PWM_dutycycle(M1Sp, invPWM)
        pi2.set_PWM_dutycycle(M2Sp, invPWM)
        sleep(rate)

def spinRight(topSpeed, time, rate=0.003):
    print("turnLeft")
    pi2.write(M1Dir, 1)
    pi2.write(M2Dir, 0)
    for pwm in range(0, topSpeed, 5):
        pi2.set_PWM_dutycycle(M1Sp, pwm)
        pi2.set_PWM_dutycycle(M2Sp, pwm)
        sleep(rate)
    sleep(time)
    for pwm in range(0, topSpeed, 5):
        invPWM = topSpeed - pwm
        pi2.set_PWM_dutycycle(M1Sp, invPWM)
        pi2.set_PWM_dutycycle(M2Sp, invPWM)
        sleep(rate)

def stop():
    print("Stop")
    pi2.set_PWM_dutycycle(M1Sp, 0)
    pi2.set_PWM_dutycycle(M2Sp, 0)

pi2 = pigpio.pi('10.3.141.1')

M2Sp = 13				# set pwm2 pin on MD10-Hat
M1Sp = 12				# set pwm1 pin on MD10-hat
M2Dir = 24				# set dir2 pin on MD10-Hat
M1Dir = 26				# set dir1 pin on MD10-Hat

topSpeed = 200                               # set maximum motor speed
accel = 0
forward = 0
reverse = 1
'''
accellerate(0, topSpeed, rate=accel)
sleep(1.0)
decellerate(topSpeed, 0, rate=accel)

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
'''

#straight(50, 2, forward)
#circleRight(50, 100, forward, 3)
#circleRight(100, 50, forward, 3)
'''
for j in range(1):
    straight(150, 2, forward)
    for i in range(1):
        spinRight(255, 1)
        #spinLeft(255, 1)
    straight(150, 2, forward)
    #time.sleep(2)
    stop()
'''
straight(150, 2, forward)
spinRight(255, 1)
straight(150, 2, forward)

stop()

print("All Done!!")

    
