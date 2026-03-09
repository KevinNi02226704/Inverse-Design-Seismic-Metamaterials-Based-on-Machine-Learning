import tensorflow as tf
from VAE import vae
from VaeDecoder import decoder
import matplotlib.pylab as plt
import numpy as np
from PIL import Image
import xlrd, xlsxwriter


def load_data(num=1):
    ims = np.zeros((num*10000, 50*50))
    for i in range(num):
        book = xlrd.open_workbook('dataset/training_VAE/'+str(i+40)+'.xlsx')
        sheet = book.sheet_by_name('images')
        for k in range(10000):
            for l in range(50*50):
                ims[int(k+i*10000), l] = int(sheet.cell(k, l).value)
    return ims.reshape(-1, 50, 50, 1)


def save_error(x, filename):
    book = xlsxwriter.Workbook(filename)
    sheet = book.add_worksheet('sheet1')
    for i in range(x.shape[0]):
        sheet.write(i, 0, x[i])
    book.close()


x = tf.placeholder(tf.float32, [None, 50, 50, 1])
learning_rate = tf.placeholder(tf.float32)
optimizer, loss, output, z_mean, z_log_var, z = vae(x, learning_rate)
saver = tf.train.Saver()

with tf.Session() as sess:
    ims = load_data(1)
    sess.run(tf.global_variables_initializer())
    saver.restore(sess, 'VAE/VAE.ckpt')
    batch_size = 2000
    batch_num = 1 #int(ims.shape[0]/batch_size)
    ims_all = np.zeros((batch_size*batch_num, 50, 100))
    for k in range(batch_num):
        test_x = ims[k*batch_size:(k+1)*batch_size]
        restore_images = sess.run(output, feed_dict={x: test_x})
        c_im = np.concatenate([restore_images.reshape(-1, 50, 50), test_x.reshape(-1, 50, 50)], axis=2)
        c_im = np.round(c_im)
        ims_all[k*batch_size:(k+1)*batch_size] = c_im
    for i in range(100):
        im = ims_all[i].reshape(50, 100)/2
        im = 1-im
        im = np.matrix(im, dtype='float')*255
        im = Image.fromarray(im.astype(np.uint8))
        im.save('testing_VAE/comparisons/'+str(k*batch_num+i)+'.jpg')


    err = 1-np.mean(1*np.equal(ims_all[:, :, :50].reshape(ims_all.shape[0], -1), ims_all[:, :, 50:].reshape(ims_all.shape[0], -1)), axis=1)
    save_error(err, 'testing_VAE/error.xlsx')
    print(np.max(err), np.mean(err))
    plt.hist(err, bins=15)
    plt.show()












