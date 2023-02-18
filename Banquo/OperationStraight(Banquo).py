import pigpio
from time import sleep
import rotaryEncoder
from DirectionVariables import *
from ControlFunctions import *

#PiSetup
pi = pigpio.pi('10.3.141.67')
sbt1 = pi.serial_open("/dev/ttyAMA1", 9600)
sbt2 = pi.serial_open("/dev/serial0", 9600)


#Function to calculate pulses
def callback(way):
  if (way == 1):
    pulses += abs(way)
    
#DecoderSetup
W_decoder = rotaryEncoder.decoder(pi, 11, 9, callback)  # West Motor
E_decoder = rotaryEncoder.decoder(pi, 24, 23, callback) # East Motor


def goStraight(motor1, motor2, direction, revs, speed, ppr, callback):
    pulses_rev = revs * ppr
    while E_decoder.pulses < pulses_rev:
      if W_decoder.pulses > E_decoder.pulses:          
        motor1(direction, speed * .9)
        motor2(direction, speed)
      else:
        motor1(direction, speed)
        motor2(direction, speed * .9)
#    sleep(3)    
    stop()
    print("pulses1: " + str(W_decoder.pulses))
    print("pulses2: " + str(E_decoder.pulses))
    print("What pulses should be: " + str(pulses_rev))
#    print("What pulses2 should be: " + str(pulses_rev2))
goStraight(westMotor, eastMotor, S, 5, 50, 189, callback)

W_decoder.cancel()
E_decoder.cancel()

#Close
pi.serial_close(sbt1)
pi.serial_close(sbt2)
