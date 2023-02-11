import Rosalind_Support_Functions as RSF
from Rosalind_Drive_Functions_2_5_2022 import *
import pigpio

from time import sleep
import sys

def calibrate(pi, key, offset, calSpeed) :
    
    calibrateSensorData = {}

    c1on = 0
    c2on = 0

    spinRight(pi, calSpeed)

    while (c1*offset) > 20 or c2 > 20: # When both sensors go low
        c1,c2 = RSF.fastcalibrateSensorData(pi, mux, sensorList, sensor)
        calibrateSensorData[key] = [c1, c2]
        key+=1
        if (c1*offset> c1on):
            c1on = c1
        if (c2 > c2on):
            c2on = c2

    for i in range(5): # keeps going for 5 more cycles to make sure both are off
        c1,c2 = RSF.fastcalibrateSensorData(pi, mux, sensorList, sensor)
        calibrateSensorData[key] = [c1, c2]
        key+=1
        if ((c1*offset)> c1on):
            c1on = c1
        if (c2 > c2on):
            c2on = c2

    calibrateSensorData[key] = [0, 0]
    c1off = c1
    c2off = c2
    key+=1

    spinLeft(pi, calSpeed)

    for i in range(25): # Reverse for 25 cycles to re-engage line
        c1,c2 = RSF.fastcalibrateSensorData(pi, mux, sensorList, sensor)
        calibrateSensorData[key] = [c1, c2]
        key+=1
        if ((c1*offset) > c1on):
            c1on = c1
        if (c2 > c2on):
            c2on = c2

    while (c1*offset) > 20 or c2 > 20: # When both sensors go low
        c1,c2 = RSF.fastcalibrateSensorData(pi, mux, sensorList, sensor)
        calibrateSensorData[key] = [c1, c2]
        key+=1
        if ((c1*offset)> c1on):
            c1on = c1
        if (c2 > c2on):
            c2on = c2

    calibrateSensorData[key] = [0, 0]
    key+=1

    spinRight(pi, calSpeed)

    for i in range(20):  #  reverse for 10 cycles
        prevData = c2
        c1,c2 = RSF.fastcalibrateSensorData(pi, mux, sensorList, sensor)
        calibrateSensorData[key] = [c1, c2]
        key+=1
        if ((c1*offset) > c1on):
            c1on = c1
        if (c2 > c2on):
            c2on = c2

    difference = prevData - c2  

    while difference < 3 : # When both sensors are equally on the line
        prevData = c2
        c1,c2 = RSF.fastcalibrateSensorData(pi, mux, sensorList, sensor)
        calibrateSensorData[key] = [c1, c2]
        difference = prevData - c2
        key+=1
        if ((c1*offset) > c1on):
            c1on = c1
        if (c2 > c2on):
            c2on = c2
    

    stop(pi)

    onDiff = c2on/c1on
    offDiff = c2off/c1off

    offset =  (onDiff+offDiff)/2

    print(f'c1on: {c1on}')
    print(f'c2on: {c2on}')
    print(f'c1off: {c1off}')
    print(f'c2off: {c2off}')
    print(f'onDiff: {onDiff}')
    print(f'offDiff: {offDiff}')
    print(f'offset: {offset}')
