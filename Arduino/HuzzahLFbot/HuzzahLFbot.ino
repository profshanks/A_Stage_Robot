#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "Adafruit_TCS34725.h"
#include "utility/Adafruit_MS_PWMServoDriver.h"

Adafruit_TCS34725 tcs = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_2_4MS, TCS34725_GAIN_1X);
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
Adafruit_DCMotor *L_Motor = AFMS.getMotor(3);
Adafruit_DCMotor *R_Motor = AFMS.getMotor(4);

uint8_t i;
uint16_t r, g, b, c, colorTemp, lux;
  
int hi = 100;
int low = 35;
int threshold = 50;

void setup() {
  
  Serial.begin(9600);
  
  if (tcs.begin()) {
    Serial.println("Found sensor");
  } else {
    Serial.println("No TCS34725 found ... check your connections");
    while (1);
  }
  AFMS.begin();  // create with the default frequency 1.6KHz
  
  // Set the speed to start, from 0 (off) to 255 (max speed)
  L_Motor->setSpeed(150);
  L_Motor->run(FORWARD);
  // turn on motor
  L_Motor->run(RELEASE);

//AFMS.begin();  // create with the default frequency 1.6KHz
  
  // Set the speed to start, from 0 (off) to 255 (max speed)
  R_Motor->setSpeed(150);
  R_Motor->run(FORWARD);
  // turn on motor
  R_Motor->run(RELEASE);
}

void loop() {
    
  tcs.getRawData(&r, &g, &b, &c);
  Serial.print("C: "); Serial.print(c, DEC); Serial.print(" ");
  Serial.println(" ");

 if (c < threshold){
    L_Motor->setSpeed(low);
    R_Motor->setSpeed(hi);
  }
  else {
    L_Motor->setSpeed(hi);
    R_Motor->setSpeed(low);
  }
  R_Motor->run(FORWARD);
  L_Motor->run(FORWARD);
}
