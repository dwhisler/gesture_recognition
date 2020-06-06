/*
  Modified by David Whisler
*/

/* Copyright 2019 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#if defined(ARDUINO) && !defined(ARDUINO_ARDUINO_NANO33BLE)
#define ARDUINO_EXCLUDE_CODE
#endif  // defined(ARDUINO) && !defined(ARDUINO_ARDUINO_NANO33BLE)

#ifndef ARDUINO_EXCLUDE_CODE

#include "input_handler.h"

// A ring buffer holding the most recent data
float save_data[kBuffSize] = {0.0};
// Most recent position in the save_data buffer
int begin_index = 0;
// The SensorFuser object where IMU data is read from
SensorFuser sf;

TfLiteStatus SetupIMU(tflite::ErrorReporter* error_reporter) {
  // Wait until we know the serial port is ready
  while (!Serial) {
  }

  // Switch on the IMU
  if (!sf.initImu()) {
    error_reporter->Report("Failed to initialize IMU");
    return kTfLiteError;
  }

  // Compute initial value for accelerometer and gyro bias
  error_reporter->Report("Measuring bias...");
  sf.measureImuBias();

  error_reporter->Report("Magic starts!");

  return kTfLiteOk;
}

bool ReadIMU(tflite::ErrorReporter* error_reporter, float* input,
                       int length) {
  // Keep track of whether we stored any new data
  bool new_data = false;
  // Loop through new samples and add to buffer
  if (sf.updateOrientation()) {
   float* acc;
   float* gyr;
   Quaternion q;

   acc = sf.getAcc(); // accelerometer values
   gyr = sf.getGyr(); // gyroscope values
   q = sf.getOrientation(); // sensor fused quaternion orientation

   // Write samples to our buffer
   save_data[begin_index++] = acc[0];
   // save_data[begin_index++] = gyr[0];
   save_data[begin_index++] = acc[1];
   // save_data[begin_index++] = gyr[1];
   save_data[begin_index++] = acc[2];
   // save_data[begin_index++] = gyr[2];
   // save_data[begin_index++] = q.q[0];
   // save_data[begin_index++] = q.q[1];
   // save_data[begin_index++] = q.q[2];
   // save_data[begin_index++] = q.q[3];

   // If we reached the end of the circle buffer, reset
   if (begin_index >= kBuffSize) {
     begin_index = 0;
   }
   new_data = true;
  }

  // Skip this round if data is not ready yet
  if (!new_data) {
   return false;
  }

  // Copy the requested number of bytes to the provided input tensor
  for (int i = 0; i < length; ++i) {
   int ring_array_index = begin_index + i - length;
   if (ring_array_index < 0) {
     ring_array_index += kBuffSize;
   }
   input[i] = save_data[ring_array_index];
  }

  return true;
}

#endif  // ARDUINO_EXCLUDE_CODE
