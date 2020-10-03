## Gesture Recognition using Sensor Fusion & Deep Learning on an Arduino Embedded Platform

## Paper

See the written report at [EE292D_Final_Report.pdf](EE292D_Final_Report.pdf)

## Getting Started

It is best to set up a virtual environment to install the Python requirements, which can be installed with the command:
`pip install -r requirements.txt`

### Prerequisites

* Python 3.7.5
* Python dependencies listed in [requirements.txt](requirements.txt)
* Arduino 1.8.12
* Arduino_TensorFlowLite 2.1.0-ALPHA
* Arduino_LSM9DS1 1.1.0
* xxd

### Data Collection
Data is collected using the script [collect_data.py](collect_data.py) with the project [data_collection.ino](data_collection.ino) running on the Arduino.

## Training

A model can be trained using the script [train_gesture_model.py](train_gesture_model.py).

## Quantization and Deploying to Arduino

A trained model can be deployed to the Arduino by first running the script [deploy_model.py](deploy_model.py).
Then, the command:
`xxd -i <quantized_model>.tflite > <gesture_model_data>.cc`
must be run to generate a TFLite Flatbuffer. Finally, the contents of this file must be copied to the file [gesture_model_data.cpp](gesture_model_data.cpp) in the gesture_model project.

## Running

When the model is deployed, the project [gesture_model.ino](gesture_model.ino) must be running on the Arduino.
Then, with the Arduino connected over serial, the script [gesture_interpreter.py](gesture_interpreter.py) can be run to demonstrate the YouTube video control application.

## Authors

* **David Whisler**

## Acknowledgments

* Pete Warden (thank you for your help!)
* TensorflowLite Magic Wand example, on which this project is based
* Gordon Wetzstein's EE267 (Virtual Reality) class at Stanford, on which the sensor fusion algorithm is based
