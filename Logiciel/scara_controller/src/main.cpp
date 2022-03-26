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
void answerSerial(void);

void setup() {
  // Serial.println("Code start here");
  setupSerial();
  shield = new cncShield;
  shield->enableMotor();
}

void loop() {
  readSerial();
  shield->update();
  // shield->motorX->update();
  // shield->motorY->update();
  // shield->motorZ->update();
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
//
      switch(operatorString.substring(1).toInt())
      {
        case 0: //G0 Move to
          shield->motorA->moveTo(aValue.toFloat());
          shield->motorB->moveTo(bValue.toFloat());
          shield->setNewMouvement();
          // shield->motorZ->moveTo(zValue.toFloat());
          serialString = "Angle set to : A=" + aValue + " B=" + bValue; // + " Z=" + zValue;
          // Serial.println(serialString);
          break;
        case 1: //G1 Set Speed
          // int speedA = aValue.toInt();
          if(aValue.toInt() <= 100 || aValue.toInt() >= 0)
            shield->motorA->setMaxSpeed(aValue.toInt());
          else
            shield->motorA->setMaxSpeed(75);
          // int speedB = bValue.toInt();
          if(bValue.toInt() <= 100 || bValue.toInt() >= 0)
            shield->motorB->setMaxSpeed(bValue.toInt());
          else
            shield->motorB->setMaxSpeed(75);
          // int speedZ = zValue.toInt();
          if(zValue.toInt() <= 100 || zValue.toInt() >= 0)
            shield->motorZ->setMaxSpeed(zValue.toInt());
          else
            shield->motorZ->setMaxSpeed(75);
          serialString = "Speed set to : A=" + aValue + " B=" + bValue + " Z=" + zValue;
          // Serial.println(serialString);
          break;
          
        case 2: //G2 Home
          shield->startHoming();
          // Serial.println("Done");
          break;

        case 3: //G3 Control Z
            shield->motorZ->moveTo(zValue.toFloat());
            shield->setNewMouvement();
            // Serial.println(zValue.toFloat());
            // G3:Z40
          break;
        case 4: //G4 Control poignet
          shield->motorP->moveTo(aValue.toFloat());
          shield->setNewMouvement();
          // G4:A40
          break;
        case 5: //G5 Control Servo
          if(aValue.toInt() <= 180 || aValue.toInt() >= 0)
          {
            shield->moveServo(aValue.toInt());
            Serial.println("Done");
            // Serial.println("servo Write" + String(aValue));
          }
          break;

      }
    }
    else if(operatorString[0] == 'M')
    {
      switch(operatorString.substring(1).toInt())
      {
        case 0: // M0 open electro
          // Serial.println("Move servo 0");
          // shield->moveServo(0);
          shield->openElectro();
          answerSerial();
          break;
        case 1: // M1 close electro
        // Serial.println("Move servo 150");
          shield->closeElectro();
          answerSerial();
          // code
          break;
        case 3: 
          //
          break;
      }
    }
  }
  
}

void answerSerial()
{
  Serial.println("Done");
}