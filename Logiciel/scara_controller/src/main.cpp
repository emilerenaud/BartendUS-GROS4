#include <Arduino.h>
#include <cncShield.h>
#include <string.h>

cncShield* shield;

int state = 0;
int angle = 0;
float angleMotor[3] = {0,0,0};
float lastAngle[3] = {0,0,0};
void setupSerial(void);
void readSerial(void);

void setup() {
  // Serial.println("Code start here");
  setupSerial();
  shield = new cncShield;
  shield->enableMotor();
  // shield->motorX->moveTo(300);
  // shield->motorY->moveTo(-200);
  // shield->motorX->setSpeed(100);
  // shield->motorY->setSpeed(100);

}

void loop() {
  readSerial();
  if(shield->motorX->isMoving())
  {
    shield->motorX->update();
  }
  // else
  // {
  //   shield->motorX->moveTo(-300);
  // }
  // if(shield->motorY->isMoving())
  // {
  //   shield->motorY->update();
  // }
  // else
  // {
  //   shield->motorY->moveTo(200);
  // }
}

void setupSerial()
{
  Serial.begin(9600);
  Serial.setTimeout(100);
  Serial.flush();
}

void readSerial()
{
  String operatorString = " ";
  int aIndex,bIndex,zIndex;
  String aValue ="",bValue="",zValue="";
  String serialString = "";
  if(Serial.available())
  {
    String tempString = Serial.readStringUntil('\r\n');
    if(tempString[0] != 'G' || tempString[0] != 'M')
      Serial.flush();
    int indexOperator = tempString.indexOf(':');
    operatorString = tempString.substring(0,indexOperator);
    Serial.print(tempString);
    Serial.print("  ");
    if(operatorString[0] == 'G')
    {
      aIndex = tempString.indexOf(':A');
      bIndex = tempString.indexOf(':B',indexOperator+1);
      zIndex = tempString.indexOf(':Z',bIndex+1);
      if(aIndex != -1)
        aValue = tempString.substring(aIndex+1,bIndex-1);
      if(bIndex != -1)
        bValue = tempString.substring(bIndex+1,zIndex-1);
      if(zIndex != -1)
        zValue = tempString.substring(zIndex+1);

      switch(operatorString.substring(1).toInt())
      {
        case 0:
          shield->motorX->moveTo(aValue.toFloat());
          // shield->motorY->moveTo(bValue.toFloat());
          // shield->motorZ->moveTo(zValue.toFloat());
          serialString = "Angle set to : A=" + aValue + " B=" + bValue + " Z=" + zValue;
          Serial.println(serialString);
          break;
        case 1:
          int speedA = aValue.toInt();
          if(speedA <= 100 || speedA >= 0)
            shield->motorX->setSpeed(speedA);
          else
            shield->motorX->setSpeed(25);
          int speedB = bValue.toInt();
          if(speedB <= 100 || speedB >= 0)
            shield->motorY->setSpeed(speedB);
          else
            shield->motorY->setSpeed(25);
          int speedZ = zValue.toInt();
          if(speedZ <= 100 || speedZ >= 0)
            shield->motorZ->setSpeed(speedZ);
          else
            shield->motorZ->setSpeed(25);
          serialString = "Speed set to : A=" + aValue + " B=" + bValue + " Z=" + zValue;
          Serial.println(serialString);
          break;
          
        case 2:
          // code
          break;
      }
    }
    else if(operatorString[0] == 'M')
    {
      switch(operatorString.substring(1).toInt())
      {
        case 0:
          // code
          break;
        case 1:
          // code
          break;
      }
    }
  }
  
}