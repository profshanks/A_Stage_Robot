import pigpio
pi = pigpio.pi('10.3.141.56')
#sbt1 = pi.serial_open("/dev/ttyAMA1", 9600)
sbt1 = pi.serial_open("/dev/serial0", 9600)

F = "forward"
R = "reverse"

