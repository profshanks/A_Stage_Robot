#import pigpio
from time import sleep
import rotaryEncoder
from DirectionVariables import *
import Banquo_Class as bc

#PiSetup
bq = bc.Banquo('10.3.141.67')

#Function to calculate pulses
def callback(way):
  if (way == 1):
    pulses += abs(way)
    
#DecoderSetup
W_decoder = rotaryEncoder.decoder(bq.pi, 11, 9, callback)  # West Motor
E_decoder = rotaryEncoder.decoder(bq.pi, 24, 23, callback) # East Motor


def goStraight(motor1, motor2, direction, revs, speed, ppr, callback):
    pulses_rev = revs * ppr
    pulses_revhalf = (revs * ppr) / 2
    #E_decoder.pulses or (W_decoder.pulses or E_decoder.pulses)
    while E_decoder.pulses < pulses_rev:
      #when it reaches half of what the rev goal should be it should
      #start to slow down the speed
        if (W_decoder.pulses or E_decoder.pulses) != pulses_revhalf:
          if W_decoder.pulses > E_decoder.pulses:          
            motor1(direction, speed * .9)
            motor2(direction, speed)
          else:
            motor1(direction, speed)
            motor2(direction, speed * .9)
        else:
          motor1(direction, speed * .9)
          motor2(direction, speed * .9)
          
#    sleep(3)    
    bq.stop()
    print("pulses1: " + str(W_decoder.pulses))
    print("pulses2: " + str(E_decoder.pulses))
    print("What pulses should be: " + str(pulses_rev))
#    print("What pulses2 should be: " + str(pulses_rev2))
goStraight(bq.westMotor, bq.eastMotor, S, 5, 50, 189, callback)

W_decoder.cancel()
E_decoder.cancel()

#Close
bq.close_serial()
