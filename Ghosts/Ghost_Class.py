from math import sin, cos, radians
import pigpio
from cardinalDirections import *


class Ghost:
    """
    Setup & drive functions for running Banquo & other polar-drive
    robots.

    Drive instructions headed to Sabertooth Motor Drivers are using
    Simplified Serial instructions (see Sabertooth documentation)

    Methods include:

    stop()
    drive(direction, speed)
    spin(direction, speed)
    closeSerial()
    """

    def __init__(self, address): 
        self.pi = pigpio.pi(address)
        #self.sbt1 = self.pi.serial_open("/dev/ttyAMA0", 9600)
        self.sbt1 = self.pi.serial_open("/dev/ttyAMA1", 9600)
        self.sbt2 = self.pi.serial_open("/dev/ttyS0", 9600)
        #self.sbt1 = self.pi.serial_open("/dev/ttyAMA3", 9600)
        #self.sbt1 = self.pi.serial_open("/dev/serial1", 9600)
        #self.sbt2 = self.pi.serial_open("/dev/serial0", 9600)
        
    def stop(self):
        self.pi.serial_write_byte(self.sbt1, 0)
        self.pi.serial_write_byte(self.sbt2, 0)

    def motor1(self, direction, speed):
        newSpeed = int(speed/100 * 63)  # Converts 0-100 scale to 0-63 scale
        if direction == 'South':
            newSpeed = newSpeed + 64
        elif direction == 'North':
            newSpeed = 64 - newSpeed
        self.pi.serial_write_byte(self.sbt1, newSpeed)
            
    def motor2(self, direction, speed):
        newSpeed = int(speed/100 * 63)
        if direction == 'West':
            newSpeed = newSpeed + 192
        elif direction == 'East':
            newSpeed = 191 - newSpeed
        self.pi.serial_write_byte(self.sbt1, newSpeed)
      
    def motor3(self, direction, speed):
        newSpeed = int(speed/100 * 63)
        if direction == 'West':
            newSpeed = newSpeed + 64
        elif direction == 'East':
            newSpeed = 64 - newSpeed
        self.pi.serial_write_byte(self.sbt2, newSpeed)
            
    def motor4(self, direction, speed):
        newSpeed = int(speed/100 * 63)
        if direction == 'South':
            newSpeed = newSpeed + 192
        elif direction == 'North':
            newSpeed = 191 - newSpeed
        self.pi.serial_write_byte(self.sbt2, newSpeed)

    def driveMotors(self, nsDIR, nsSPEED, ewDIR, ewSPEED):
        '''Sends instructions to motors based on compent-vector
            breakdown. This assumes straignt-line travel.'''
        self.motor1(nsDIR, nsSPEED)
        self.motor2(ewDIR, ewSPEED)
        self.motor3(ewDIR, ewSPEED)
        self.motor4(nsDIR, nsSPEED)

    def drive(self, direction, speed):
        '''Direction is N/S/E/W etc.
           NNW is an option too.
           So are polar coordinates such as 27 or 118.45.
           Speed is on a scale of 0-100.'''
        if direction in cardinalConversion:
            direction = cardinalConversion[direction]
            
        if direction < 90:
            direction = radians(direction)
            nSpeed = speed * cos(direction)
            eSpeed = speed * sin(direction)
            self.driveMotors(N, nSpeed, E, eSpeed)
            
        elif direction < 180:
            direction = 180 - direction      # Quadrant-specific adjustment
            direction = radians(direction)   # Convert to radians
            sSpeed = speed * cos(direction)  # Component vectors
            eSpeed = speed * sin(direction)
            self.driveMotors(S, sSpeed, E, eSpeed) # Drive instructions
            
        elif direction < 270:
            direction =  direction - 180
            direction = radians(direction)
            sSpeed = speed * cos(direction)
            wSpeed = speed * sin(direction)
            self.driveMotors(S, sSpeed, W, wSpeed)
            
        elif direction <= 360:
            direction = 360 - direction
            direction = radians(direction)
            nSpeed = speed * cos(direction)
            wSpeed = speed * sin(direction)
            self.driveMotors(N, nSpeed, W, wSpeed)
            
        else:
            print('Bad direction parameter!')
            

    def spin(self, direction, speed):
        '''Direction is CW or CCW.
           Speed is on a scale of 0-100.'''
        if direction == 'CW':
            self.motor1(S, speed)
            self.motor2(E, speed)
            self.motor3(W, speed)
            self.motor4(N, speed)

        elif direction == 'CCW':
            self.motor1(N, speed)
            self.motor2(W, speed)
            self.motor3(E, speed)
            self.motor4(S, speed)

        else:
            print('Bad direction parameter!')

    def closeSerial(self):
        self.pi.serial_close(self.sbt1)
        self.pi.serial_close(self.sbt2)

    

       
