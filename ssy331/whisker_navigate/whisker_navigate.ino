#include <Servo.h>

Servo servoLeft;
Servo servoRight;

#define PI 3.1415926535897932384626433832795

const int servoLeftPin = 13;
const int servoRightPin = 12;
const int piezoPin = 4;

const float msPermm = 6.1;
const int wheelBase = 107;

const int wLeftPin = 5;
const int wRightPin = 7;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(wLeftPin, INPUT);
  pinMode(wRightPin, INPUT);
  servoLeft.attach(servoLeftPin);
  servoRight.attach(servoRightPin);
  stopWheel(1000);
}

void loop() {
  // put your main code here, to run repeatedly:
  byte wLeft = digitalRead(wLeftPin);
  byte wRight = digitalRead(wRightPin);
  //Serial.print(wLeft);
  //Serial.println(wRight);
  //delay(100);
  //moveDist(100, 100, 10);
  if (wLeft == 0 and wRight == 0) {
          moveDist(-100, -100, 200);
          turnAngleBoth(180);

    }
  else if (wLeft == 0) {
      moveDist(-100, -100, 100);
      turnAngleBoth(45);

   } else if (wRight == 0) {
     moveDist(-100, -100, 100);
     
      turnAngleBoth(-45);

    }
     moveDist(100, 100, 10);

   
  
}

void stopWheel(int msTime)
{
  servoLeft.writeMicroseconds(1500);   // Set Left servo speed
  servoRight.writeMicroseconds(1500); // Set right servo speed
  delay(msTime);
}

void moveDist(int speedLeft, int speedRight, int mm)
{
  servoLeft.writeMicroseconds(1500 + speedLeft);   // Set Left servo speed
  servoRight.writeMicroseconds(1500 - speedRight); // Set right servo speed

  delay(int(msPermm*mm));                                   // Delay for msTime
}

void turnAngleOne(int ang)
{
  int circleDist = ((PI*abs(ang))/360)*wheelBase*2;
  if (ang < 0) {
      moveDist(0, 200, circleDist);
    } else {
        moveDist(200, 0, circleDist);

      }
  }

void turnAngleBoth(int ang)
{
    int circleDist = ((PI*abs(ang))/360)*wheelBase;
    if (ang < 0) {
      moveDist(-200, 200, circleDist);
    } else {
            moveDist(200, -200, circleDist);
    }
  }
