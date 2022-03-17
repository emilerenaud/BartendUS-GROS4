#include <Arduino.h>
#include <stepper.h>
#include <Servo.h>

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
#define SpnEn 12
#define Electro_pin 49

#define stepPinP_pin 34
#define dirPinP_pin 36

#define offset_A 176.5
#define offset_B -141
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
        float convertionForMM(float mm);
        void moveServo(int angle);
        void closeElectro(void);
        void openElectro(void);
        Servo *servoShaker;
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
