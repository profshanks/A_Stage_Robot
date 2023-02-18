import pigpio
from time import sleep
import rotaryEncoder
#from SetupImports import *
from DirectionVariables import *
from ControlFunctions import *

pi = pigpio.pi('10.3.141.67')
sbt1 = pi.serial_open("/dev/ttyAMA1", 9600)
sbt2 = pi.serial_open("/dev/serial0", 9600)

def callback(way):
  if (way == 1):
    pulses += abs(way)

N_decoder = rotaryEncoder.decoder(pi, 17, 27, callback)
print("pulses before: " + str(N_decoder.pulses))
N_decoder.levA = 0
N_decoder.levB = 0
N_decoder.tick = 0
#lowest speed 10
#revs are 12 maybe ~13
northMotor(W,30)
sleep(4)
stop()
revs = N_decoder.pulses/189
print("pulses after: " + str(N_decoder.pulses))
print("North revs are: " + str(revs))

N_decoder.cancel()

#close 
pi.serial_close(sbt1)
pi.serial_close(sbt2)
