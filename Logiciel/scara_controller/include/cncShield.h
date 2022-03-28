#ifndef CNCSHIELD_H 
#define CNCSHIELD_H

#include <Arduino.h>
#include <stepper.h>
#include <Servo.h>
#include <pompe.h>

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

#define pompe_pin_1 50
#define pompe_pin_2 51
#define pompe_pin_3 48
#define pompe_pin_4 46
#define pompe_pin_5 44
#define pompe_pin_6 42

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
        void setNewMouvement(void);
        float convertionForMM(float mm);
        void moveServo(int angle);
        void closeElectro(void);
        void openElectro(void);
        void shake(void);
        void startShake(void);
        void verser(void);
        void startVerser(int sens);
        Servo *servoShaker;
        Stepper* motorA;
        Stepper* motorB;
        Stepper* motorZ;
        Stepper* motorP;
        Pompe* pompeTab[6];
        Pompe* pompe1;
        void controlPompe(int pompe,float volume);

    private:
        bool _enMotor;
        bool _homing = 0;
        bool _newMouvement = 0;
        bool _setupHoming = 0;
        int _homingSequence = 0;
        bool _shake = 0;
        bool _initShake = 0;
        bool _shakeDone = 0;
        int _compteurShake = 0;
        bool _verser = 0;
        int _sensVerser = 0;
        bool _verserDone = 0;
        int _compteurVerser = 0;
        int pompe_pin[6] = {pompe_pin_1,pompe_pin_2,pompe_pin_3,pompe_pin_4,pompe_pin_5,pompe_pin_6};
};

#endif
