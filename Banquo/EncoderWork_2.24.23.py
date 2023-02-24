#Date February 24th 2023

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
    rev_goal = 2
    pulses_goal = revs * ppr
    revs_goal = rev_goal * ppr
    while (W_decoder.pulses and E_decoder.pulses) < pulses_goal:
        motor1(direction, speed)
        motor2(direction, speed)
        if E_decoder.pulses > W_decoder.pulses: # if (east * 1.12) > west:        
            motor1(direction, speed * 2)
            motor2(direction, speed)
        else:
            motor1(direction, speed)
            motor2(direction, speed * .5)
    bq.stop()
    print("pulses1: " + str(W_decoder.pulses))
    print("pulses2: " + str(E_decoder.pulses))

goStraight(bq.westMotor, bq.eastMotor, N, 2, 20, 189, callback)

W_decoder.cancel()
E_decoder.cancel()

#Close
bq.close_serial()
