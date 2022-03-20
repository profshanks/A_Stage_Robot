'''
This works for controlling four motors using a pair ofSabertooth 2x32
Motor Driver boards. A RPi 4 is used as the micro-controller.
'''

import pigpio
from time import sleep
pi = pigpio.pi('10.3.141.51')
sbt1 = pi.serial_open("/dev/ttyAMA1", 9600)
sbt2 = pi.serial_open("/dev/serial0", 9600)
fwd = 'forward'
rev = 'reverse'

def motor1(direction, speed):
    newSpeed = int(speed/100 * 63)
    if direction == 'forward':
        newSpeed = newSpeed + 64
    elif direction == 'reverse':
        newSpeed = 64 - newSpeed
    pi.serial_write_byte(sbt1, newSpeed)
        
def motor2(direction, speed):
    newSpeed = int(speed/100 * 63)
    if direction == 'forward':
        newSpeed = newSpeed + 192
    elif direction == 'reverse':
        newSpeed = 191 - newSpeed
    pi.serial_write_byte(sbt1, newSpeed)
  
def motor3(direction, speed):
    newSpeed = int(speed/100 * 63)
    if direction == 'forward':
        newSpeed = newSpeed + 64
    elif direction == 'reverse':
        newSpeed = 64 - newSpeed
    pi.serial_write_byte(sbt2, newSpeed)
        
def motor4(direction, speed):
    newSpeed = int(speed/100 * 63)
    if direction == 'forward':
        newSpeed = newSpeed + 192
    elif direction == 'reverse':
        newSpeed = 191 - newSpeed
    pi.serial_write_byte(sbt2, newSpeed)

def allMotors(direction, speed):
    motor1(direction, speed)
    motor2(direction, speed)
    motor3(direction, speed)
    motor4(direction, speed)

def allMotorsLeft(speed):
    motor1(rev, speed)
    motor2(rev, speed)
    motor3(fwd, speed)
    motor4(rev, speed)
'''
allMotors(rev, 100)
sleep(2)
allMotors(fwd, 100)
sleep(1)
'''
allMotorsLeft(50)
sleep(2)

pi.serial_write_byte(sbt1, 0)
pi.serial_write_byte(sbt2, 0)





'''
pi.serial_write_byte(sbt1, 122)
sleep(1)
pi.serial_write_byte(sbt1, 0)
sleep(1)
pi.serial_write_byte(sbt1, 5)
sleep(1)
pi.serial_write_byte(sbt1, 0)
sleep(1)
pi.serial_write_byte(sbt1, 132)
sleep(1)
pi.serial_write_byte(sbt1, 0)
sleep(1)
pi.serial_write_byte(sbt1, 250)
sleep(1)
pi.serial_write_byte(sbt1, 0)
sleep(1)

pi.serial_write_byte(sbt2, 122)
sleep(1)
pi.serial_write_byte(sbt2, 0)
sleep(1)
pi.serial_write_byte(sbt2, 5)
sleep(1)
pi.serial_write_byte(sbt2, 0)
sleep(1)
pi.serial_write_byte(sbt2, 132)
sleep(1)
pi.serial_write_byte(sbt2, 0)
sleep(1)
pi.serial_write_byte(sbt2, 250)
sleep(1)
pi.serial_write_byte(sbt2, 0)
sleep(1)

'''
print('All done!')
