from DirectionVariables import *
#from SetupImports import *
from math import sin, cos, radians
import pigpio

class Banquo:
    
    '''Class to setup and run a Banquo-style robot with 4 independent
        motors w/encoders, serviced by two Sabertooth motor drivers.'''

    def __init__(self, ip_address):
        
        '''
        Instantiate the class by setting up objects for the pi, the two
        Sabertooth motor drivers etc.
        '''
        
        self.pi = pigpio.pi(ip_address)
        self.sbt1 = self.pi.serial_open("/dev/ttyAMA1", 9600)
        self.sbt2 = self.pi.serial_open("/dev/serial0", 9600)
    

    def northMotor(self, direction, speed):
        newSpeed = int(speed/100 * 63)
        if direction == 'West': 
            newSpeed = newSpeed + 192
        elif direction == 'East': 
            newSpeed = 191 - newSpeed
        self.pi.serial_write_byte(self.sbt1, newSpeed)

    def southMotor(self, direction, speed):
        newSpeed = int(speed/100 * 63)
        if direction == 'East': 
            newSpeed = newSpeed + 64
        elif direction == 'West':
            newSpeed = 64 - newSpeed
        self.pi.serial_write_byte(self.sbt2, newSpeed)
        
    def eastMotor(self, direction, speed):
        newSpeed = int(speed/100 * 63)
        if direction == 'South':
            newSpeed = newSpeed + 64
        elif direction == 'North':
            newSpeed = 64 - newSpeed
        self.pi.serial_write_byte(self.sbt1, newSpeed)
        
    def westMotor(self, direction, speed):
        newSpeed = int(speed/100 * 63)
        if direction == 'North':
            newSpeed = newSpeed + 192
        elif direction == 'South':
            newSpeed = 191 - newSpeed
        self.pi.serial_write_byte(self.sbt2, newSpeed)

    def North_South(self, direction, speed):
        self.eastMotor(direction,speed)
        self.westMotor(direction,speed)

    def West_East(self, direction, speed):
        self.northMotor(direction,speed)
        self.southMotor(direction,speed)

    def drive(self, direction, speed):
        '''This function converts a direction into degrees.
           You can use the following variables N,S,E,W... or 0,90,180...
           Your speed must be between the intervals 0-100, 0 being the slowest and 100 the fastest.'''
        if direction in convert:
            direction = convert[direction]
        if direction < 90:
            direction = radians(direction)
            NS_Component = cos(direction) * speed
            WE_Component = sin(direction) * speed
            self.North_South(N,NS_Component)
            self.West_East(E,WE_Component)
        elif direction < 180:
            direction = 180 - direction        
            direction = radians(direction)
            NS_Component = cos(direction) * speed
            WE_Component = sin(direction) * speed
            self.North_South(S,NS_Component)
            self.West_East(E,WE_Component)
        elif direction < 270:
            direction = direction - 180        
            direction = radians(direction)
            NS_Component = cos(direction) * speed
            WE_Component = sin(direction) * speed
            self.North_South(S,NS_Component)
            self.West_East(W,WE_Component)

        elif direction <= 360:
            direction = 360 - direction        
            direction = radians(direction)
            NS_Component = cos(direction) * speed
            WE_Component = sin(direction) * speed
            self.North_South(N,NS_Component)
            self.West_East(W,WE_Component)
        else:
            print("Error")

    def stop(self):
        self.pi.serial_write_byte(self.sbt1, 0)
        self.pi.serial_write_byte(self.sbt2, 0)

    def close_serial(self):
        self.pi.serial_close(self.sbt1)
        self.pi.serial_close(self.sbt2)
    
