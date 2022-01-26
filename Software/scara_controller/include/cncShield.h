#include <Arduino.h>
#include <stepper.h>
#ifndef CNCSHIELD_H 
#define CNCSHIELD_H

#define stepPinX 2
#define stepPinY 3
#define stepPinZ 4
#define dirPinX 5
#define dirPinY 6
#define dirPinZ 7
#define enPin 8
#define endStopX 9
#define endStopY 10
#define endStopZ 11

class cncShield
{
    public:
        cncShield();
        void enableMotor(void);
        void disableMotor(void);
        bool areMotorEnabled(void);

        Stepper* motorX;
        Stepper* motorY;
        Stepper* motorZ;

    private:
        bool _enMotor;
};

#endif
