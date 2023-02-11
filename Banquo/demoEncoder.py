import pigpio
from time import sleep
import rotaryEncoder
from SetupImports import *
from DirectionVariables import *
from ControlFunctions import *

pi = pigpio.pi('10.3.141.67')
pos = 0

def callback(way):
  global pos
  pos += way
#print("pos={}".format(pos))

decoder = rotaryEncoder.decoder(pi, 24, 23, callback)
#print("Move clockwise")
eastMotor(N,100)
sleep(1)
print(decoder.tick)
decoder.levA = 0
decoder.levB = 0
decoder.tick = 0
#print("Move counterclockwise")
eastMotor(S,100)
sleep(1)
print(decoder.tick)
stop()
decoder.cancel()
pi.stop()


#stop()
#Shutdown
#pi.serial_close(sbt1)
#pi.serial_close(sbt2)
