import pigpio
from time import sleep
import rotaryEncoder
#from SetupImports import *
from DirectionVariables import *
from ControlFunctions import *

#i want to run the motor at the lowest and highest speed at 60 seconds to
#see how many revs i get

pi = pigpio.pi('10.3.141.67')
sbt1 = pi.serial_open("/dev/ttyAMA1", 9600)
sbt2 = pi.serial_open("/dev/serial0", 9600)
#revs = 0
#global pulses
#pulses = 0


def callback(way):
  if (way == 1):
    pulses += abs(way)




E_decoder = rotaryEncoder.decoder(pi, 24, 23, callback)
print("pulses before: " + str(E_decoder.pulses))
E_decoder.levA = 0
E_decoder.levB = 0
E_decoder.tick = 0
#lowest speed 10
#revs are 12 maybe ~13
eastMotor(N,30)
sleep(4)
stop()
revs = E_decoder.pulses/189
print("pulses after: " + str(E_decoder.pulses))
print("East revs are: " + str(revs))

E_decoder.cancel()

#close 
pi.serial_close(sbt1)
pi.serial_close(sbt2)
