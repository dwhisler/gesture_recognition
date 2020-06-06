/**
 * Based on SensorFuser class from Stanford class EE267 (Virtual Reality) by Gordon Wetzstein
 * https://stanford.edu/class/ee267/
 */

#include "SensorFuser.h"

SensorFuser::SensorFuser() :

  imu(IMUHandler()),
  gyr{0,0,0},
  acc{0,0,0},
  sample_rate(0),
  gyr_bias{0,0,0},
  acc_bias{0,0,0},
  prevT(0.0),
  alpha(0.9),
  ema(0.05),
  deltaT(0.0),
  orientation(Quaternion())

{}

bool SensorFuser::initImu() {

  bool success = imu.init();
  sample_rate = imu.sample_rate;
  return success;

}


void SensorFuser::measureImuBias() {

  for (int i = 0; i < 3; i++){
    gyr_bias[i] = 0;
    acc_bias[i] = 0;
  }
  float n = 1000;

  for (int i = 0; i < (int) n; i++){
    if (imu.read()){
      gyr_bias[0] += imu.gyrX/n;
      gyr_bias[1] += imu.gyrY/n;
      gyr_bias[2] += imu.gyrZ/n;
      acc_bias[0] += imu.accX/n;
      acc_bias[1] += imu.accY/n;
      acc_bias[2] += imu.accZ/n;
    }
    else{
      i--;
    }
  }

}

void SensorFuser::setImuBias(float gyr_bias_in[3], float acc_bias_in[3]) {

  for (int i = 0; i < 3; i++) {
    gyr_bias[i] = gyr_bias_in[i];
    acc_bias[i] = acc_bias_in[i];
  }

}

void SensorFuser::resetOrientation() {

  orientation = Quaternion();

}


bool SensorFuser::updateOrientation() {

  //sample imu values
  if (!imu.read()) {
  // return false if there's no data
    return false;
  }

  // update acceleration bias with exponential moving average
  acc_bias[0] = ema*imu.accX + (1-ema)*acc_bias[0];
  acc_bias[1] = ema*imu.accY + (1-ema)*acc_bias[1];
  acc_bias[2] = ema*imu.accZ + (1-ema)*acc_bias[2];

  //call micros() to get current time in microseconds
  //update:
  //previousTimeImu (in seconds)
  //deltaT (in seconds)
  float currT = ((float) micros()) / 1000000;
  deltaT = currT - prevT;
  prevT = currT;

  gyr[0] = imu.gyrX - gyr_bias[0];
  gyr[1] = imu.gyrY - gyr_bias[1];
  gyr[2] = imu.gyrZ - gyr_bias[2];

  acc[0] = imu.accX - acc_bias[0];
  acc[1] = imu.accY - acc_bias[1];
  acc[2] = imu.accZ - acc_bias[2];

  // update to new orientation with complementary filter

  float eps = 0.00000001; // for numerical stability in division
  float norm = sqrt(gyr[0]*gyr[0]+gyr[1]*gyr[1]+gyr[2]*gyr[2]);
  if (norm < eps){
    return false;
  }

  Quaternion qdelta = Quaternion();
  qdelta.setFromAngleAxis(deltaT*norm, gyr[0]/norm, gyr[1]/norm, gyr[2]/norm);

  Quaternion qnewgyr = orientation.multiply(qdelta);

  Quaternion qacc = Quaternion(0, acc[0], acc[1], acc[2]);
  Quaternion qaworld = qacc.rotate(qnewgyr);
  qaworld.normalize();

  float phi = acos(qaworld.q[2])*PI/180;
  float n[3];
  n[0] = -1*qaworld.q[3];
  n[1] = 0;
  n[2] = qaworld.q[1];
  float normN = sqrt(n[0]*n[0]+n[1]*n[1]+n[2]*n[2]);

  Quaternion qtiltCorr = Quaternion();
  qtiltCorr.setFromAngleAxis((1-alpha)*phi, n[0]/normN, n[1]/normN, n[2]/normN);

  orientation = qtiltCorr.multiply(qnewgyr);

  return true;

}
