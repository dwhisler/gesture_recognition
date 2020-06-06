import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split

gesture_map = {'none':0, 'up':1, 'down':2, 'right':3}
gesture_map_reverse = {0:'none', 1:'up', 2:'down', 3:'right'}

# Loads data and labels from directory into a numpy array inside a dict of users
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

# Augments training data by shifting along time axis
def augment_data(X, y):
    seq_length = X.shape[1]

    X_aug = []
    y_aug = []
    for n in range(X.shape[0]):
        Xn = X[n,:,:]
        yn = y[n]
        for i in range(seq_length):
            X_shift = np.roll(Xn, i, axis=0)
            X_aug.append(X_shift)
            y_aug.append(yn)

    X_aug = np.stack(X_aug, axis=0)
    y_aug = np.stack(y_aug, axis=0)

    return X_aug, y_aug

# Builds Keras model
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

# Trains Keras model
def train_model():
    path = '../data/session5/'
    users = ['david']
    gestures = ['none', 'up', 'down', 'right']
    num_takes = 50
    seq_length = 256
    num_classes = len(gestures)
    data_dict, sample_rate = load_data(path, users, gestures, num_takes, seq_length)
    X, y = data_dict['david']

    X, y = augment_data(X, y)

    X = X[:, :, :, np.newaxis] # add channels axis (1)

    X = X[:, :, 0:5:2] # acceleration data only
    # X = X[:, :, 1:6:2] # gyroscope data only
    # X = X[:, :, 6:] # quaternion data only
    # X = X[:, :, :6] # acceleration & gyro data only
    # X = np.concatenate((X[:,:,0:5:2], X[:,:,6:]), axis=2) # acceleration and quaternion data only

    data_axes = X.shape[2]

    model = build_model(data_axes, seq_length, num_classes)
    model.summary()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)

    batch_size = 4
    ds_train = tf.data.Dataset.from_tensor_slices((X_train, y_train)).shuffle(len(X_train)).batch(batch_size)
    ds_test = tf.data.Dataset.from_tensor_slices((X_test, y_test)).shuffle(len(X_test)).batch(batch_size)

    epochs = 2

    learning_rate = 1e-3
    loss = 'sparse_categorical_crossentropy'
    metrics = ['accuracy']
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

    model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

    model.fit(ds_train, epochs=epochs, validation_data=ds_test)
    model.evaluate(ds_test)

    model.save('../saved_models/rel_gestures_model_aug_acc')


if __name__ == '__main__':
    train_model()
