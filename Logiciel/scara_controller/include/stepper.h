#include <Arduino.h>
#ifndef STEPPER_H
#define STEPPER_H

class Stepper
{
    public:
        Stepper();
        Stepper(int dirPin, int stepPin, int microstep, float gearRatio);
        void update(void);
        bool moveTo(float degree);
        bool isMoving(void);
        void setpin(int dirPin, int stepPin);
        void setGearRatio(float gearRatio);
        float getCurrentPosition(void);
        void setSpeed(int speed);
        void setMicroStep(int microStep);
        void setDirection(int direction);
        void updateAccel(void);
    private:
        int _dirPin;
        int _direction;
        int _stepPin;
        int _stepCount;
        float _gearRatio;
        int _microstep;
        float _currentPosition;
        int _speed;
        int _maxSpeed;
        int _delaySpeed;
        long _timeAcc;
        long _stepAccel;
        int _calculStepAccel;
        int _accelStep = 0;
        
};

#endif
