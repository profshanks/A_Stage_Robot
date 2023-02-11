from time import sleep
# from gpiozero import DistanceSensor

import pigpio

from time import sleep

#########
# sETUP #
#########

ip_Address = '10.3.141.1'
pi = pigpio.pi(ip_Address) # Sets up RPi as pigpio object

