#include <Servo.h>
#define SRV_CTRL 2
#define PWR_LASR 3
#define INP_CTRL 4
#define INP_TRGT 5
#define STANDBY 1
#define TRIPPED 0

Servo laserServo;

void acquireTargetLock(int range, int offset) {
  while (true) {
    for (int i = (90 - range) - offset; i < 90 + range + 1 - offset; i++) {
      laserServo.write(i);
      delay(100);
      if (digitalRead(INP_CTRL) == TRIPPED ) {
        return;
      }
    }
  }
}

void setup() {
  // Set up tech
  laserServo.attach(SRV_CTRL);
  Serial.begin(9600);
  
  acquireTargetLock(20, 10);
}
void loop() {
}