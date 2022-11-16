import pigpio
from ControlFunctions import *
from time import sleep

pi = pigpio.pi('10.3.141.67')


drive(E, 50)
sleep(2)

stop()







pi.serial_close(sbt1)
pi.serial_close(sbt2)


'''

M1pwm = 12   # RPi pin cotrolling PWM for Motor 1 (orange wire)
M2pwm = 18   # RPi pin cotrolling PWM for Motor 2 (yellow wire)
M3pwm = 13   # RPi pin cotrolling PWM for Motor 3 (also orange wire)
M4pwm = 19   # RPi pin cotrolling PWM for Motor 4 (blue wire)

speed = 170

#pwm = GF.convert2pwm(speed)
stop = GF.convert2pwm(0)
print(stop)
print("Stop")
GF.drive4motors(pi, stop)

sleep(1.0)

print("Accellerate")
for step in range(speed):
    pwm = GF.convert2pwm(step)
    GF.drive4motors(pi, pwm)
    sleep(0.01)

sleep(3.0)

print("Decellerate")
for step in range(speed):
    step = 100 - step
    pwm = GF.convert2pwm(step)
    GF.drive4motors(pi, pwm)
    sleep(0.01)

print("Stop")
GF.drive4motors(pi, stop)

sleep(3.0)
print("Reverse")

print("Accellerate")
for step in range(speed):
    step = -step
    pwm = GF.convert2pwm(step)
    GF.drive4motors(pi, pwm)
    sleep(0.01)

sleep(3.0)

print("Stop")
GF.drive4motors(pi, stop)

sleep(3.0)
'''
print("All Done!!")
