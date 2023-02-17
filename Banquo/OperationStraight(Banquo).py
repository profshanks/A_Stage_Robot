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
    pulse += abs(way)
    
#DecoderSetup
#N_decoder = rotaryEncoder.decoder(pi, 17, 27, callback) # North Motor
W_decoder = rotaryEncoder.decoder(pi, 11, 9, callback)  # West Motor
#S_decoder = rotaryEncoder.decoder(pi, 16, 20, callback) # South Motor
E_decoder = rotaryEncoder.decoder(pi, 24, 23, callback) # East Motor


def goStraight(motor1, motor2, direction, revs, speed, wind_down):
    pulses_rev = 5640
    wd_pulses = wind_down * pulses_rev
    cut_able_speed1 = speed - 10
    cut_able_speed2 = speed - 10

    while (E_decoder.pulses and W_decoder.pulses) < pulses_rev:
        if (E_decoder.pulses and W_decoder.pulses) < (pulses_rev - wd_pulses):
            motor1(N, speed)
            motor2(N, speed)
        else:
            pulses_to_go1 = pulses_rev - W_decoder.pulses
            pct_wind_down_remaining1 = pulses_to_go1/wd_pulses
            cut_speed1 = speed - ((1 - pct_wind_down_remaining1) * cut_able_speed1)
            pulses_to_go2 = pulses_rev - E_decoder.pulses
            pct_wind_down_remaining2 = pulses_to_go2/wd_pulses
            cut_speed2 = speed - ((1 - pct_wind_down_remaining2) * cut_able_speed2)
            print(cut_speed1)
            print(cut_speed2)
            eastMotor(N, cut_speed1)
            westMotor(N, cut_speed2)
    stop()
    revs1 = W_decoder.pulses/pulses_rev
    revs2 = E_decoder.pulses/pulses_rev
    print("pulses after: " + str(W_decoder.pulses))
    print("West revs are: " + str(revs1))
    print("pulses after: " + str(E_decoder.pulses))
    print("East revs are: " + str(revs2))
goStraight(westMotor, eastMotor, N, 30, 100, 3)

W_decoder.cancel
E_decoder.cancel

#Close
pi.serial_close(sbt1)
pi.serial_close(sbt2)
