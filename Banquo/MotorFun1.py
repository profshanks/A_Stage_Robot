'''
This works for controlling four motors using a pair ofSabertooth 2x32
Motor Driver boards. A RPi 4 is used as the micro-controller.
'''

import pigpio
from time import sleep
pi = pigpio.pi('10.3.141.67')
sbt1 = pi.serial_open("/dev/ttyAMA1", 9600)
sbt2 = pi.serial_open("/dev/serial0", 9600)
N = 'North'
E = 'East'
S = 'South'
W = 'West'

def motor1(direction, speed):
    newSpeed = int(speed/100 * 63)
    if direction == 'South':
        newSpeed = newSpeed + 64
    elif direction == 'North':
        newSpeed = 64 - newSpeed
    pi.serial_write_byte(sbt1, newSpeed)
        
def motor2(direction, speed):
    newSpeed = int(speed/100 * 63)
    if direction == 'West':
        newSpeed = newSpeed + 192
    elif direction == 'East':
        newSpeed = 191 - newSpeed
    pi.serial_write_byte(sbt1, newSpeed)
  
def motor3(direction, speed):
    newSpeed = int(speed/100 * 63)
    if direction == 'West':
        newSpeed = newSpeed + 64
    elif direction == 'East':
        newSpeed = 64 - newSpeed
    pi.serial_write_byte(sbt2, newSpeed)
        
def motor4(direction, speed):
    newSpeed = int(speed/100 * 63)
    if direction == 'South':
        newSpeed = newSpeed + 192
    elif direction == 'North':
        newSpeed = 191 - newSpeed
    pi.serial_write_byte(sbt2, newSpeed)
'''

for speed in range(100):
    motor1(N, speed)
    motor4(S, speed)
    motor3(E, speed)
    motor2(W, speed)
    sleep(.025)

print('Full Speed')
sleep(5)

for speed in range(100):
    speed = 100 - speed
    motor1(N, speed)
    motor4(S, speed)
    motor3(E, speed)
    motor2(W, speed)
    sleep(.025)
'''
pi.serial_write_byte(sbt1, 0)
pi.serial_write_byte(sbt2, 0)

pi.serial_close(sbt1)
pi.serial_close(sbt2)
print('All done!')
