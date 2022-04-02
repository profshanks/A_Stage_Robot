#!/usr/bin/python3

import pigpio
import Adafruit_TCS34725_pigpio as Adafruit_TCS34725

ip_Address = '10.3.141.249'
pi = pigpio.pi(ip_Address)
tcs1 = Adafruit_TCS34725.TCS34725(ip_Address)

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

r1, g1, b1, c1 = tcs1.get_raw_data()
processData(r1,g1,b1,c1)

tcs1.disable()
