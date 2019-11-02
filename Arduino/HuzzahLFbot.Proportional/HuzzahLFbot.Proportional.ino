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
  
double R_power;
double L_power;
double cut;
double cutPower = 7.0;
double target = 50;
double topSpeed = 60;

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
  Serial.print("C: "); Serial.print(c); Serial.print(" ");
  Serial.println(" ");

  cut = cutPower * (topSpeed * ((target-c)/target));

  if (c < target) {
    R_power = topSpeed;
    L_power = topSpeed - cut;
    if (L_power < 1){
      L_power = 0;
    }
  }
  else {
    R_power = topSpeed + cut;
    L_power = topSpeed;
    if (R_power < 1){
      R_power = 0;
    }
  }

  Serial.print("Cut: "); Serial.print(cut, DEC); Serial.print(" ");
  Serial.print("L_power: "); Serial.print(L_power, DEC); Serial.print(" ");
  Serial.print("R_power: "); Serial.print(R_power, DEC); Serial.print(" ");
  Serial.println(" ");
  
  L_Motor->setSpeed(L_power);
  R_Motor->setSpeed(R_power);

  R_Motor->run(FORWARD);
  L_Motor->run(FORWARD);
}
