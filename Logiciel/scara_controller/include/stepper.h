#include <Arduino.h>
#ifndef STEPPER_H
#define STEPPER_H

class Stepper
{
    public:
        Stepper();
        Stepper(int dirPin, int stepPin, int microstep, float gearRatio);
        bool update(bool accel);
        bool moveTo(float degree);
        bool isMoving(void);
        void setpin(int dirPin, int stepPin);
        void setGearRatio(float gearRatio);
        float getCurrentPosition(void);
        void setCurrentPosition(float position);
        void setMicroStep(int microStep);
        void setDirection(int direction);
        void setMaxSpeed(int speed);
        void setSpeed(int speed);
    private:
        
        void updateAccel(void);
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
        long _lastTime = 0;
        int _flipflopStep = 0;
        
};

#endif
