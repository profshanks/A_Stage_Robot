#!/usr/bin/python3

import time
#import board
import pigpio
from adafruit_motorkit_pigpio import MotorKit

ip_Address = '10.3.141.249'
pi = pigpio.pi(ip_Address)

kit = MotorKit(ip_Address)

kit.motor1.throttle = .7
kit.motor4.throttle = .7

time.sleep(2.0)

kit.motor1.throttle = -.7
kit.motor4.throttle = -.7

time.sleep(2.0)

kit.motor1.throttle = 0
kit.motor4.throttle = 0
