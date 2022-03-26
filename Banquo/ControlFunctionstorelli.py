from DirectionVariables import *
from SetupImports import *
from math import sin, cos, radians

def northMotor(direction, speed):
    newSpeed = int(speed/100 * 63)
    if direction == 'North': 
        newSpeed = newSpeed + 192
    elif direction == 'South': 
        newSpeed = 191 - newSpeed
    pi.serial_write_byte(sbt1, newSpeed)

def southMotor(direction, speed):
    newSpeed = int(speed/100 * 63)
    if direction == 'North': 
        newSpeed = newSpeed + 64
    elif direction == 'South':
        newSpeed = 64 - newSpeed
    pi.serial_write_byte(sbt2, newSpeed)
    
def eastMotor(direction, speed):
    newSpeed = int(speed/100 * 63)
    if direction == 'North':
        newSpeed = newSpeed + 64
    elif direction == 'South':
        newSpeed = 64 - newSpeed
    pi.serial_write_byte(sbt1, newSpeed)
    
def westMotor(direction, speed):
    newSpeed = int(speed/100 * 63)
    if direction == 'North':
        newSpeed = newSpeed + 192
    elif direction == 'South':
        newSpeed = 191 - newSpeed
    pi.serial_write_byte(sbt2, newSpeed)
    
def allMotors(direction, speed):
    northMotor(direction, speed)
    eastMotor(direction, speed)
    westMotor(direction, speed)
    southMotor(direction, speed)
    
def drive(direction, speed):
    if direction == N:
        allMotors(direction, speed)
    elif direction == S:
        allMotors(direction, speed)
    elif direction == E:
        northMotor(S, speed)
        eastMotor(S, speed)
        westMotor(N, speed)
        southMotor(N, speed)
    elif direction == W:
        northMotor(N, speed)
        eastMotor(N, speed)
        westMotor(S, speed)
        southMotor(S, speed)
    elif direction == NW:
        northMotor(N, 100)
        eastMotor(N, 100)
        westMotor(S, 50)
        southMotor(S,50)

def stop():
    pi.serial_write_byte(sbt1, 0)
    pi.serial_write_byte(sbt2, 0)
    
