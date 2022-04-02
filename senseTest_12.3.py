#!/usr/bin/python3

try:
    import pigpio
except:
    import pip
    pip.main(['install', 'pigpio'])
import Adafruit_TCS34725_pigpio as Adafruit_TCS34725
from time import sleep
import sys

ip_Address = '10.3.141.249'
pi2 = pigpio.pi(ip_Address)

# This processes the data and reports it to the screen
def processData(r,g,b,c):
    print('r=' + str(r) + '; g=' + str(g) + '; b=' + str(b) + '; c=' + str(c))
    # Calculate color temperature using utility functions.  You might also want to
    # check out the colormath library for much more complete/accurate color functi$
    color_temp = Adafruit_TCS34725.calculate_color_temperature(r, g, b)

    # Calculate lux with another utility function.
    lux = Adafruit_TCS34725.calculate_lux(r, g, b)

    # Print out the values.
    col = ('Color: red={0} green={1} blue={2} clear={3}'.format(r, g, b, c))
    print(col)

    # Print out color temperature.
    if color_temp is None:
        print('Too dark to determine color temperature!')
    else:
        print('Color Temperature: {0} K'.format(color_temp))

    # Print out the lux.
    print('Luminosity: {0} lux'.format(lux))
    print()

sensor_1 = 4

M2Sp = 13				# set pwm2 pin on MD10-Hat
M1Sp = 12				# set pwm1 pin on MD10-hat
M2Dir = 24				# set dir2 pin on MD10-Hat
M1Dir = 26				# set dir1 pin on MD10-Hat

pwm = 100                            # set maximum motor speed
cut = 1
threshold = 70
ko = .2
clim = .5
i = 0

pi2.write(M1Dir, 0)
pi2.write(M2Dir, 0)

tcs1 = Adafruit_TCS34725.TCS34725(ip_Address)

r1, g1, b1, c1 = tcs1.get_raw_data()
processData(r1,g1,b1,c1)

'''
# This is the super-squiggly algorithm
while (b1/c1) < .4 :
    if c1 < 45:
        pi2.set_PWM_dutycycle(M1Sp, pwm * cut)
        pi2.set_PWM_dutycycle(M2Sp, pwm)

    else:
        pi2.set_PWM_dutycycle(M1Sp, pwm)
        pi2.set_PWM_dutycycle(M2Sp, pwm * cut)

    r1, g1, b1, c1 = tcs1.get_raw_data()
    processData(r1,g1,b1,c1)

'''
# This is the proportional-cut algorithm
while (b1/c1) < .4:
    if c1 < 15:
        print('Stop!')
        pi2.set_PWM_dutycycle(M1Sp, 0)
        pi2.set_PWM_dutycycle(M2Sp, 0)
        sys.exit()
    
    if c1 < threshold: # Turn Left
        i += 1
        offBy = (threshold - c1) * ko
        cut = (threshold-offBy)/threshold
        if (cut < clim):
            cut = .5
        if i > 5:
            cut = .45
        pi2.set_PWM_dutycycle(M1Sp, pwm * cut)
        pi2.set_PWM_dutycycle(M2Sp, pwm)

    else:  # Turn Right
        i = 0
        offBy = (c1 - threshold) * ko
        cut = abs((threshold-offBy)/threshold)
        if (cut < clim):
            cut = .5
        pi2.set_PWM_dutycycle(M1Sp, pwm)
        pi2.set_PWM_dutycycle(M2Sp, pwm * cut)

    r1, g1, b1, c1 = tcs1.get_raw_data()
    processData(r1,g1,b1,c1)

print('I see Blue!')
pi2.set_PWM_dutycycle(M1Sp, 0)
pi2.set_PWM_dutycycle(M2Sp, 0)
        
tcs1.disable()
