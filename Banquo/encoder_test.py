import pigpio
from ControlFunctions import *
from rotary_encoder import decoder
from time import sleep

pi = pigpio.pi('10.3.141.67')
sbt1 = pi.serial_open("/dev/ttyAMA1", 9600)
sbt2 = pi.serial_open("/dev/serial0", 9600)

pos = 0

def callback(way):

   global pos

   pos += way

   print("pos={}".format(pos))

encoder_s = decoder(pi, 23, 24, callback)
print('Doing something?')

print(encoder_s.gpioA)



pi.stop()

drive(E, 50)
sleep(5)
drive(W, 50)
sleep(5)
stop()

encoder_s.cancel()






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
