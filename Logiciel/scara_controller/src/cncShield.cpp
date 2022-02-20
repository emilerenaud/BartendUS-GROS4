#include <cncShield.h>

cncShield::cncShield()
{
    motorA = new Stepper(dirPinX_pin,stepPinX_pin,16,5.6);
    motorB = new Stepper(dirPinY_pin,stepPinY_pin,16,11.2);
    motorZ = new Stepper(dirPinZ_pin,stepPinZ_pin,16,20);

    pinMode(enPin_pin,OUTPUT);
    pinMode(endStopX_pin,INPUT_PULLUP);
    pinMode(endStopY_pin,INPUT_PULLUP);
    pinMode(endStopZ_pin,INPUT_PULLUP);
};



void cncShield::enableMotor()
{
    digitalWrite(enPin_pin,LOW);
    _enMotor = 1;
};

void cncShield::disableMotor()
{
    digitalWrite(enPin_pin,HIGH);
    _enMotor = 0;
};

void cncShield::update()
{
    if(_homing)
    {
        if(homing())
        {
            _homing = 0;
            Serial.println("Homing_Done");
        }
    }
    else if(motorA->isMoving() || motorB->isMoving() || motorZ->isMoving()) // do not update motor while homing
    {
        motorA->update(1);
        motorB->update(1);
        motorZ->update(1);
    }
};

bool cncShield::homing()
{
    switch(_homingSequence)
    {
        case 0: // prepare homing B joint
            motorB->setDirection(homingDirB);
            motorB->moveTo(-300);
            motorB->setSpeed(25);
            _homingSequence ++;
            // Serial.println("Step 0");
            break;
        case 1: // Move B until limit switch get pressed.
            motorB->update(0);
            if(this->getLimitSwitchB()) // 1=pressed
            {   
                // Serial.println("Step 1 Switch");
                motorB->setCurrentPosition(offset_B);
                _homingSequence ++;
            }
            break;
        case 2: // Prepare homing A joint + prepare to move joint B to 90.
            motorB->moveTo(90);
            motorA->setDirection(homingDirA);
            motorA->moveTo(-300);
            motorA->setSpeed(25);
            // Serial.println("Step 2");
            _homingSequence ++;
            break;
        case 3: // Move B joint to 90 and move joint A until limit switch get pressed.
            motorA->update(0);
            motorB->update(0);
            if(this->getLimitSwitchA())
            {
                motorA->setCurrentPosition(offset_A);
                // Serial.println("Step 3 switch");
            }
            if(!motorB->isMoving() && this->getLimitSwitchA())
            {
                // Serial.println("Step 3 end moving");
                motorB->setCurrentPosition(0);  // reset it at 0 because Tony want it like that.
                _homingSequence ++;
            }    
            break;
        case 4:
            motorA->moveTo(90);
            // Serial.println("Step 4");
            _homingSequence ++;
            break;
        case 5:
            motorA->update(0);
            if(!motorA->isMoving())
            {
                // Serial.println("Step 5 last");
                _homing = 0;
                _homingSequence = 0;
                return 1;
            }
            break;
    }
    return 0;
};

 void cncShield::startHoming()
 {
     _homing = 1;
     _homingSequence = 0;
 };

bool cncShield::areMotorEnabled()
{
    return _enMotor;
};

bool cncShield::getLimitSwitchA()
{
    return !digitalRead(endStopX_pin);
};

bool cncShield::getLimitSwitchB()
{
    return !digitalRead(endStopY_pin);
};

bool cncShield::getLimitSwitchZ()
{
    return !digitalRead(endStopZ_pin);
};
