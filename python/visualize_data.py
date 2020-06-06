import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from train_gesture_model import load_data

gesture_map = {'none':0, 'up':1, 'down':2, 'right':3}
gesture_map_reverse = {0:'none', 1:'up', 2:'down', 3:'right'}

# Visualizes a training example by plotting over time
def visualize_data():
    path = '../data/session4/'
    users = ['david']
    gestures = ['none', 'up', 'down', 'right']
    seq_length = 256
    num_takes = 50
    data_dict, sample_rate = load_data(path, users, gestures, num_takes, seq_length)
    (X, y) = data_dict['david']

    ex = X[2,:,:]

    fig, ax = plt.subplots(1,3)
    # Acceleration
    ax[0].plot(np.arange(seq_length), ex[:,0])
    ax[0].plot(np.arange(seq_length), ex[:,2])
    ax[0].plot(np.arange(seq_length), ex[:,4])
    ax[0].set_title('Acceleration')
    # Gyroscope
    ax[1].plot(np.arange(seq_length), ex[:,1])
    ax[1].plot(np.arange(seq_length), ex[:,3])
    ax[1].plot(np.arange(seq_length), ex[:,5])
    ax[1].set_title('Gyroscope')
    # Quaternion
    ax[2].plot(np.arange(seq_length), ex[:,6])
    ax[2].plot(np.arange(seq_length), ex[:,7])
    ax[2].plot(np.arange(seq_length), ex[:,8])
    ax[2].plot(np.arange(seq_length), ex[:,9])
    ax[2].set_title('Quaternion')

    plt.show()

if __name__ == '__main__':
    visualize_data()
