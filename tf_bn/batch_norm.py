from __future__ import division, print_function, absolute_import

import tflearn
from tflearn.data_utils import shuffle, to_categorical
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation

from tflearn.layers.normalization import batch_normalization

# prepairing datasets
from tflearn.datasets import cifar10
(X, Y), (X_test, Y_test) = cifar10.load_data()
X, Y = shuffle(X, Y)
Y = to_categorical(Y, 10)
Y_test = to_categorical(Y_test, 10)

# Normalization and Augmentation
img_prep = ImagePreprocessing()
img_prep.add_featurewise_zero_center()
img_prep.add_featurewise_stdnorm()

img_aug = ImageAugmentation()
img_aug.add_random_flip_leftright()
img_aug.add_random_rotation(max_angle=25.)

# constructing CNN
network = input_data(shape=[None, 32, 32, 3], data_preprocessing=img_prep, data_augmentation=img_aug)
network = conv_2d(network, 32, 3, activation='tanh')
network = max_pool_2d(network, 2)
network = conv_2d(network, 64, 3, activation='tanh')
network = conv_2d(network, 64, 3, activation='tanh')
network = batch_normalization(network)
network = max_pool_2d(network, 2)
network = fully_connected(network, 512, activation='tanh')
network = batch_normalization(network)
network = fully_connected(network, 10, activation='softmax')
network = regression(network, optimizer='sgd', loss='categorical_crossentropy', learning_rate=0.03)

model = tflearn.DNN(network, tensorboard_verbose=0)
model.fit(X, Y, n_epoch=50, shuffle=True, validation_set=(X_test, Y_test), show_metric=True, batch_size=96, run_id='Normalization')