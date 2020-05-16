#ifndef IMUHandler_H_
#define IMUHandler_H_

#include <Arduino.h>
#include <Arduino_LSM9DS1.h>

class IMUHandler {
public:
  float gyrX, gyrY, gyrZ;
  float accX, accY, accZ;
  int sample_rate;

  bool init();

  bool read();
};

#endif
