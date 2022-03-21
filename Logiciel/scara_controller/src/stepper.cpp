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
    _stepAccel = 0;
    _timeAcc = 2;
    _setupAcc = 1;
};

bool Stepper::update(bool accel)
{
    if(_stepCount != 0)
    {
        if(accel)
            updateAccelV2();
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

void Stepper::updateAccelV2()
{
    if(millis() - _lastTimeAcc >= _timeAcc)
    {
        _lastTimeAcc = millis();
        if(_setupAcc)
        {
            _setupAcc = 0;
            this->setSpeed(int(_maxSpeed*0.25));
        }
        if(_stepCount >= _calculStepAccel*2)
        {
            if(_speed < _maxSpeed)
            {
                this->setSpeed(_speed + 0.2);
            }
            // premiere moitier du parcour

        }
        else if(_stepCount < _calculStepAccel*2)
        {
            // deuxieme moititier du parcour
            // if(_speed > abs(_maxSpeed/2))
            // {
            //     this->setSpeed(_speed - 5);
            // }
            if(_speed > (_maxSpeed*0.25))
            {
                this->setSpeed((_speed - 0.5));
            }

            if(_stepCount == 1)
            {
                _setupAcc = 1;
            }
        }
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
    _lastTimeAcc = millis();
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

void Stepper::setSpeed(float speed)
{
    if(speed > 100.0)
        speed = 100.0;
    if(speed < 0.0)
        speed = 0.0;
    _speed = speed;
    int tempSpeed = _speed * 10;
    _delaySpeed = map(tempSpeed,0,1000,800,80);
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



