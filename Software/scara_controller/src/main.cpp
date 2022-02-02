#include <Arduino.h>
#include <cncShield.h>

cncShield* shield;

int state = 0;
int angle = 0;
int tempAngle = 0;
void readSerial(void);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.setTimeout(1);
  // Serial.println("Code start here");
  shield = new cncShield;
  shield->enableMotor();
  shield->motorX->moveTo(90);
  shield->motorX->setSpeed(100);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  if(shield->motorX->isMoving())
  {
    shield->motorX->update();
  }
  // if(shield->motorX->isMoving())
  // {
  //   shield->motorX->update();
  // }
  // else
  // {
  //   readSerial();
  //   if(tempAngle != angle)
  //   {
  //     angle = tempAngle;
  //     shield->motorX->moveTo(angle);
  //   }
  // }
  // if(shield->motorX->isMoving())
  // {
  //   shield->motorX->update();
  // }
  // else
  // {
  //   shield->motorX->moveTo(-360);
  // }  
}

void readSerial()
{
  if(Serial.available())
  {
    tempAngle = Serial.readString().toFloat();
    Serial.print(tempAngle + 1);
  }
}