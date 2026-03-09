import tensorflow as tf
from VAE import vae
import numpy as np
import xlrd, xlsxwriter


def VAE_decoder(latent_vectors):
    tf.reset_default_graph()
    x = tf.placeholder(tf.float32, [None, 50, 50, 1])
    learning_rate = tf.placeholder(tf.float32)
    optimizer, loss, output, z_mean, z_log_var, z = vae(x, learning_rate)
    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        saver.restore(sess, 'VAE/VAE.ckpt')
        images = sess.run(output, feed_dict={z: latent_vectors})
        images = np.round(images)
    return images


def save_images_excel(x, lvs, filename):
    x = x.reshape(-1, 50*50)
    book = xlsxwriter.Workbook(filename)
    sheet1 = book.add_worksheet('images')
    sheet2 = book.add_worksheet('soil_parameters')
    sheet3 = book.add_worksheet('filling_fractions')
    sheet4 = book.add_worksheet('latent_vectors')
    Es = np.random.uniform(1, 990, x.reshape[0])
    Ps = np.random.uniform(0.15, 0.45, x.shape[0])
    rhos = np.random.uniform(1.5, 2.2, x.shape[0])
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            sheet1.write(i, j, x[i, j])
        sheet2.write(i, 0, Es[i])
        sheet2.write(i, 1, Ps[i])
        sheet2.write(i, 2, rhos[i])
        sheet3.write(i, 0, np.mean(x[i]))
        for j in range(lvs.shape[1]):
            sheet4.write(i, j, lvs[i, j])
    book.close()


for i in range(5):
    lvs = np.random.uniform([-2, -2, -2], [2, 2, 2], [10000, 3])
    images = VAE_decoder(lvs)
    save_images_excel(images, lvs, 'dataset/generated_images_for_FEM/'+str(i)+'.xlsx')

















