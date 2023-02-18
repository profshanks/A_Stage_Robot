from SetupImports import *
from time import sleep
from ControlFunctions import *


t = .05
mm = 20
for i in range(5,mm):
    j = i + 2
    if j > 100:
        j = 100
    rightMotor(F,j)
    leftMotor(F,i)
    print(i)
    sleep(t)
    
sleep(3)

for i in range(0,mm):
    i =  mm - i
    if i < 10:
        i = 0
    rightMotor(F,i)
    leftMotor(F,i)
    sleep(.05)

stop()
pi.serial_close(sbt1)
