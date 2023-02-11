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

E_decoder = rotaryEncoder.decoder(pi, 24, 23, callback)
print("pulses before: " + str(E_decoder.pulses)) #n/a
E_decoder.levA = 0
E_decoder.levB = 0
E_decoder.tick = 0
revs=input("Enter revs: ")
pulses = revs * 189
rev = E_decoder.pulses/189
while pulses != E_decoder.pulses:
    i += 10
    eastMotor(N,i)
    if i == 100:
        stop()
print("pulses after: " + str(E_decoder.pulses)) #n/a
print("East revs are: " + str(revs)) #n/a
E_decoder.cancel()

#while speed == 90%:
#if eastpulses < westpulses:
#speed - 10
#else if westpulse > eastpulse:
#speed - 10
#close 
pi.serial_close(sbt1)
pi.serial_close(sbt2)
