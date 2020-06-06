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

#include "output_handler.h"

#include "Arduino.h"

// // BLE Gesture Model Service
// BLEService gestureService("180F");
//
// // Detected gesture characteristic
// BLEByteCharacteristic detectedGestureChar("2A18",  // standard 16-bit characteristic UUID
//   BLERead | BLENotify); // remote clients will be able to get notifications if this characteristic changes
//
// BLEDevice central;
//
// bool SetupBLE(tflite::ErrorReporter* error_reporter) {
//   if (!BLE.begin()) {
//     error_reporter->Report("Starting BLE Failed!");
//     return false;
//   }
//
//   /* Set a local name for the BLE device
//      This name will appear in advertising packets
//      and can be used by remote devices to identify this BLE device
//      The name can be changed but maybe be truncated based on space left in advertisement packet
//   */
//   BLE.setLocalName("GestureDetector");
//   BLE.setAdvertisedService(gestureService); // add the service UUID
//   gestureService.addCharacteristic(detectedGestureChar); // add the detected gesture characteristic
//   BLE.addService(gestureService); // Add the gesture service
//   detectedGestureChar.writeValue((byte)0xAB); // set initial value for this characteristic ("none")
//
//   /* Start advertising BLE.  It will start continuously transmitting BLE
//      advertising packets and will be visible to remote BLE central devices
//      until it receives a new connection */
//
//   // start advertising
//   BLE.advertise();
//   error_reporter->Report("Bluetooth device active, waiting for connections...");
//
//   return true;
// }

void HandleOutput(tflite::ErrorReporter* error_reporter, int kind) {
  // The first time this method runs, set up our LED
  static bool is_initialized = false;
  if (!is_initialized) {
    pinMode(LED_BUILTIN, OUTPUT);
    is_initialized = true;
  }
  // Toggle the LED every time an inference is performed
  static int count = 0;
  ++count;
  if (count & 1) {
    digitalWrite(LED_BUILTIN, HIGH);
  } else {
    digitalWrite(LED_BUILTIN, LOW);
  }

  // Print to serial port
  if (kind == 0) {
    // error_reporter->Report("None");
  }
  else if (kind == 1) {
    error_reporter->Report("Up");
  }
  else if (kind == 2) {
    error_reporter->Report("Down");
  }
  else if (kind == 3) {
    error_reporter->Report("Right");
  }

  // // wait for a BLE central
  // central = BLE.central();
  // // Advertise to bluetooth
  // if (central) {
  //   error_reporter->Report("Connected to central");
  //   detectedGestureChar.writeValue((byte)0xAB);
  //   // detectedGestureChar.writeValue(kind);
  // }

}

#endif  // ARDUINO_EXCLUDE_CODE
