from SetupImports import *

def leftMotor(direction, speed):
    newSpeed = int(speed/100 * 63)
    if direction == 'forward': 
        newSpeed = newSpeed + 192
    elif direction == 'reverse': 
        newSpeed = 191 - newSpeed
    pi.serial_write_byte(sbt1, newSpeed)

def rightMotor(direction, speed):
    newSpeed = int(speed/100 * 63)
    if direction == 'reverse': 
        newSpeed = newSpeed + 64
    elif direction == 'forward':
        newSpeed = 64 - newSpeed
    pi.serial_write_byte(sbt1, newSpeed)

def stop():
    pi.serial_write_byte(sbt1, 0)
