#include "SensorFuser.h"

SensorFuser sf;
float* acc;
float* gyr;
Quaternion q;

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

    acc = sf.getAcc();
    gyr = sf.getGyr();

    for (int i = 0; i < 3; i++) {
      Serial.print(acc[i]);
      Serial.print(" ");
      Serial.print(gyr[i]);
      Serial.print(" ");
    }

    q = sf.getOrientation();
    for (int i = 0; i < 4; i++) {
      Serial.print(q.q[i]);
      Serial.print(" ");
    }

    Serial.print(sf.getSampleRate());

    Serial.println();
  }

}
