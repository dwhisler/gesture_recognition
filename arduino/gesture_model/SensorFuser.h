/**

 * Based on OrientationTracker class from Stanford class EE267 (Virtual Reality) by Gordon Wetzstein

 * @class OrientationTracker
 * This class performs orientation tracking using values from the IMU.
 * Overview:
 * - samples data from the imu.
 * - performs complementary filtering to estimate orientation
 * in either  euler angles or quaternion
 * - calls functions from Quaternion for quaternion math
 * - calls functions from OrientationMath for complementary filtering
 *
 * The complementary filter alpha value is between [0,1].
 * If 1, ignore angle correction from acc. If 0, use full correction
 * from accc.
 *
 * See get..() functions to get read-only access to the following values:
 * - euler angle estimate
 * - quaternion estimate
 * - gyro and acc values (after preprocessing)
 * - gyro bias and variance
 *
 */

#ifndef SensorFuser_H_
#define SensorFuser_H_

#include "IMUHandler.h"
#include "Quaternion.h"

class SensorFuser {

  public:

    /**
     * constructor
     */
    SensorFuser();


    /**
     * samples and processes imu data.
     * updates the quaternion, and euler
     * @returns true if sampling processing was successful,
     * false, if no data was available.
     */
    bool initImu();

    /**
     * measures Imu bias and variance.
     * updates the gyrBias and gyrVariance fields.
     * updates the accBias and accVariance fields.
     * the order of elements is [x-axis, y-axis, z-axis],
     * i.e. gyrBias[0] is the gyro bias of the x-axis
     *
     * steps to sample from imu:
     * - call imu.read() to sample IMU
     * - if it returns true, get values from
     *   imu.gyrX, imu.gyrY, imu.gyrZ,
     *   imu.accX, imu.accY, imu.accZ,
     */
    void measureImuBias();


    /**
     * sets the Imu bias
     * @param [in] bias - copy the bias values in this array into
     *  this class' gyrBias variable
     */
    void setImuBias(float gyr_bias_in[3], float acc_bias_in[3]);

    /**
     * resets orientation estimates to 0
     */
    void resetOrientation();

    /**
     * @returns read-only reference to accelerometer values,
     * order is ax,ay,az
     */
    float* getAcc() { return acc; };


    /**
     * @returns read-only reference to gyroscope values,
     * order is wx, wy, wz
     */
    float* getGyr() { return gyr; };


    /**
     * @returns sample rate in Hz
     */
    int getSampleRate() { return sample_rate; };

    /**
     * @returns read-only reference to gyroscope bias values
     * order is wx, wy, wz
     */
    const float* getGyrBias() const { return gyr_bias; };

    /**
     * @returns read-only reference to accelerometer bias values
     * order is ax, ay, az
     */
    const float* getAccBias() const { return acc_bias; };

    /**
     * @returns orientation (as quaternion)
     * order is w, x, y, z
     */
    Quaternion getOrientation() const { return orientation; };


    /**
     * calls the orientation tracking functions and
     * updates the orientation
     */
    bool updateOrientation();


  protected:


    /** Imu class for sampling from IMU */
    IMUHandler imu;


    /**
     * gyro values in order (x,y,z) after bias subtraction
     * in IMU ref frame (z-axis points out of imu).
     * units are deg/s
     */
    float gyr[3];


    /**
     * acc values in order (x,y,z)
     * units are m/s^2
     * in IMU ref frame (z-axis points out of imu).
     */
    float acc[3];


    /**
     * sample rate in Hz
     */
    int sample_rate;


    /**
     * gyro bias values. order is: (wx,wy,wz)
     */
    float gyr_bias[3];


    /**
     * accelerometer bias values. order is: (ax,ay,az)
     */
    float acc_bias[3];


    /**
     * the previous time in s the imu was polled
     */
    float prevT;


    /**
     * complementary filter alpha value [0,1]
     * - 1: use full value of acc tilt correction
     * - 0: ignore acc tilt correction
     */
    float alpha;


    /**
     * time since the previous imu read, in s
     */
    float deltaT;;

    /**
     * estimate of orientation (as a quaternion)
     * from comp. filter of acc and gyr
     */
    Quaternion orientation;

};

#endif
