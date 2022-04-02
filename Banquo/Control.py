#Imports
from SetupImports import *
from DirectionVariables import *
from ControlFunctionstorelli import *
from time import sleep
'''
numbers = "1234567890"
answer = input("Start drive controls(yes or no)? ")
while answer == 'yes':
    d = input("What direction should I go? ")
    if d[0] in numbers:
        d = int(d)
    s = input("What speed should I go? ")
    s = int(s)
    drive(d,s)
    sleep(1)
    stop()
    answer = input("Keep Going(yes or no)? ")
'''
stop()
#Shutdown
pi.serial_close(sbt1)
pi.serial_close(sbt2)
