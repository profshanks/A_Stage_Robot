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
pos = 0
pulses = 0
revs = 0

def callback(way):
  global pulses
  global pos
  if (way == 1):
    pulses += way
#    print("way={}".format(way))
#    print("revs are: " + str(revs))


  
decoder = rotaryEncoder.decoder(pi, 24, 23, callback)
#lowest speed 10
#revs are 12 maybe ~13
eastMotor(S,30)
sleep(4)
stop()
revs = pulses/189
print("revs are: " + str(revs))

decoder.cancel()
'''
####################################################
decoder = rotaryEncoder.decoder(pi, 17, 27, callback)
#lowest speed 10
#revs are 12 maybe ~13
northMotor(W,30)
sleep(4)
stop()
revs = pulses/189
print("revs are: " + str(revs))

decoder.cancel()
####################################################
decoder = rotaryEncoder.decoder(pi, 11, 9, callback)
#lowest speed 10
#revs are 12 maybe ~13
westMotor(N,30)
sleep(4)
stop()
revs = pulses/189
print("revs are: " + str(revs))

decoder.cancel()
####################################################
decoder = rotaryEncoder.decoder(pi, 16, 20, callback)
#lowest speed 10
#revs are 12 maybe ~13
southMotor(W,30)
sleep(4)
stop()
revs = pulses/189
print("revs are: " + str(revs))

decoder.cancel()
'''
#pi.stop()
#stop()
#Shutdown
pi.serial_close(sbt1)
pi.serial_close(sbt2)
