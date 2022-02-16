#include <stepper.h>

Stepper::Stepper(){
};

Stepper::Stepper(int dirPin, int stepPin,int microstep, float gearRatio)
{
    _gearRatio = gearRatio;
    _microstep = microstep;
    this->setpin(dirPin,stepPin);
    this->setSpeed(100);
    this->setDirection(1);
    digitalWrite(_dirPin,LOW);
    digitalWrite(_stepPin,LOW);
    _maxSpeed = 100;
    _currentPosition = 0;
    _stepCount = 0;
    _timeAcc = millis();
    _stepAccel = 0;
};

void Stepper::update()
{
    if(_stepCount != 0)
    {
        updateAccel();
        digitalWrite(_stepPin,HIGH);
        delayMicroseconds(_delaySpeed);
        digitalWrite(_stepPin,LOW);
        delayMicroseconds(_delaySpeed);
        // _currentPosition = _stepCount;
        _stepCount --;
    }
};

void Stepper::updateAccel()
{


    if(_stepCount <= (_calculStepAccel *6) && _stepCount > (_calculStepAccel *5))
    {
        this->setSpeed(int(_maxSpeed * 0.50));
    }
    else if(_stepCount <= (_calculStepAccel *5) && _stepCount > (_calculStepAccel *4))
    {
        this->setSpeed(int(_maxSpeed * 0.75));
    }
    else if(_stepCount <= (_calculStepAccel *4) && _stepCount > (_calculStepAccel *2))
    {
        this->setSpeed(int(_maxSpeed));
    }
    else if(_stepCount <= (_calculStepAccel *2) && _stepCount > (_calculStepAccel *1))
    {
        this->setSpeed(int(_maxSpeed) * 0.75);
    }
    else if(_stepCount <= (_calculStepAccel *1) && _stepCount > (_calculStepAccel *0))
    {
        this->setSpeed(int(_maxSpeed) * 0.50);
    }
}

bool Stepper::moveTo(float degree)
{
    if(_stepCount != 0)
        return EXIT_FAILURE;
    if(_direction == 1 || _direction == -1)
        degree = degree * _direction;
    float deltaPos = _currentPosition - degree;
    if(degree > _currentPosition)
        digitalWrite(_dirPin,LOW);
    else
        digitalWrite(_dirPin,HIGH);
    
        
    // Serial.println(degree);
    if(degree == _currentPosition)
        return EXIT_FAILURE;
    
    _currentPosition = degree;
    _stepCount = int((abs(deltaPos) * _gearRatio * _microstep * 200.0) /360); 
     _calculStepAccel = _stepCount / 6;
    // Serial.println("step count : " + String(_stepCount));
    
    return EXIT_SUCCESS;
};

bool Stepper::isMoving()
{
    if(_stepCount != 0)
        return 1;
    else
        return 0;
};

void Stepper::setpin(int dirPin, int stepPin)
{
    _dirPin = dirPin;
    _stepPin = stepPin;

    pinMode(_dirPin,OUTPUT);
    pinMode(_stepPin,OUTPUT);
};

void Stepper::setGearRatio(float gearRatio)
{
    _gearRatio = gearRatio;
};

float Stepper::getCurrentPosition()
{
    return _currentPosition;
};

void Stepper::setSpeed(int speed)
{
    _speed = speed;
    _delaySpeed = map(_speed,0,100,800,80);
    // Serial.println(_delaySpeed);
};

void Stepper::setMicroStep(int microstep)
{
    _microstep = microstep;
};

void Stepper::setDirection(int direction)
{
    if(direction == 1 || direction == -1)
        _direction = direction;
};



