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
  if (way == -1):
    pulses += abs(way)




E_decoder = rotaryEncoder.decoder(pi, 24, 23, callback)
print("pulses before: " + str(E_decoder.pulses))
E_decoder.levA = 0
E_decoder.levB = 0
E_decoder.tick = 0
#lowest speed 10
#revs are 12 maybe ~13
eastMotor(S,30)
sleep(4)
stop()
revs = E_decoder.pulses/189
print("pulses after: " + str(E_decoder.pulses))
print("East revs are: " + str(revs))

E_decoder.cancel()

####################################################
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

####################################################
W_decoder = rotaryEncoder.decoder(pi, 11, 9, callback)
print("pulses before: " + str(W_decoder.pulses))
W_decoder.levA = 0
W_decoder.levB = 0
W_decoder.tick = 0
#lowest speed 10
#revs are 12 maybe ~13
westMotor(S,30)
sleep(4)
stop()
revs = W_decoder.pulses/189
print("pulses after: " + str(W_decoder.pulses))
print("West revs are: " + str(revs))

W_decoder.cancel()
####################################################
S_decoder = rotaryEncoder.decoder(pi, 16, 20, callback)
print("pulses before: " + str(S_decoder.pulses))
S_decoder.levA = 0
S_decoder.levB = 0
S_decoder.tick = 0
#lowest speed 10
#revs are 12 maybe ~13
southMotor(W,30)
sleep(4)
stop()
revs = S_decoder.pulses/189
print("pulses after: " + str(S_decoder.pulses))
print("South revs are: " + str(revs))

S_decoder.cancel()

#pi.stop()
#stop()
#Shutdown
pi.serial_close(sbt1)
pi.serial_close(sbt2)
