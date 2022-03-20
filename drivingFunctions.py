


def accellerate(pi2, startSpeed, endSpeed, rate=0.01, direction=0):
    print("Accellerate")
    pi2.write(M1Dir, direction)
    pi2.write(M2Dir, direction)
    for pwm in range(startSpeed, endSpeed):
        pi2.set_PWM_dutycycle(M1Sp, pwm)
        pi2.set_PWM_dutycycle(M2Sp, pwm)
        sleep(rate)

def decellerate(pi2, startSpeed, endSpeed, rate=0.01, direction=0):
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
