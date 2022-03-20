import pigpio
import GhostFunctions as GF
from time import sleep

pi = pigpio.pi('10.3.141.95')

M1pwm = 12   # RPi pin cotrolling PWM for Motor 1 (orange wire)
M2pwm = 18   # RPi pin cotrolling PWM for Motor 2 (yellow wire)
M3pwm = 13   # RPi pin cotrolling PWM for Motor 3 (green wire)
M4pwm = 19   # RPi pin cotrolling PWM for Motor 4 (blue wire)

speed = 100

pi.set_PWM_dutycycle(17, 255)
print("LED on")
sleep(3)
pi.set_PWM_dutycycle(17, 0)
print("LED off")
