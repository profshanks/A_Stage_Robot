import pigpio
from time import sleep
import rotaryEncoder
#from SetupImports import 
from DirectionVariables import *
import ControlFunctions as cf

#i want to run the motor at the lowest and highest speed at 60 seconds to
#see how many revs i get

bq = cf.Banquo('10.3.141.67')
#pi = pigpio.pi('10.3.141.67')
#sbt1 = pi.serial_open("/dev/ttyAMA1", 9600)
#sbt2 = pi.serial_open("/dev/serial0", 9600)
#revs = 0
#global pulses
#pulses = 0


def callback(way):
  if (way == 1):
    pulses += abs(way)

    
N_decoder = rotaryEncoder.decoder(bq.pi, 17, 27, callback) # North Motor
W_decoder = rotaryEncoder.decoder(bq.pi, 11, 9, callback)  # West Motor
S_decoder = rotaryEncoder.decoder(bq.pi, 16, 20, callback) # South Motor
E_decoder = rotaryEncoder.decoder(bq.pi, 24, 23, callback) # East Motor

print("pulses before: " + str(W_decoder.pulses))
W_decoder.levA = 0
W_decoder.levB = 0
W_decoder.tick = 0
#lowest speed 10
#revs are 12 maybe ~13

def run_for_revs(motor, direction, speed, encoder, ppr, revs, wind_down):
    pulse_goal = revs * ppr
    wd_pulses = wind_down * ppr
    cut_able_speed = speed - 10
    
    while encoder.pulses < pulse_goal:
        if encoder.pulses < (pulse_goal - wd_pulses):
            motor(direction, speed)                    
        else:
            pulses_to_go = pulse_goal - encoder.pulses
            pct_wind_down_remaining = pulses_to_go/wd_pulses
            cut_speed = speed - ((1 - pct_wind_down_remaining) * cut_able_speed)
            motor(direction, cut_speed)

    bq.stop()
    revs = encoder.pulses/pulses_per_rev
    print("pulses after: " + str(encoder.pulses))
    print("revs are: " + str(revs))

pulses_per_rev = 188
rev_goal = 10
speed = 100

run_for_revs(bq.southMotor, E, 100, S_decoder, 188, 10, 3)

W_decoder.cancel()
bq.close_serial()

'''
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
'''
# close 
#pi.serial_close(sbt1)
#pi.serial_close(sbt2)
