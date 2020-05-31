import serial
import tensorflow as tf
import numpy as np

gesture_map = {'none':0, 'click':1, 'doubleclick':2, 'rightcircle':3, 'leftcircle':4}
gesture_map_reverse = {0:'none', 1:'click', 2:'doubleclick', 3:'rightcircle', 4:'leftcircle'}

def run_model():
    model = tf.keras.models.load_model('../saved_models/david_click_gestures_model_fused2')
    seq_length = 255
    data_axes = 4

    print('Looking for Arduino...')
    with serial.Serial('/dev/ttyACM0', 115200) as ser:
        print("Arduino found!")
        circ_buff = np.zeros((1, seq_length, data_axes, 1))
        t = 0 # circular buffer index
        run_freq = 50 # how often to run model

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
            circ_buff[0,t,:,0] = np.array([float(data_str[i]) for i in range(6,10)])

            if (t == seq_length-1):
                y_pred = model.predict(circ_buff)
                pred_gesture = gesture_map_reverse[np.argmax(y_pred[0,:])]
                print(pred_gesture)
                if (pred_gesture != 'none'):
                    print('Predicted gesture: ' + pred_gesture)

            t += 1
            if (t >= seq_length):
                t = 0

if __name__ == '__main__':
    run_model()
