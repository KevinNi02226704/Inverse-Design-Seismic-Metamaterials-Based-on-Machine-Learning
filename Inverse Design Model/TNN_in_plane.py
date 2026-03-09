import tensorflow as tf
import xlrd, xlsxwriter
import numpy as np
import time
from PIL import Image
from VAE import vae


def data_max_min():
    bg_max = np.array([856.62599899, 1050.99363584, 1275.77413043, 1109.95870452, 1275.79041984, 1176.1276015]).reshape(1, 6)
    bg_min = np.array([16.91745922, 17.7592743, 20.60484015, 19.13586242, 23.91920225, 21.22547942]).reshape(1, 6)
    s_max = np.array([9.99996773e+02, 4.49996706e-01, 2.19998187e+00]).reshape(1, 3)
    s_min = np.array([1.00969092, 0.15000441, 1.50002107]).reshape(1, 3)
    lv_max = np.array([1.99995557, 1.99978886, 1.99998289]).reshape(1, 3)
    lv_min = np.array([-1.99975419, -1.99990383, -1.99995594]).reshape(1, 3)
    return bg_max, bg_min, s_max, s_min, lv_max, lv_min


def load_targets(filename):
    book = xlrd.open_workbook(filename)
    sheet1 = book.sheet_by_name('targeted_bandgaps')
    sheet2 = book.sheet_by_name('soil_parameters')
    m, n1, n2 = sheet1.nrows, sheet1.ncols, sheet2.ncols
    t_bgs = np.zeros((m, n1))
    s = np.zeros((m, n2))
    for i in range(m):
        for j in range(n1):
            t_bgs[i, j] = sheet1.cell(i, j).value
        for j in range(n2):
            s[i, j] = sheet2.cell(i, j).value
    return t_bgs, s


def save_designed_results(images, lvs, a, s, t_bg, loss_v, filename):
    images = images.reshape(-1, 50*50)
    book = xlsxwriter.Workbook(filename)
    sheet1 = book.add_worksheet('designed_images')
    sheet2 = book.add_worksheet('designed_latent_vectors')
    sheet3 = book.add_worksheet('designed_periodic_constants')
    sheet4 = book.add_worksheet('soil_parameters')
    sheet5 = book.add_worksheet('targeted_bandgaps')
    sheet6 = book.add_worksheet('loss_value')
    for i in range(images.shape[0]):
        for j in range(images.shape[1]):
            sheet1.write(i, j, images[i, j])
        for j in range(lvs.shape[1]):
            sheet2.write(i, j, lvs[i, j])
        for j in range(a.shape[1]):
            sheet3.write(i, j, a[i, j])
        for j in range(s.shape[1]):
            sheet4.write(i, j, s[i, j])
        for j in range(t_bg.shape[1]):
            sheet5.write(i, j, t_bg[i, j])
        for j in range(loss_v.shape[1]):
            sheet6.write(i, j, loss_v[i, j])
    book.close()
    for i in range(images.shape[0]):
        im = images[i].reshape(50, 50)
        im = np.matrix(np.round(im), dtype='float')*255
        im = Image.fromarray(im.astype(np.uint8))
        im.save('results/designed_images_in/'+str(i+1)+'.jpg')


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


def inverse_network(t, alpha_a, beta_a):
    with tf.variable_scope('inverse_design_network'):
        l = tf.layers.dense(t, 16)
        l = tf.layers.batch_normalization(l)
        l = tf.nn.tanh(l)

        # 用于输出潜向量
        l_lvs = tf.layers.dense(l, 3)
        l_lvs = tf.layers.batch_normalization(l_lvs)
        designed_lvs_n = (tf.sin(l_lvs)+1)/2

        # 用于输出周期常熟
        l_a = tf.layers.dense(l, 1)
        l_a = tf.layers.batch_normalization(l_a)
        designed_a = (tf.sin(l_a)+1)/2*(beta_a-alpha_a)+alpha_a
    return designed_lvs_n, designed_a


def MLP(p):
    # 非常重要！！！给前向模拟网络内部所有参数（权重w和偏差b）命名相同的“姓氏”，方便TNN运行时所有参数的调用
    with tf.variable_scope('pretrained_forward_modeling_network_for_in_plane_waves'):
        l1 = tf.layers.dense(p, 1024)
        l1 = tf.layers.batch_normalization(l1)
        l1 = tf.nn.relu(l1)

        l2 = tf.layers.dense(l1, 512)
        l2 = tf.layers.batch_normalization(l2)
        l2 = tf.nn.relu(l2)

        l3 = tf.layers.dense(l2, 256)
        l3 = tf.layers.batch_normalization(l3)
        l3 = tf.nn.relu(l3)

        l4 = tf.layers.dense(l3, 256)
        l4 = tf.layers.batch_normalization(l4)
        l4 = tf.nn.relu(l4)

        l5 = tf.layers.dense(l4, 128)
        l5 = tf.layers.batch_normalization(l5)
        l5 = tf.nn.relu(l5)

        l6 = tf.layers.dense(l5, 6)
        l6 = tf.layers.batch_normalization(l6)
        output = tf.nn.sigmoid(l6)
    return output


bg_max, bg_min, s_max, s_min, lv_max, lv_min = data_max_min()

x = tf.placeholder(tf.float32, [None, 2])
c = tf.placeholder(tf.float32, [None, 3])

lv_n, a = inverse_network(x, 0.1, 40)
lv = lv_n*(lv_max-lv_min)+lv_min

c_n = (c-s_min)/(s_max-s_min)

p = tf.concat([lv_n, c_n], axis=1)

pre_bg_n = MLP(p)

pre_bg = (pre_bg_n*(bg_max-bg_min)+bg_min)/a

loss = tf.reduce_mean(tf.square(pre_bg[:, :2]-x))


#######  核心
t_vars = tf.trainable_variables()
updated_variables = [var for var in t_vars if var.name.startswith('inverse_design_network')]
optimizer = tf.train.AdamOptimizer(1e-3).minimize(loss, var_list=updated_variables)

restored_variables = [var for var in t_vars if var.name.startswith('pretrained_forward_modeling_network_for_in_plane_waves')]
saver = tf.train.Saver(restored_variables)
######  核心


with tf.Session() as sess:
    md = 10
    designed_lvs, designed_as, loss_vs = np.zeros((md, 3)), np.zeros((md, 1)), np.zeros((md, 1))

    t_bgs, s_ps = load_targets('targets.xlsx')

    sess.run(tf.global_variables_initializer())
    saver.restore(sess, 'pretrained_models/pretrained_forward_modeling_network_for_in_plane_waves.ckpt')

    start = time.clock()
    for k in range(md):
        input_bg = t_bgs[k].reshape(-1, 2)
        input_s = s_ps[k].reshape(-1, 3)
        for epoch in range(2000):
            _, loss_v = sess.run([optimizer, loss], feed_dict={x: input_bg, c: input_s})
            if epoch > 100 and np.min(loss_v)<1e-4:
                break
        d_lv, d_a = sess.run([lv, a], feed_dict={x: input_bg})
        designed_lvs[k] = d_lv
        designed_as[k] = d_a
        loss_vs[k] = loss_v

        print(k, np.round(loss_v, 2))
    end = time.clock()
    print('It costs:', np,round(end-start, 2), 's')

designed_images = VAE_decoder(designed_lvs)
designed_images = np.round(designed_images.reshape(-1, 50*50))
save_designed_results(designed_images, designed_lvs, designed_as, s_ps, t_bgs, loss_vs, 'results/designed_parameters_in.xlsx')



















