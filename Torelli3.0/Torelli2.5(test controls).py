import rotaryEncoder
from SetupImports import *
from time import sleep, time
from ControlFunctions import *

#Function to calculate pulses
def callback(way):
  if (way == 1):
    pulses += abs(way)

    
#DecoderSetup
R_decoder = rotaryEncoder.decoder(pi, 17, 27, callback)  # Right Motor
L_decoder = rotaryEncoder.decoder(pi, 23, 24, callback) # Left Motor

'''
# To test leftMotor seperately(revs)
def Drive(motor2, direction, revs, speed, ppr, callback):
    pulses_rev = revs * ppr
    while L_decoder.pulses < pulses_rev:
      motor2(direction, speed)
    stop()
    print("pulses: " + str(L_decoder.pulses))
    print("What pulses should be: " + str(pulses_rev))
Drive(leftMotor, F, 10, 100, 1310, callback)
'''


# To test dual motor functionality(revs)
def Drive(motor1, motor2, direction, revs, speed, ppr, callback):
    pulses_rev = revs * ppr
    while (R_decoder.pulses and L_decoder.pulses) < pulses_rev:
      seconds = time()
      motor1(direction, speed)
      motor2(direction, speed)
    stop()
    print("Seconds since epoch =", seconds)	
    print("pulses1: " + str(R_decoder.pulses))
    print("pulses2: " + str(L_decoder.pulses))
    print("What pulses should be: " + str(pulses_rev))
Drive(rightMotor, leftMotor, F, 10, 100, 1310, callback)


'''
# To test leftMotor seperately(sleep)
def Drive(motor2, direction, revs, speed, ppr, callback):
    pulses_rev = revs * ppr
    motor2(direction, speed)
    sleep(3)
    stop()
    print("pulses: " + str(L_decoder.pulses))
    print("What pulses should be: " + str(pulses_rev))
Drive(leftMotor, F, 2, 100, 1316, callback)
'''

#Decoder cancel
R_decoder.cancel()
L_decoder.cancel()

#Serial close
pi.serial_close(sbt1)
