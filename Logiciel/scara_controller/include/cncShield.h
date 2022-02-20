#include <Arduino.h>
#include <stepper.h>

#ifndef CNCSHIELD_H 
#define CNCSHIELD_H

#define stepPinX_pin 2
#define stepPinY_pin 3
#define stepPinZ_pin 4
#define dirPinX_pin 5
#define dirPinY_pin 6
#define dirPinZ_pin 7
#define enPin_pin 8
#define endStopX_pin 9
#define endStopY_pin 10
#define endStopZ_pin 11

#define offset_A 10
#define offset_B 10
#define homingDirA 1
#define homingDirB 1

class cncShield
{
    public:
        cncShield();
        void enableMotor(void);
        void disableMotor(void);
        void update(void);
        bool homing(void);
        void startHoming(void);
        bool areMotorEnabled(void);
        bool getLimitSwitchA(void);
        bool getLimitSwitchB(void);
        bool getLimitSwitchZ(void);

        Stepper* motorA;
        Stepper* motorB;
        Stepper* motorZ;

    private:
        bool _enMotor;
        bool _homing = 0;
        bool _setupHoming = 0;
        int _homingSequence = 0;
};

#endif
