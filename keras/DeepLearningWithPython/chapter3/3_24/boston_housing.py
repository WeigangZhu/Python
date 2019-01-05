#!/usr/bin/python3

from keras.datasets import boston_housing
from keras import models
from keras import layers
import numpy as np
import matplotlib.pyplot as plt


#
def data_handle():
    (train_data, train_targets), (test_data, test_targets) = boston_housing.load_data()
    mean = train_data.mean(axis = 0)
    train_data -= mean
    std = train_data.std(axis = 0)
    train_data /= std

    test_data -= mean
    test_data /= std 
    
    return (train_data, test_data, train_targets, test_targets)

#
def build_model(train_data):
    model = models.Sequential()
    model.add(layers.Dense(64, activation = 'relu', input_shape = (train_data.shape[1],)))
    model.add(layers.Dense(1))
    model.compile(optimizer = 'rmsprop', loss = 'mse', metrics = ['mae'])
    return model


#
def K_test():
    k = 4
    (train_data, test_data, train_targets, test_targets) = data_handle()
    num_val_samples = len(train_data) // k
    num_epochs = 500
    all_mae_histories = []


    for i in range(k):
        print('processing fold #', i)
        val_data = train_data[i*num_val_samples:(i+1)*num_val_samples]
        val_targets = train_targets[i*num_val_samples:(i+1)*num_val_samples]

        partial_train_data = np.concatenate(
            [train_data[:i*num_val_samples], 
            train_data[(i+1)*num_val_samples:]],
            axis = 0)
        partial_train_targets = np.concatenate(
            [train_targets[:i*num_val_samples],
            train_targets[(i+1)*num_val_samples:]],
            axis = 0)

        model = build_model(train_data)
        history = model.fit(partial_train_data, partial_train_targets,
                validation_data = (val_data, val_targets),
                epochs = num_epochs, batch_size = 1, verbose = 0)
        
        mae_history = history.history['val_mean_absolute_error']
        all_mae_histories.append(mae_history)

    average_mae_histroy = [
        np.mean([x[i] for x in all_mae_histories]) for i in range(num_epochs)]

    plt.plot(range(1, len(average_mae_histroy) + 1), average_mae_histroy)
    plt.xlabel('Epochs')
    plt.ylabel('Validation MAE')
    plt.show()


##############################################################################



if __name__ == '__main__':
    K_test()
