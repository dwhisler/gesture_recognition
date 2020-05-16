#include "IMUHandler.h"

// Initializes IMU connection, sets sample rate
bool IMUHandler::init() {
  if (!IMU.begin()) {
    return false;
  }
  sample_rate = IMU.accelerationSampleRate(); // Assuming gyro and acc set to same sample rate
  return true;
}

bool IMUHandler::read() {
  if ( !(IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) ) {
    return false;
  }
  IMU.readAcceleration(accX, accY, accZ);
  IMU.readGyroscope(gyrX, gyrY, gyrZ);
  return true;
}
