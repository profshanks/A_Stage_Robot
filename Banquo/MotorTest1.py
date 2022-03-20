import pigpio
import GhostFunctions as GF
from time import sleep

pi = pigpio.pi('10.3.141.95')

M1pwm = 12   # RPi pin cotrolling PWM for Motor 1 (orange wire)
M2pwm = 18   # RPi pin cotrolling PWM for Motor 2 (yellow wire)
M3pwm = 13   # RPi pin cotrolling PWM for Motor 3 (green wire)
M4pwm = 19   # RPi pin cotrolling PWM for Motor 4 (blue wire)

speed = 170

#pwm = GF.convert2pwm(speed)
stop = GF.convert2pwm(0)
print(stop)
print("Stop")
GF.drive4motors(pi, stop)

sleep(3.0)

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

print("All Done!!")
