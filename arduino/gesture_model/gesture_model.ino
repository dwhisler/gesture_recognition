#include "SensorFuser.h"

#include <TensorFlowLite.h>
#include "gesture_predictor.h"
#include "magic_wand_model_data.h"
#include "output_handler.h"
#include "tensorflow/lite/experimental/micro/kernels/micro_ops.h"
#include "tensorflow/lite/experimental/micro/micro_error_reporter.h"
#include "tensorflow/lite/experimental/micro/micro_interpreter.h"
#include "tensorflow/lite/experimental/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "tensorflow/lite/version.h"

// Globals, used for compatibility with Arduino-style sketches.
namespace {
  SensorFuser sf;
  float* acc;
  float* gyr;
  Quaternion q;
  
  tflite::ErrorReporter* error_reporter = nullptr;
  const tflite::Model* model = nullptr;
  tflite::MicroInterpreter* interpreter = nullptr;
  TfLiteTensor* model_input = nullptr;
  int input_length;

  // Create an area of memory to use for input, output, and intermediate arrays.
  // The size of this will depend on the model you're using, and may need to be
  // determined by experimentation.
  constexpr int kTensorArenaSize = 60 * 1024;
  uint8_t tensor_arena[kTensorArenaSize];

  // Whether we should clear the buffer next time we fetch data
  bool should_clear_buffer = false;
}  // namespace

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
    // sf.getOrientation().serialPrint();

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
