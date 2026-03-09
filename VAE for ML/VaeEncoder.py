import numpy as np
import tensorflow as tf


def encoder(x, n_z):

    x = tf.layers.conv2d(x, filters=16, kernel_size=3, strides=1)  # 48
    x = tf.layers.batch_normalization(x)
    x = tf.nn.relu(x)
    x = tf.layers.conv2d(x, filters=32, kernel_size=3, strides=1)  # 46
    x = tf.layers.batch_normalization(x)
    x = tf.nn.relu(x)
    x = tf.layers.max_pooling2d(x, pool_size=2, strides=2)  # 23
    x = tf.layers.batch_normalization(x)
    x = tf.nn.relu(x)

    x = tf.layers.conv2d(x, filters=48, kernel_size=3, strides=1)  # 21
    x = tf.layers.batch_normalization(x)
    x = tf.nn.relu(x)
    x = tf.layers.max_pooling2d(x, pool_size=2, strides=2)  # 10
    x = tf.layers.batch_normalization(x)
    x = tf.nn.relu(x)

    x = tf.layers.conv2d(x, filters=64, kernel_size=3, strides=1)  # 8
    x = tf.layers.batch_normalization(x)
    x = tf.nn.relu(x)
    x = tf.layers.max_pooling2d(x, pool_size=2, strides=2)  # 4
    x = tf.layers.batch_normalization(x)
    x = tf.nn.relu(x)

    x = tf.layers.conv2d(x, filters=128, kernel_size=3, strides=1)  # 2
    x = tf.layers.batch_normalization(x)
    x = tf.nn.relu(x)
    x = tf.layers.max_pooling2d(x, pool_size=2, strides=2)  # 1
    x = tf.layers.batch_normalization(x)
    x = tf.nn.relu(x)

    x = tf.layers.flatten(x)  # 1*128
    x = tf.layers.dense(x, 512)
    x = tf.layers.batch_normalization(x)
    x = tf.nn.relu(x)

    x = tf.layers.dense(x, 256)
    x = tf.layers.batch_normalization(x)
    x = tf.nn.relu(x)
    x = tf.layers.dense(x, 128)
    x = tf.layers.batch_normalization(x)

    w1 = tf.Variable(tf.truncated_normal([128, n_z], stddev=0.1), name='w1')
    b1 = tf.Variable(tf.zeros([1]), name='b1')
    w2 = tf.Variable(tf.truncated_normal([128, n_z], stddev=0.1), name='w2')
    b2 = tf.Variable(tf.zeros([1]), name='b2')
    z_mean = tf.matmul(x, w1)+b1
    z_log_var = tf.matmul(x, w2)+b2
    return z_mean, z_log_var




































