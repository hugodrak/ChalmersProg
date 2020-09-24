#include <Servo.h>

Servo servoLeft;
Servo servoRight;

#define PI 3.1415926535897932384626433832795

const int servoLeftPin = 13;
const int servoRightPin = 12;
const int piezoPin = 4;

const float msPermm = 6.1;
const int wheelBase = 107;
int notes [] = {1568, 1568, 1318, 1318, 1568, 1568, 1318, 1318, 1397, 1397, 1175, 1175, 1568, 1568, 1318, 1318};

void setup() {

  Serial.begin(9600);
  servoLeft.attach(servoLeftPin);
  servoRight.attach(servoRightPin);
  stopWheel(1000);
  
  moveDist(200, 200, 200);//200
  turnAngleBoth(112);
  moveDist(200, 200, 540); //540
  turnAngleBoth(-112);
  moveDist(200, 200, 200); //200
  stopWheel(10);
  // PLAY MELODY
  for (int i=0;i<15;i++) {
    tone(piezoPin, notes[i], 400);
    delay(400);
  }
  turnAngleBoth(180);
  moveDist(200, 200, 200);//200
  turnAngleBoth(112);
  moveDist(200, 200, 540); //540
  turnAngleBoth(-112);
  moveDist(200, 200, 200); //200
  
  servoLeft.detach();
  servoRight.detach();
 
}

void loop() {
  // put your main code here, to run repeatedly:

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
