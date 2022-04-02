
import pigpio
from time import sleep
import Adafruit_TCS34725_pigpio as Adafruit_TCS34725

# This processes the data and reports it to the screen
def processData(r,g,b,c):
    #print('r=' + str(r) + '; g=' + str(g) + '; b=' + str(b) + '; c=' + str(c))
    # Calculate color temperature using utility functions.  You might also want to
    # check out the colormath library for much more complete/accurate color functi$
    color_temp = Adafruit_TCS34725.calculate_color_temperature(r, g, b)

    # Calculate lux with another utility function.
    lux = Adafruit_TCS34725.calculate_lux(r, g, b)

    # Print out the values.
    col = ('Color: red={0} green={1} blue={2} clear={3}'.format(r, g, b, c))
    #print(col)
    '''
    # Print out color temperature.
    if color_temp is None:
        print('Too dark to determine color temperature!')
    else:
        print('Color Temperature: {0} K'.format(color_temp))

    # Print out the lux.
    print('Luminosity: {0} lux'.format(lux))
    print()
    '''

def grabColorData():
    pi.i2c_write_byte(mux, sensor_1)
    r1, g1, b1, c1 = tcs1.get_raw_data()
    processData(r1,g1,b1,c1)
    
    pi.i2c_write_byte(mux, sensor_2)
    r2, g2, b2, c2 = tcs2.get_raw_data()
    processData(r2,g2,b2,c2)
    
    pi.i2c_write_byte(mux, sensor_3)
    r3, g3, b3, c3 = tcs3.get_raw_data()
    processData(r3,g3,b3,c3)

    pi.i2c_write_byte(mux, sensor_4)
    r4, g4, b4, c4 = tcs4.get_raw_data()
    processData(r4,g4,b4,c4)

    return (r1,g1,b1,c1,r2,g2,b2,c2,r3,g3,b3,c3,r4,g4,b4,c4)

ip_Address = '10.3.141.249'
pi = pigpio.pi(ip_Address)
mux = pi.i2c_open(1, 0x70)
print('Mux: ' + str(mux))

# Set the multiplexer channels for the different sensors here (Adafruit TCA954$
    # For channel 0 use "1"         # For channel 4 use "16"
    # For channel 1 use "2"         # For channel 5 use "32"
    # For channel 2 use "4"         # For channel 6 use "64"
    # For channel 3 use "8"         # For channel 7 use "128"

sensor_1 = 1
sensor_2 = 2
sensor_3 = 16
sensor_4 = 32
sensorList = [4, 8, 16 ,32]

# Now we create different objects for each sensor
pi.i2c_write_byte(mux, sensor_1)
tcs1 = Adafruit_TCS34725.TCS34725(ip_Address)

pi.i2c_write_byte(mux, sensor_2)
tcs2 = Adafruit_TCS34725.TCS34725(ip_Address)

pi.i2c_write_byte(mux, sensor_3)
tcs3 = Adafruit_TCS34725.TCS34725(ip_Address)

pi.i2c_write_byte(mux, sensor_4)
tcs4 = Adafruit_TCS34725.TCS34725(ip_Address)

M2Sp = 13				# set pwm2 pin on MD10-Hat
M1Sp = 12				# set pwm1 pin on MD10-hat
M2Dir = 24				# set dir2 pin on MD10-Hat
M1Dir = 26				# set dir1 pin on MD10-Hat
forward = 0
reverse = 1

clear = (20,20,20,20)
topSpeed = 140                             # set maximum motor speed
cut = .5

pi.write(M1Dir, forward)
pi.write(M2Dir, forward)

#for i in range(155):
while clear[1] > 10:
    data = grabColorData()
    clear = (data[3], data[7], data[10], data[13])
    print(clear[1])

    if clear[0] > 40:  # Hard Right!
        print("danger")
        pi.set_PWM_dutycycle(M1Sp, topSpeed * 1.3)
        pi.write(M2Dir, reverse)
        pi.set_PWM_dutycycle(M2Sp, topSpeed * .5)
    
    if clear[1] > 35:  # Turn Right
        pi.set_PWM_dutycycle(M1Sp, topSpeed)
        pi.write(M2Dir, forward)
        pi.set_PWM_dutycycle(M2Sp, topSpeed * cut)
        #sleep(0.01)
    else:              # Turn Left
        pi.set_PWM_dutycycle(M1Sp, topSpeed * cut)
        pi.write(M2Dir, forward)
        pi.set_PWM_dutycycle(M2Sp, topSpeed)
        #sleep(0.01)

print("Stop")
pi.set_PWM_dutycycle(M1Sp, 0)
pi.set_PWM_dutycycle(M2Sp, 0)


# Put the sensor chips back to low power sleep/disabled.
pi.i2c_write_byte(mux, sensor_1)
tcs1.disable()
pi.i2c_write_byte(mux, sensor_2)
tcs2.disable()
pi.i2c_write_byte(mux, sensor_3)
tcs3.disable()
pi.i2c_write_byte(mux, sensor_4)
tcs4.disable()
'''
for sen in sensorList:
    pi.i2c_write_byte(mux, sen)
    pi.i2c_close(sensor)
    sensor -=1
'''
pi.i2c_close(mux)

print("All Done!!")
