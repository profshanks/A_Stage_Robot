#!/usr/bin/python3
import Adafruit_TCS34725_pigpio as Adafruit_TCS34725
import pigpio

pi = pigpio.pi('10.3.141.1')
mux = pi.i2c_open(1, 0x70)

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

# Set the multiplexer channels for the different sensors here (Adafruit TCA954$
    # For channel 0 use "1"         # For channel 4 use "16"
    # For channel 1 use "2"         # For channel 5 use "32"
    # For channel 2 use "4"         # For channel 6 use "64"
    # For channel 3 use "8"         # For channel 7 use "128"

sensor_1 = 2
sensor_2 = 8
sensor_3 = 128

# Now we create different objects for each sensor
pi.i2c_write_byte(mux, sensor_1)
tcs1 = Adafruit_TCS34725.TCS34725()

pi.i2c_write_byte(mux, sensor_2)
tcs2 = Adafruit_TCS34725.TCS34725()

pi.i2c_write_byte(mux, sensor_3)
tcs3 = Adafruit_TCS34725.TCS34725()

# MAIN PROGRAM
for i in range(1,1002):
    pi.i2c_write_byte(mux, sensor_1)
    r1, g1, b1, c1 = tcs1.get_raw_data()
    processData(r1,g1,b1,c1)

    pi.i2c_write_byte(mux, sensor_2)
    r2, g2, b2, c2 = tcs2.get_raw_data()
    processData(r2,g2,b2,c2)

    pi.i2c_write_byte(mux, sensor_3)
    r3, g3, b3, c3 = tcs3.get_raw_data()
    processData(r3,g3,b3,c3)

# Put the sensor chips back to low power sleep/disabled.
pi.i2c_write_byte(mux, sensor_1)
tcs1.disable()
pi.i2c_write_byte(mux, sensor_2)
tcs2.disable()
pi.i2c_write_byte(mux, sensor_3)
tcs3.disable()
