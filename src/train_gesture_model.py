import serial
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

gesture_map = {'none':0, 'click':1, 'doubleclick':2, 'rightcircle':3, 'leftcircle':4}
gesture_map_reverse = {0:'none', 1:'click', 2:'doubleclick', 3:'rightcircle', 4:'leftcircle'}


def find_min_num_samples(path, users, gestures, num_takes):
    min_count = 1000
    for u in users:
        for g in gestures:
            for n in range(1, num_takes+1):
                fname = path + u + '_' + g + '_' + str(n) + '.csv'
                with open(fname, 'r') as f:
                    header = f.readline()
                    count = 0
                    for data_point in f:
                        count += 1
                    if count < min_count:
                        min_count = count
    return min_count

def load_data(path, users, gestures, num_takes, seq_length):
    data_dict = {}
    for u in users:
        user_batch = []
        user_labels = []
        for g in gestures:
            for nt in range(1, num_takes+1):
                fname = path + u + '_' + g + '_' + str(nt) + '.csv'
                with open(fname, 'r') as f:
                    header = f.readline()
                    data = []
                    for ns in range(seq_length):
                        new_data = np.array([float(x) for x in f.readline().split(',')[:-1]])
                        sample_rate = new_data[-1]
                        data.append(new_data[:-1])

                    data = np.stack(data, axis=0)

                user_batch.append(data)
                user_labels.append(gesture_map[g])

        user_labels = np.array(user_labels)
        user_batch = np.stack(user_batch, axis=0)
        data_dict[u] = (user_batch, user_labels)

    return data_dict, sample_rate

def build_model(data_axes, seq_length, num_classes):
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Conv2D(8, (4, data_axes), padding='same', activation='relu', input_shape=(seq_length, data_axes, 1)))
    model.add(tf.keras.layers.MaxPool2D((3, data_axes)))
    model.add(tf.keras.layers.Dropout(0.1))
    model.add(tf.keras.layers.Conv2D(16, (4, 1), padding='same', activation='relu'))
    model.add(tf.keras.layers.Dropout(0.1))
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(16, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.1))
    model.add(tf.keras.layers.Dense(num_classes, activation='softmax'))

    return model

def visualize_examples():
    path = '../data/session2/'
    users = ['david']
    gestures = ['none', 'click', 'doubleclick', 'rightcircle', 'leftcircle']
    num_takes = 10
    seq_length = 255
    num_classes = 5
    data_dict, sample_rate = load_data(path, users, gestures, num_takes, seq_length)
    (X, y) = data_dict['david']

    none_ex = X[0,:,:]
    click_ex = X[10,:,:]
    doubleclick_ex = X[20,:,:]
    rightcircle_ex = X[30,:,:]
    leftcircle_ex = X[40,:,:]

    ex = click_ex
    seq_length = len(click_ex[:,0])

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

def train_model():
    path = '../data/session2/'
    users = ['david']
    gestures = ['none', 'click', 'doubleclick', 'rightcircle', 'leftcircle']
    num_takes = 10
    seq_length = 255
    num_classes = 5
    data_dict, sample_rate = load_data(path, users, gestures, num_takes, seq_length)
    (X, y) = data_dict['david']
    X = X[:, :, :, np.newaxis] # add channels axis (1)

    #X = X[:, :, 0:5:2] # acceleration data only
    #X = X[:, :, -4:] # quaternion data only
    #X = X[:, :, :6] # acceleration & gyro data only
    data_axes = X.shape[2]

    model = build_model(data_axes, seq_length, num_classes)
    model.summary()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)

    batch_size = 4
    ds_train = tf.data.Dataset.from_tensor_slices((X_train, y_train)).shuffle(len(X_train)).batch(batch_size)
    ds_test = tf.data.Dataset.from_tensor_slices((X_test, y_test)).shuffle(len(X_test)).batch(batch_size)

    epochs = 50

    learning_rate = 1e-3
    loss = 'sparse_categorical_crossentropy'
    metrics = ['accuracy']
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

    model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

    model.fit(ds_train, epochs=epochs, validation_data=ds_test)
    model.evaluate(ds_test)

    model.save('../saved_models/david_click_gestures_model_raw_and_fused')


if __name__ == '__main__':
    #visualize_examples()
    train_model()
