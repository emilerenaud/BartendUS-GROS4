#include <cncShield.h>

cncShield::cncShield()
{
    motorX = new Stepper(dirPinX,stepPinX,16,1);
    motorY = new Stepper(dirPinY,stepPinY,16,1);
    motorZ = new Stepper(dirPinZ,stepPinZ,16,1);

    pinMode(enPin,OUTPUT);

};

void cncShield::enableMotor()
{
    digitalWrite(enPin,LOW);
    _enMotor = 1;
};

void cncShield::disableMotor()
{
    digitalWrite(enPin,HIGH);
    _enMotor = 0;
};

bool cncShield::areMotorEnabled()
{
    return _enMotor;
};