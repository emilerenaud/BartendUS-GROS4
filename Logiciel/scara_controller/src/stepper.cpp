#include <stepper.h>

Stepper::Stepper(){
};

Stepper::Stepper(int dirPin, int stepPin,int microstep, float gearRatio)
{
    _gearRatio = gearRatio;
    _microstep = microstep;
    this->setpin(dirPin,stepPin);
    this->setDirection(1);
    digitalWrite(_dirPin,LOW);
    digitalWrite(_stepPin,LOW);
    _maxSpeed = 100;
    _currentPosition = 0;
    _stepCount = 0;
    _timeAcc = millis();
    _stepAccel = 0;
};

bool Stepper::update(bool accel)
{
    if(_stepCount != 0)
    {
        if(accel)
            updateAccel();
        if(micros() - _lastTime >= _delaySpeed)
        {
            if(_flipflopStep&0x01)
            {
                digitalWrite(_stepPin,HIGH);
            }
            else
            {
                digitalWrite(_stepPin,LOW);
                _stepCount --;
            }
            _flipflopStep++;
            _lastTime = micros();
        }
        
        // _currentPosition = _stepCount;
        return 1;
    }
    else
    {
        return 0;
    }
};

void Stepper::updateAccel()
{
    int tempSpeed = 0;
    if(_stepCount <= (_calculStepAccel *6) && _stepCount > (_calculStepAccel *4))
    {
        tempSpeed = map(_stepCount,(_calculStepAccel*6),(_calculStepAccel*4),(_maxSpeed*0.25),_maxSpeed);
        this->setSpeed(int(tempSpeed));
    }
    else if(_stepCount <= (_calculStepAccel *4) && _stepCount > (_calculStepAccel *2))
    {
        this->setSpeed(int(_speed));
    }
    else if(_stepCount <= (_calculStepAccel *2) && _stepCount > (_calculStepAccel *0))
    {
        tempSpeed = map(_stepCount,(_calculStepAccel*0),(_calculStepAccel*2),(_maxSpeed*0.25),_maxSpeed);
        this->setSpeed(int(tempSpeed));
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
    _lastTime = micros();
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

void Stepper::setCurrentPosition(float position)
{
    _currentPosition = position;
    _stepCount = 0;

}

void Stepper::setMaxSpeed(int speed)
{
    _maxSpeed = speed;
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



