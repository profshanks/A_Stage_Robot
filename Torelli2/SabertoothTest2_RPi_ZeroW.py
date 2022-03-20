'''
This works for controlling two motors using a Sabertooth 2x32 Motor Driver
board. A RPi Zero-W is used as the micro-controller.
'''

import pigpio
from time import sleep

pi = pigpio.pi('10.3.141.58')

sbt1 = pi.serial_open("/dev/serial0", 9600)
#sbt1 = pi.serial_open("/dev/ttyAMA1", 9600)

pi.serial_write_byte(sbt1, 122)
sleep(2)
pi.serial_write_byte(sbt1, 0)
sleep(2)
pi.serial_write_byte(sbt1, 5)
sleep(2)
pi.serial_write_byte(sbt1, 0)
sleep(2)
pi.serial_write_byte(sbt1, 132)
sleep(2)
pi.serial_write_byte(sbt1, 0)
sleep(2)
pi.serial_write_byte(sbt1, 250)
sleep(2)
pi.serial_write_byte(sbt1, 0)
sleep(2)

print('All done!')
