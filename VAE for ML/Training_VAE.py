import tensorflow as tf
import numpy as np
from VAE import vae
import xlrd


def load_data(num=1):
    ims = np.zeros((num*10000, 50*50))
    for i in range(num):
        book = xlrd.open_workbook('dataset/training_VAE/'+str(i)+'.xlsx')
        sheet = book.sheet_by_name('images')
        for k in range(10000):
            for l in range(50*50):
                ims[int(k+i*10000), l] = int(sheet.cell(k, l).value)
    return ims.reshape(-1, 50, 50, 1)


num = 1
ims = load_data(num)
tr_x = ims[:int(num*10000*0.9)]
va_x = ims[int(num*10000*0.9):int(num*10000*1)]
x = tf.placeholder(tf.float32, [None, 50, 50, 1])
learning_rate = tf.placeholder(tf.float32)
optimizer, loss, output, z_mean, z_log_var, z = vae(x, learning_rate)

tr_loss = []
va_loss = []

saver = tf.train.Saver()

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    lr = 1e-4

    batch_size = 20
    batch_num = int(tr_x.shape[0]/batch_size)
    for epoch in range(1000000):
        tr_lv = 0
        for i in range(batch_num):
            _, loss_v = sess.run([optimizer, loss], feed_dict={x: tr_x[i*batch_size:(i+1)*batch_size], learning_rate: lr})
            tr_lv = tr_lv+loss_v
        tr_loss.append(tr_lv/batch_num)

        va_lv = 0
        v_num = 1000
        for i in range(int(va_x.shape[0]/v_num)):
            loss_v = sess.run(loss, feed_dict={x: va_x[i*v_num:(i+1)*v_num], learning_rate: lr})
            va_lv = va_lv+loss_v
        va_loss.append(va_lv/int(va_x.shape[0]/v_num))
        print(epoch, 'training loss:', tr_loss[-1], '|', 'validation loss', va_loss[-1])
        if epoch > 10 and tr_loss[-1] <= np.min(tr_loss):
            saver.save(sess, 'VAE/VAE.ckpt')
            print('VAE has been saved!')

















