import os
import numpy as np
import tensorflow as tf

def deploy_model():
    model = tf.keras.models.load_model('../saved_models/david_click_gestures_model_raw_and_fused2')
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    model_no_quant_tflite = converter.convert()

    # Saved unquantized model
    open('../saved_models/unquant.tflite', "wb").write(model_no_quant_tflite)
    # Set the optimization flag.
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    # Enforce full-int8 quantization (except inputs/outputs which are always float)
    #converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    model_tflite = converter.convert()
    # Saved quantized model
    open('../saved_models/quant.tflite', "wb").write(model_tflite)

    # Compare model sizes
    model_no_quant_size = os.path.getsize('../saved_models/unquant.tflite')
    print("Model is %d bytes" % model_no_quant_size)
    model_size = os.path.getsize('../saved_models/quant.tflite')
    print("Quantized model is %d bytes" % model_size)
    difference = model_no_quant_size - model_size
    print("Difference is %d bytes" % difference)

if __name__ == '__main__':
    deploy_model()
