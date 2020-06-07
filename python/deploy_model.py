import os
import numpy as np
import tensorflow as tf
from train_gesture_model import load_data
from sklearn.model_selection import train_test_split

path = '../data/session4/'
users = ['david']
gestures = ['none', 'up', 'down', 'right']
num_takes = 50
seq_length = 256

# Representative dataset generator for model quantization
def representative_dataset_gen():
    data_dict, sample_rate = load_data(path, users, gestures, num_takes, seq_length)
    (X, y) = data_dict['david']
    for i in range(X.shape[0]):
        data = X[i,:,0:5:2] # only accelerometer data
        data = data[np.newaxis,:,:,np.newaxis] # expand dims to 4-tensor
        data = data.astype(np.float32)
        yield [data]

# Converts Keras model to quantized TFLite model for deployment to Arduino
# After conversion, must convert to TFLite flatbuffer with command:
# xxd -i <quantized_model>.tflite > <gesture_model_data>.cc
def deploy_model():
    saved_model_dir = '../saved_models/tilt_gestures_model_aug_acc'
    unquantized_tflite_model_dir = '../saved_models/tilt_gestures_model_aug_acc_unquant.tflite'
    quantized_tflite_model_dir = '../saved_models/tilt_gestures_model_aug_acc_quant.tflite'

    converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
    converter.representative_dataset = representative_dataset_gen
    model_no_quant_tflite = converter.convert()
    # Saved unquantized model
    open(unquantized_tflite_model_dir, "wb").write(model_no_quant_tflite)
    # Set the optimization flag.
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    # Enforce full-int8 quantization (except inputs/outputs which are always float)
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]

    model_tflite = converter.convert()
    # Saved quantized model
    open(quantized_tflite_model_dir, "wb").write(model_tflite)

    # Compare model sizes
    model_no_quant_size = os.path.getsize(unquantized_tflite_model_dir)
    print("Model is %d bytes" % model_no_quant_size)
    model_size = os.path.getsize(quantized_tflite_model_dir)
    print("Quantized model is %d bytes" % model_size)
    difference = model_no_quant_size - model_size
    print("Difference is %d bytes" % difference)

    # Evaluate quantized tflite model on_dataset
    data_dict, sample_rate = load_data(path, users, gestures, num_takes, seq_length)
    (X, y) = data_dict['david']
    X = X[:, :, 0:5:2, np.newaxis] # only accelerometer data, add channels axis
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)
    batch_size = 4
    ds_test = tf.data.Dataset.from_tensor_slices((X_test, y_test)).shuffle(len(X_test)).batch(batch_size)

    # Load TFLite model and allocate tensors.
    interpreter = tf.lite.Interpreter(model_path=quantized_tflite_model_dir)
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Test TFlite model
    input_shape = input_details[0]['shape']
    num_correct = 0
    for n in range(X_test.shape[0]):
        data_point = X_test[n,:,:,:]
        data_point = data_point[np.newaxis,:,:,:]
        input_data = data_point.astype('float32')
        interpreter.set_tensor(input_details[0]['index'], input_data)

        interpreter.invoke()

        output_gesture = np.argmax(interpreter.get_tensor(output_details[0]['index']))
        if output_gesture == y_test[n]:
            num_correct += 1

    post_quant_accuracy = num_correct/X_test.shape[0]

    # Test original Keras model
    model_unquant = tf.keras.models.load_model(saved_model_dir)
    results = model_unquant.evaluate(ds_test, verbose=0)

    print('Pre quant accuracy: ', results[1])
    print('Post quant accuracy: ', post_quant_accuracy)



if __name__ == '__main__':
    deploy_model()
