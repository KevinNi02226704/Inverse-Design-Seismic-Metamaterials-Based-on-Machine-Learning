import tensorflow as tf


def decoder(x):
    x = tf.layers.flatten(x)

    x = tf.layers.dense(x, 512)
    x = tf.layers.batch_normalization(x)
    x = tf.nn.relu(x)

    x = tf.layers.dense(x, 1024)
    x = tf.layers.batch_normalization(x)
    x = tf.nn.relu(x)

    x = tf.layers.dense(x, 5*5*128)
    x = tf.layers.batch_normalization(x)
    x = tf.nn.relu(x)

    x = tf.reshape(x, [-1, 5, 5, 128])

    # o = s*(i-1)+k
    x = tf.layers.conv2d_transpose(x, filters=64, kernel_size=3, strides=2)  # 11
    x = tf.layers.batch_normalization(x)
    x = tf.nn.relu(x)

    x = tf.layers.conv2d_transpose(x, filters=48, kernel_size=3, strides=2)  # 23
    x = tf.layers.batch_normalization(x)
    x = tf.nn.relu(x)

    x = tf.layers.conv2d_transpose(x, filters=32, kernel_size=3, strides=2)  # 47
    x = tf.layers.batch_normalization(x)
    x = tf.nn.relu(x)

    x = tf.layers.conv2d_transpose(x, filters=16, kernel_size=3, strides=1)  # 49
    x = tf.layers.batch_normalization(x)
    x = tf.nn.relu(x)

    x = tf.layers.conv2d_transpose(x, filters=1, kernel_size=2, strides=1)  # 50
    x = tf.layers.batch_normalization(x)

    x1 = tf.reshape(x, [-1, 50, 50, 1])
    x2 = tf.image.rot90(x1)
    x3 = tf.image.rot90(x2)
    x4 = tf.image.rot90(x3)
    x5 = tf.reverse(x1, axis=[2])
    x6 = tf.reverse(x2, axis=[1])
    x7 = tf.reverse(x3, axis=[2])
    x8 = tf.reverse(x4, axis=[1])
    x = (x1+x2+x3+x4+x5+x6+x7+x8)/8
    x = tf.nn.sigmoid(x)
    return x
















