#include <Arduino.h>
#include <cncShield.h>

cncShield shield;

void setup() {
  // put your setup code here, to run once:
  shield.motorX->moveTo(10);
}

void loop() {
  // put your main code here, to run repeatedly:
}