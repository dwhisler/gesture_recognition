import os
import numpy as np
import tensorflow as tf
from train_gesture_model import load_data
from sklearn.model_selection import train_test_split

def representative_dataset_gen():
    path = '../data/session2/'
    users = ['david']
    gestures = ['none', 'click', 'doubleclick', 'rightcircle', 'leftcircle']
    num_takes = 10
    seq_length = 255
    data_dict, sample_rate = load_data(path, users, gestures, num_takes, seq_length)
    (X, y) = data_dict['david']
    for i in range(X.shape[0]):
        data = X[i,:,:]
        data = data[np.newaxis,:,:,np.newaxis]
        data = data.astype(np.float32)
        yield [data]

def deploy_model():
    saved_model_dir = '../saved_models/david_click_gestures_model_raw_and_fused'

    converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
    converter.representative_dataset = representative_dataset_gen
    model_no_quant_tflite = converter.convert()
    # Saved unquantized model
    open('../saved_models/unquant_raw_and_fused.tflite', "wb").write(model_no_quant_tflite)
    # Set the optimization flag.
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    # Enforce full-int8 quantization (except inputs/outputs which are always float)
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]

    model_tflite = converter.convert()
    # Saved quantized model
    open('../saved_models/quant_raw_and_fused.tflite', "wb").write(model_tflite)

    # Compare model sizes
    model_no_quant_size = os.path.getsize('../saved_models/unquant_raw_and_fused.tflite')
    print("Model is %d bytes" % model_no_quant_size)
    model_size = os.path.getsize('../saved_models/quant_raw_and_fused.tflite')
    print("Quantized model is %d bytes" % model_size)
    difference = model_no_quant_size - model_size
    print("Difference is %d bytes" % difference)

    # Evaluate quantized tflite model on_dataset
    path = '../data/session2/'
    users = ['david']
    gestures = ['none', 'click', 'doubleclick', 'rightcircle', 'leftcircle']
    num_takes = 10
    seq_length = 255
    data_dict, sample_rate = load_data(path, users, gestures, num_takes, seq_length)
    (X, y) = data_dict['david']
    X = X[:, :, :, np.newaxis] # add channels axis (1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)
    batch_size = 4
    ds_test = tf.data.Dataset.from_tensor_slices((X_test, y_test)).shuffle(len(X_test)).batch(batch_size)

    # Load TFLite model and allocate tensors.
    interpreter = tf.lite.Interpreter(model_path='../saved_models/quant_raw_and_fused.tflite')
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Test model on random input data.
    input_shape = input_details[0]['shape']
    num_correct = 0
    for n in range(X_test.shape[0]):
        data_point = X_test[n,:,:,:]
        data_point = data_point[np.newaxis,:,:,:]
        input_data = data_point.astype('float32')
        interpreter.set_tensor(input_details[0]['index'], input_data)

        interpreter.invoke()

        # The function `get_tensor()` returns a copy of the tensor data.
        # Use `tensor()` in order to get a pointer to the tensor.
        output_gesture = np.argmax(interpreter.get_tensor(output_details[0]['index']))
        if output_gesture == y_test[n]:
            num_correct += 1

    post_quant_accuracy = num_correct/X_test.shape[0]

    model_unquant = tf.keras.models.load_model('../saved_models/david_click_gestures_model_raw_and_fused')
    results = model_unquant.evaluate(ds_test, verbose=0)

    print('Pre quant accuracy: ', results[1])
    print('Post quant accuracy: ', post_quant_accuracy)



if __name__ == '__main__':
    deploy_model()
