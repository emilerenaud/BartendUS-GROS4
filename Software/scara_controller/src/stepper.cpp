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

    _currentPosition = 0;
    _stepCount = 0;
};

void Stepper::update()
{
    if(_stepCount != 0)
    {
        digitalWrite(_stepPin,HIGH);
        delayMicroseconds(_delaySpeed);
        digitalWrite(_stepPin,LOW);
        delayMicroseconds(_delaySpeed);
        // _currentPosition = _stepCount;
        _stepCount --;
    }
};

bool Stepper::moveTo(float degree)
{
    if(_stepCount != 0)
        return EXIT_FAILURE;
    if(_direction == 1 || _direction == -1)
        degree = degree * _direction;
    if(degree > 0)
        digitalWrite(_dirPin,LOW);
    else
        digitalWrite(_dirPin,HIGH);
    // Serial.println(degree);
    if(degree == _currentPosition)
        return EXIT_FAILURE;

    _currentPosition = degree;
    _stepCount = int((abs(degree) * _gearRatio * _microstep * 200.0) /360); 
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
    _delaySpeed = map(_speed,0,100,800,100);
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



