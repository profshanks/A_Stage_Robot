import pigpio
from time import sleep

pi = pigpio.pi('10.3.141.51')
print("Set up PI")
motor1 = pi.serial_open("/dev/ttyAMA3", 9600)
print("Set up motor1")
print(motor1)
pi.serial_write_byte(motor1, 127)
print("Full Speed")
sleep(3)

pi.serial_write_byte(motor1, 64)
print("Stop")
print("All Done!!")

