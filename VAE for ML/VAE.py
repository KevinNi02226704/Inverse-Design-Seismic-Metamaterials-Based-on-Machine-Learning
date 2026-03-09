import tensorflow as tf
from VaeEncoder import encoder
from VaeDecoder import decoder


def vae(x, lr):
    z_n = 3
    miu, log_var = encoder(x, z_n)
    eps = tf.random_normal((tf.shape(miu)), 0, 1, dtype=tf.float32)
    z = miu+tf.exp(log_var/2)*eps
    x_reconstr_mean = decoder(z)

    reconstr_loss = -tf.reduce_sum(tf.reshape(x, (-1, 50*50))*tf.log(1e-7+tf.reshape(x_reconstr_mean, (-1, 50*50)))+(1-tf.reshape(x, (-1, 50*50)))*tf.log(1e-7+1-tf.reshape(x_reconstr_mean, (-1, 50*50))), 1)

    latent_loss = -0.5*tf.reduce_sum(1+log_var-miu**2-tf.exp(log_var), 1)
    cost = tf.reduce_mean(reconstr_loss+latent_loss)
    optimizer = tf.train.AdamOptimizer(lr).minimize(cost)
    return optimizer, cost, x_reconstr_mean, miu, log_var, z