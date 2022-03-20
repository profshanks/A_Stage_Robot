from time import sleep
import sys
import struct

import pigpio
import Adafruit_TCS34725_pigpio as Adafruit_TCS34725

# Sensor Variables
COMMAND = 0x80
ATIME = 0x01
ITIME = 0xFF
GAIN = 0x01
CONTROL = 0x0F
ENABLE = 0x00
ENABLE_AEN = 0x02
ENABLE_PON = 0x01

colorRegisters = [0x16, 0x18, 0x1A, 0x14]

# Set the multiplexer channels for the different sensors here (Adafruit TCA954$
    # For channel 0 use "1"         # For channel 4 use "16"
    # For channel 1 use "2"         # For channel 5 use "32"
    # For channel 2 use "4"         # For channel 6 use "64"
    # For channel 3 use "8"         # For channel 7 use "128"

sensorList = [1, 2]


# LED variables

red = 10
green = 27
blue = 17
RGB = [red, green, blue]

RED = [0, 255, 255]
GREEN = [255, 0, 255]
BLUE = [255, 255, 0]
YELLOW = [0, 50, 255]
ORANGE = [0, 200, 255]
PURPLE = [225, 255, 0]
WHITE = [0, 0, 0]

def setUpSensors(pi, mux, sensorList):
    for sen in sensorList:
        pi.i2c_write_byte(mux, sen)
        sensor= pi.i2c_open(1, 0x29)

        # Set Integration Time
        pi.i2c_write_byte_data(sensor, (COMMAND | ATIME), ITIME)

        # Set Gain
        pi.i2c_write_byte_data(sensor, (COMMAND | CONTROL), GAIN)

        # Enable sensor
        pi.i2c_write_byte_data(sensor, (COMMAND | ENABLE), ENABLE_PON)
        sleep(0.01)
        pi.i2c_write_byte_data(sensor, (COMMAND | ENABLE), (ENABLE_PON | ENABLE_AEN))
    return sensor
    
def getSensorData(pi, mux, sensorList, sensor):
    """ Pulls sensor data from the registers on the chip.

        Returns a list ('data') with readings for r/g/b/c on all
                three sensors.

        data[0] = r1    data[4] = r2    data[8] = r3    data[12] = r4
        data[1] = g1    data[5] = g2    data[9] = g3    data[13] = g4
        data[2] = b1    data[6] = b2    data[10] = b3   data[14] = b4
        data[3] = c1    data[7] = c2    data[11] = c3   data[15] = c4
        """
    data = []
    for s in sensorList:
        pi.i2c_write_byte(mux, s)
        for reg in colorRegisters:
            (c, d) = pi.i2c_read_i2c_block_data(sensor,
                                                (COMMAND | reg), 2)
            #print(c, d)
            neat = struct.unpack('H'*1, d)
            data.append(neat[0])
    return data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]

def shutdownSensors(pi, mux, sensorList, sensor):
    for sen in sensorList:
        pi.i2c_write_byte(mux, sen)
        pi.i2c_close(sensor)
        sensor -=1

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

def blinkMe(cycles):
    for i in range(cycles, time):
        pi.set_PWM_dutycycle(red, 0)
        sleep(time)
        pi.set_PWM_dutycycle(red, 255)
        sleep(time)
        pi.set_PWM_dutycycle(green, 0)
        sleep(time)
        pi.set_PWM_dutycycle(green, 255)
        sleep(time)
        pi.set_PWM_dutycycle(blue, 0)
        sleep(time)
        pi.set_PWM_dutycycle(blue, 255)
        sleep(time)
        pi.set_PWM_dutycycle(red, 0)
        pi.set_PWM_dutycycle(green, 0)
        pi.set_PWM_dutycycle(blue, 0)
        sleep(time)
        pi.set_PWM_dutycycle(red, 255)
        pi.set_PWM_dutycycle(green, 255)
        pi.set_PWM_dutycycle(blue, 255)
        sleep(time)    

def LED_on(pi, color, intensity=100):
    intensity = (intensity/100)
    for i in range(0, 3):
        color[i] = 255 - color[i]
        color[i] = color[i] * intensity
        color[i] = 255 - color[i]
    
    for i in range(0, 3):
        pi.set_PWM_dutycycle(RGB[i], color[i])

def LED_off(pi):
    for i in range(0, 3):
        pi.set_PWM_dutycycle(RGB[i], 255)
    
