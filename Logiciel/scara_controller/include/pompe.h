#ifndef POMPE_H
#define POMPE_H

#include <Arduino.h>

class Pompe
{
    public:
        Pompe();
        ~Pompe();
        Pompe(int dir_1, int dir_2, int vit_);
        Pompe(int vit_);
        void vol_pompe_oz(float volume);
        void update(void);

    private:
        int dir1;
        int dir2;
        int vit;
        long delais_pompe = 0;
        unsigned long time_pompe = 0;
        unsigned long  start_time = 0;
        const float oz_par_sec = 0.965; // Dropper un peu. 6465
        const float oz_des = 0.0067;
        bool message_done = false;
};

#endif
