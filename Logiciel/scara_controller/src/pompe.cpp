#include "pompe.h"

Pompe::Pompe()
{

};

Pompe::~Pompe()
{

};

Pompe::Pompe(int dir_1, int dir_2, int vit_)
{
    // Definition entrees et sorties
    dir1 = dir_1;
    dir2 = dir_2;
    vit = vit_;
    pinMode(dir1, OUTPUT);
    pinMode(dir2, OUTPUT);
    pinMode(vit, OUTPUT);
    digitalWrite(dir1, 1);
    digitalWrite(dir2, 0);
};

Pompe::Pompe(int vit_)
{
    // Definition entrees et sorties
    vit = vit_;
    pinMode(vit, OUTPUT);
};

// Fonction qui actionne les pompes selon le volume desire
void Pompe::vol_pompe_oz(float volume)
{
    if (delais_pompe > 300000)
    {
        delais_pompe = 300000;
    }
    long t_pompe = (volume * 1000) / oz_par_sec + delais_pompe * oz_des / 1000;
    long t_deb = millis();

    time_pompe = t_pompe;

    // while (millis() - t_deb <= t_pompe)
    // {
    //     digitalWrite(vit,1);
    // }s
    // digitalWrite(vit, 0);
    delais_pompe = millis() - delais_pompe;
    start_time = millis();
};

void Pompe::update()
{
    if(millis() - start_time <= time_pompe)
    {
        digitalWrite(vit,1);
    }
    else
    {
        digitalWrite(vit,0);
    }
    
};