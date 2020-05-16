#include "SensorFuser.h"

SensorFuser sf;

void setup() {
  Serial.begin(115200);
  while (!Serial);
  Serial.println("Started");

  while (!sf.initImu()) {
    Serial.println("Failed to initialize IMU!");
  }

  Serial.println("Measuring bias...");
  sf.measureImuBias();

}

void loop() {

  if (sf.updateOrientation()) {
    sf.getOrientation().serialPrint();
  }

}
