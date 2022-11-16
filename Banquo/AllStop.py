import pigpio
import GhostFunctions as GF
from time import sleep

pi = pigpio.pi('10.3.141.67')

M1pwm = 12   # RPi pin cotrolling PWM for Motor 1 (orange wire)
M2pwm = 18   # RPi pin cotrolling PWM for Motor 2 (yellow wire)
M3pwm = 13   # RPi pin cotrolling PWM for Motor 3 (green wire)
M4pwm = 19   # RPi pin cotrolling PWM for Motor 4 (blue wire)

speed = 100

GF.drive4motors(pi, 170)

print("All Done!!")
