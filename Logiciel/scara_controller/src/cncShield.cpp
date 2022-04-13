#include <cncShield.h>

cncShield::cncShield()
{
    motorA = new Stepper(dirPinX_pin,stepPinX_pin,8,11.2);
    motorB = new Stepper(dirPinY_pin,stepPinY_pin,8,5.6);
    // motorB = new Stepper(dirPinP_pin,stepPinP_pin,16,1);
    motorZ = new Stepper(dirPinZ_pin,stepPinZ_pin,2,20);
    motorP = new Stepper(dirPinP_pin,stepPinP_pin,16,1);
    motorP->setSpeed(50);
    motorP->setMaxSpeed(50);
    motorZ->setSpeed(70);
    motorZ->setMaxSpeed(70);
    
    for(int i=0; i<6; i++)
    {
        pompeTab[i] = new Pompe(pompe_pin[i]);
    }
    // pompe1 = new Pompe(pompe_pin_1);
    servoShaker = new Servo();
    servoShaker->attach(SpnEn);
    servoShaker->write(10);
    pinMode(Electro_pin,OUTPUT);
    openElectro();
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

void cncShield::openElectro()
{
    digitalWrite(Electro_pin,LOW);
};

void cncShield::closeElectro()
{
    digitalWrite(Electro_pin,HIGH);
};

void cncShield::update()
{
    // pompe1->update();
    for(int i =0; i<6; i++)
    {
        pompeTab[i]->update();
    }
    // int test = 0;
    if(_homing)
    {
        if(homing())
        {
            _homing = 0;
            _homingSequence = 0;
            Serial.println("Done");
        }
    }
    else if(_newMouvement)
    {
        if(motorA->isMoving() || motorB->isMoving() || motorZ->isMoving() || motorP->isMoving()) // do not update motor while homing
        {
            motorA->update(1);
            motorB->update(1);
            motorZ->update(0);
            motorP->update(0);
        }
        else
        {
            Serial.println("Done");
            _newMouvement = 0;
        }
    }
    else if(_shake)
    {

        if(motorP->isMoving())
        {
            motorP->update(0);
        }
        else if(!_shakeDone)
        {
            shake();
        }
        else
        {
            Serial.println("Done");
            _shake = 0;
            _shakeDone = 0;
        }
    }
    else if(_verser)
    {
        if(motorZ->isMoving() || motorP->isMoving())
        {
            motorZ->update(0);
            motorP->update(0);
        }
        else if(!_verserDone)
        {
            verser();
        }
        else
        {
            Serial.println("Done");
            _verser = 0;
            _verserDone = 0;
        }
    }
    
};

bool cncShield::homing()
{
    switch(_homingSequence)
    {
        case 0: // prepare homing B joint
            motorZ->moveTo(-250);
            // motorZ->setSpeed(60);
            motorB->setDirection(homingDirB);
            motorB->moveTo(-300);
            motorB->setSpeed(60);
            _homingSequence ++;
            // Serial.println("Step 0");
            break;
        case 1: // Move B until limit switch get pressed.
            // motorB->update(0);
            // motorZ->update(0);
            if(this->getLimitSwitchZ())
            {
                motorZ->setCurrentPosition(0.0);
            }
            else
            {
                motorZ->update(0);
            }
            if(this->getLimitSwitchB())
            {
                motorB->setCurrentPosition(offset_B);
            }
            else
            {
                motorB->update(0);
            }
            if(!motorB->isMoving() && !motorZ->isMoving()) // 1=pressed
            {   
                // Serial.println("Step 1 Switch");
                // motorB->setCurrentPosition(offset_B);
                _homingSequence ++;
            }
            break;
        case 2: // Prepare homing A joint + prepare to move joint B to 90.
            motorB->moveTo(0);
            motorA->setDirection(homingDirA);
            motorA->moveTo(300);
            motorA->setSpeed(50);
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
                motorA->setCurrentPosition(offset_A);
                motorB->setCurrentPosition(0);  // reset it at 0 because Tony want it like that.
                _homingSequence ++;
            }    
            break;
        case 4:
            // motorA->setDirection(-1);
            motorA->moveTo(90);
            // Serial.println("Step 4");
            _homingSequence ++;
            break;
        case 5:
            motorA->update(0);
            if(!motorA->isMoving())
            {
                // Serial.println("Step 5 last");
                // _homing = 0;
                _homingSequence = 0;
                // Serial.println("Done");
                return 1;
            }
            break;
    }
    return 0;
};

void cncShield::startVerser(int sens)
{
    _verser = 1;
    _sensVerser = sens;
};

void cncShield::startShake()
{
    _shake = 1;
};

void cncShield::shake()
{
    if(!_initShake)
    {
        moveServo(0);
        motorP->setMaxSpeed(50);
        motorP->setSpeed(50);
        _compteurShake = 0;
        _initShake = 1;
    }
    if(_compteurShake >= 6)
    {
        motorP->moveTo(0);
        _compteurShake = 0;
        _initShake = 0;
        _shakeDone = 1;
    }
    else if(_compteurShake&0x01)
    {
        motorP->moveTo(36);
    }
    else
    {
        motorP->moveTo(-36);
    }
    _compteurShake ++;
    
};

void cncShield::verser(void)
{   

    switch(_compteurVerser)
    {
        case 0:
            motorZ->setSpeed(70);
            motorZ->moveTo(80);
            _compteurVerser ++;
            break;
        case 1:
            // motorP->setSpeed(1);
            // motorP->moveTo(-80);
            _compteurVerser ++;
            break;
        case 2:
            motorP->setSpeed(0);
            motorP->moveTo(90 * _sensVerser);
            _compteurVerser ++;
            break; 
        case 3:
            delay(250);
            motorP->setSpeed(0);
            motorP->moveTo(100 * _sensVerser);
            _compteurVerser ++;
            break;
        case 4:
            delay(100);
            motorP->setSpeed(0);
            motorP->moveTo(115 * _sensVerser);
            motorZ->setSpeed(70);
            // motorZ->setMaxSpeed(60);
            motorZ->moveTo(200);
            _compteurVerser ++;
            break;
        case 5:
            _compteurVerser ++;
            break;
        case 6:
            motorP->setSpeed(2);
            motorP->moveTo(0);
            _compteurVerser = 0;
            _verserDone = 1;
            break;
    }
};

void cncShield::moveServo(int angle)
{
    servoShaker->write(angle);
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

float cncShield::convertionForMM(float mm)
{
    return mm*180;
};

void cncShield::setNewMouvement(void)
{
    _newMouvement = 1;
};

void cncShield::controlPompe(int pompe,float volume)
{
    if(pompe <0)
        pompe =0;
    if(pompe>=6)
        pompe = 6;
    int pompeNum = pompe - 1;
    pompeTab[pompeNum]->vol_pompe_oz(volume);
};

