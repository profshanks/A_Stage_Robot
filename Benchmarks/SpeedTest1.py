import pigpio
from time import sleep

pi2 = pigpio.pi('10.3.141.1')

M2Sp = 13				# set pwm2 pin on MD10-Hat
M1Sp = 12				# set pwm1 pin on MD10-hat
M2Dir = 24				# set dir2 pin on MD10-Hat
M1Dir = 26				# set dir1 pin on MD10-Hat

topSpeed = 255                               # set maximum motor speed

pi2.write(M1Dir, 0)
pi2.write(M2Dir, 0)

print("Go")

pi2.set_PWM_dutycycle(M1Sp, topSpeed)
pi2.set_PWM_dutycycle(M2Sp, topSpeed)

sleep(10.0)

print("Stop")
pi2.set_PWM_dutycycle(M1Sp, 0)
pi2.set_PWM_dutycycle(M2Sp, 0)

print("All Done!!")

