
from time import sleep

#from GhostFunctions import cardinalDirections
from cardinalDirections import *
'''
drive(direction, speed):    Direction is N/S/E/W etc.
                            NNW is an option too
                            So are polar coordinates such as 27 or 118.45
                            Speed is on a scale of 0-100
spin(direction, speed):     Direction is CW or CCW
                            Speed is on a scale of 0-100
'''

    
print(N, E, S, W)
 
'''
for speed in range(100):
    motor1(N, speed)
    motor4(S, speed)
    motor3(E, speed)
    motor2(W, speed)
    sleep(.025)

print('Full Speed')
sleep(5)
'''
pi.serial_write_byte(sbt1, 0)
pi.serial_write_byte(sbt2, 0)

pi.serial_close(sbt1)
pi.serial_close(sbt2)
print('All done!')

