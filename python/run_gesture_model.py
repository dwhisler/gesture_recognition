import serial
import tensorflow as tf
import numpy as np

gesture_map = {'none':0, 'up':1, 'down':2, 'right':3}
gesture_map_reverse = {0:'none', 1:'up', 2:'down', 3:'right'}

def run_model():
    model = tf.keras.models.load_model('../saved_models/tilt_gestures_model_aug_fused')
    seq_length = 256
    data_axes = 4

    print('Looking for Arduino...')
    with serial.Serial('/dev/ttyACM0', 115200) as ser:
        print("Arduino found!")
        circ_buff = np.zeros((1, seq_length, data_axes, 1))
        t = 0 # circular buffer index

        new_data_available = False
        measuring_bias = True
        while (ser.readline().strip().decode('utf-8') == "Measuring bias..."):
            if (measuring_bias):
                measuring_bias = False
                print('Measuring bias...')

        # Main running loop
        while(1):
            data = ser.readline()
            data_str = data.strip().decode('utf-8').split()
            #print(data_str[0])
            circ_buff[0,t,:,0] = np.array([float(data_str[i]) for i in range(6, 10)])

            if (t == seq_length-1):
                y_pred = model.predict(circ_buff)
                pred_gesture = gesture_map_reverse[np.argmax(y_pred[0,:])]
                print(pred_gesture)
                if (pred_gesture != 'none'):
                    print('Predicted gesture: ' + pred_gesture)

            t += 1
            if (t >= seq_length):
                t = 0

def run_tflite_model():
    # Load TFLite model and allocate tensors.
    interpreter = tf.lite.Interpreter(model_path='../saved_models/quant_aug_fused.tflite')
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    seq_length = 256
    data_axes = 4

    print('Looking for Arduino...')
    with serial.Serial('/dev/ttyACM0', 115200) as ser:
        print("Arduino found!")
        circ_buff = np.zeros((1, seq_length, data_axes, 1))
        t = 0 # circular buffer index

        new_data_available = False
        measuring_bias = True
        while (ser.readline().strip().decode('utf-8') == "Measuring bias..."):
            if (measuring_bias):
                measuring_bias = False
                print('Measuring bias...')

        # Main running loop
        while(1):
            data = ser.readline()
            data_str = data.strip().decode('utf-8').split()
            #print(data_str[0])
            circ_buff[0,t,:,0] = np.array([float(data_str[i]) for i in range(6, 10)])

            if (t == seq_length-1):
                interpreter.set_tensor(input_details[0]['index'], circ_buff.astype('float32'))
                interpreter.invoke()

                y_pred = interpreter.get_tensor(output_details[0]['index'])
                pred_gesture = gesture_map_reverse[np.argmax(y_pred[0,:])]
                print(pred_gesture)
                if (pred_gesture != 'none'):
                    print('Predicted gesture: ' + pred_gesture)

            t += 1
            if (t >= seq_length):
                t = 0

if __name__ == '__main__':
    run_tflite_model()
