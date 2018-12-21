import pigpio
from time import sleep

pi2 = pigpio.pi('10.3.141.1')

M2Sp = 13				# set pwm2 pin on MD10-Hat
M1Sp = 12				# set pwm1 pin on MD10-hat
M2Dir = 24				# set dir2 pin on MD10-Hat
M1Dir = 26				# set dir1 pin on MD10-Hat

Max = 250                               # set maximum motor speed

pi2.write(M1Dir, 0)
pi2.write(M2Dir, 0)

print("Whoa!!!")
pi2.set_PWM_dutycycle(M1Sp, 0)
pi2.set_PWM_dutycycle(M2Sp, 0)
sleep(0.01)

print("All Done!!")
'''
    

for j in range(1,10):
    for i in range(1,255):
        pi2.set_PWM_dutycycle(17, i)
        time.sleep(0.01)


       
import RPi.GPIO as GPIO			# using Rpi.GPIO module
GPIO.setmode(GPIO.BCM)			# GPIO numbering
GPIO.setwarnings(False)			# enable warning from GPIO

GPIO.setup(AN2, GPIO.OUT)		# set pin as output
GPIO.setup(AN1, GPIO.OUT)		# set pin as output
GPIO.setup(DIG2, GPIO.OUT)		# set pin as output
GPIO.setup(DIG1, GPIO.OUT)		# set pin as output
sleep(1)				# delay for 1 seconds
p1 = GPIO.PWM(AN1, 100)			# set pwm for M1
p2 = GPIO.PWM(AN2, 100)			# set pwm for M2

try:					
  while True:

   print "Left"				# display "Forward" when programe run
   GPIO.output(DIG1, GPIO.HIGH)		# set DIG1 as HIGH, M1B will turn ON
   GPIO.output(DIG2, GPIO.LOW)		# set DIG2 as HIGH, M2B will turn ON
   p1.start(100)			# set speed for M1 at 100%
   p2.start(100)			# set speed for M2 at 100%
   sleep(2)				#delay for 2 second
   print "Forward"
   GPIO.output(DIG1, GPIO.LOW)          # set DIG1 as LOW, to control direction
   GPIO.output(DIG2, GPIO.LOW)          # set DIG2 as LOW, to control direction
   p1.start(100)                        # set speed for M1 at 100%
   p2.start(100)                        # set speed for M2 at 100%
   sleep(2)                             #delay for 2 second

   print "Backward"
   GPIO.output(DIG1, GPIO.HIGH)         # set DIG1 as HIGH, to control direction
   GPIO.output(DIG2, GPIO.HIGH)         # set DIG2 as HIGH, to control direction
   p1.start(100)                        # set speed for M1 at 100%
   p2.start(100)                        # set speed for M2 at 100%
   sleep(2)                             #delay for 2 second

   print "Right"
   GPIO.output(DIG1, GPIO.LOW)       
   GPIO.output(DIG2, GPIO.HIGH)    
   p1.start(100)                     
   p2.start(100)                   
   sleep(2)                        

   print "STOP"
   GPIO.output(DIG1, GPIO.LOW)          # Direction can ignore
   GPIO.output(DIG2, GPIO.LOW)          # Direction can ignore
   p1.start(0)                          # set speed for M1 at 0%
   p2.start(0)                          # set speed for M2 at 0%
   sleep(3)                             #delay for 3 second


except:					# exit programe when keyboard interupt
   p1.start(0)				# set speed to 0
   p2.start(0)				# set speed to 0
# Control+x to save file and exit
'''
