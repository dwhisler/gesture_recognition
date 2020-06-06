/**
 * Based on Quaternion class from Stanford class EE267 (Virtual Reality) by Gordon Wetzstein
 * https://stanford.edu/class/ee267/
 */

#ifndef QUATERNION_H_
#define QUATERNION_H_

#include "Arduino.h"

class Quaternion {
public:
  /**
   * Definition:
   * q = q[0] + q[1] * i + q[2] * j + q[3] * k
   */
  float q[4];

  /* Default constructor */
  Quaternion() :
    q{1.0, 0.0, 0.0, 0.0} {}

  Quaternion(float q0, float q1, float q2, float q3) :
    q{q0, q1, q2, q3} {}

  Quaternion(const Quaternion &other) {
    for (int i = 0; i < 4; i++){
      q[i] = other.q[i];
    }
  }

  /* function to construct a quaternion from angle-axis representation. angle is given in degrees. */
  void setFromAngleAxis(float angle, float vx, float vy, float vz) {
    float th = angle*PI/180;

    q[0] = cos(th/2);
    q[1] = vx*sin(th/2);
    q[2] = vy*sin(th/2);
    q[3] = vz*sin(th/2);
  }

  /* function to convert quaternion to Euler angles (as array roll, pitch, yaw (x, y, z))*/
  float* toEuler() {
    float euler[3];

    // roll (x-axis rotation)
    float sinr_cosp = 2*(q[0]*q[1] + q[2]*q[3]);
    float cosr_cosp = 1 - 2*(q[1]*q[1] + q[2]*q[2]);
    euler[0] = atan2(sinr_cosp, cosr_cosp);

    // pitch (y-axis rotation)
    float sinp = 2*(q[0]*q[2] - q[3]*q[1]);
    if (abs(sinp) >= 1)
        euler[1] = (sinp >= 0) ? PI/2 : -1*PI/2; // use 90 degrees if out of range
    else
        euler[1] = asin(sinp);

    // yaw (z-axis rotation)
    float siny_cosp = 2*(q[0]*q[3] + q[1]*q[2]);
    float cosy_cosp = 1 - 2*(q[2]*q[2] + q[3]*q[3]);
    euler[2] = atan2(siny_cosp, cosy_cosp);

    return euler;
  }

  /* function to compute the length of a quaternion */
  float length() {
    return sqrt(q[0]*q[0]+q[1]*q[1]+q[2]*q[2]+q[3]*q[3]);
  }

  /* function to normalize a quaternion */
  void normalize() {
    float len = length();

    for (int i = 0; i < 4; i++){
      q[i] /= len;
    }
  }

  /* function to invert a quaternion */
  Quaternion inverse() {
    Quaternion inv = Quaternion();

    float lensq = q[0]*q[0]+q[1]*q[1]+q[2]*q[2]+q[3]*q[3];

    inv.q[0] = q[0]/lensq;
    inv.q[1] = -1*q[1]/lensq;
    inv.q[2] = -1*q[2]/lensq;
    inv.q[3] = -1*q[3]/lensq;

    return inv;
  }

  /* function to multiply this quaternion with another */
  Quaternion multiply(Quaternion other) {
    Quaternion prod = Quaternion();

    prod.q[0] = q[0]*other.q[0] - q[1]*other.q[1] - q[2]*other.q[2] - q[3]*other.q[3];
    prod.q[1] = q[0]*other.q[1] + q[1]*other.q[0] + q[2]*other.q[3] - q[3]*other.q[2];
    prod.q[2] = q[0]*other.q[2] - q[1]*other.q[3] + q[2]*other.q[0] + q[3]*other.q[1];
    prod.q[3] = q[0]*other.q[3] + q[1]*other.q[2] - q[2]*other.q[1] + q[3]*other.q[0];

    return prod;
  }

  /* function to rotate a quaternion by r * q * r^{-1} */
  Quaternion rotate(Quaternion r) {
    Quaternion rinv = r.inverse();

    return r.multiply(*this).multiply(rinv);
  }

  /* helper function to print out a quaternion */
  void serialPrint() {
    Serial.print("QC ");
    Serial.print(q[0]);
    Serial.print(" ");
    Serial.print(q[1]);
    Serial.print(" ");
    Serial.print(q[2]);
    Serial.print(" ");
    Serial.print(q[3]);
    Serial.println();
  }
};

#endif // ifndef QUATERNION_H
