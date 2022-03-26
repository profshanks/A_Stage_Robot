from DirectionVariables import *
from SetupImports import *
from math import sin, cos, radians

def northMotor(direction, speed):
    newSpeed = int(speed/100 * 63)
    if direction == 'West': 
        newSpeed = newSpeed + 192
    elif direction == 'East': 
        newSpeed = 191 - newSpeed
    pi.serial_write_byte(sbt1, newSpeed)

def southMotor(direction, speed):
    newSpeed = int(speed/100 * 63)
    if direction == 'East': 
        newSpeed = newSpeed + 64
    elif direction == 'West':
        newSpeed = 64 - newSpeed
    pi.serial_write_byte(sbt2, newSpeed)
    
def eastMotor(direction, speed):
    newSpeed = int(speed/100 * 63)
    if direction == 'South':
        newSpeed = newSpeed + 64
    elif direction == 'North':
        newSpeed = 64 - newSpeed
    pi.serial_write_byte(sbt1, newSpeed)
    
def westMotor(direction, speed):
    newSpeed = int(speed/100 * 63)
    if direction == 'North':
        newSpeed = newSpeed + 192
    elif direction == 'South':
        newSpeed = 191 - newSpeed
    pi.serial_write_byte(sbt2, newSpeed)

def North_South(direction, speed):
    eastMotor(direction,speed)
    westMotor(direction,speed)

def West_East(direction, speed):
    northMotor(direction,speed)
    southMotor(direction,speed)

def drive(direction, speed):
    '''This function converts a direction into degrees.
       You can use the following variables N,S,E,W... or 0,90,180...
       Your speed must be between the intervals 0-100, 0 being the slowest and 100 the fastest.'''
    if direction in convert:
        direction = convert[direction]
    if direction < 90:
        direction = radians(direction)
        NS_Component = cos(direction) * speed
        WE_Component = sin(direction) * speed
        North_South(N,NS_Component)
        West_East(E,WE_Component)
    elif direction < 180:
        direction = 180 - direction        
        direction = radians(direction)
        NS_Component = cos(direction) * speed
        WE_Component = sin(direction) * speed
        North_South(S,NS_Component)
        West_East(E,WE_Component)
    elif direction < 270:
        direction = direction - 180        
        direction = radians(direction)
        NS_Component = cos(direction) * speed
        WE_Component = sin(direction) * speed
        North_South(S,NS_Component)
        West_East(W,WE_Component)

    elif direction <= 360:
        direction = 360 - direction        
        direction = radians(direction)
        NS_Component = cos(direction) * speed
        WE_Component = sin(direction) * speed
        North_South(N,NS_Component)
        West_East(W,WE_Component)
    else:
        print("Error")

def stop():
    pi.serial_write_byte(sbt1, 0)
    pi.serial_write_byte(sbt2, 0)
    
