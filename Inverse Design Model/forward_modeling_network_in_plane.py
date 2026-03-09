import tensorflow as tf
import xlrd, xlsxwriter
import numpy as np


def normalized_data(x):
    x_max = np.max(x, axis=0)
    x_min = np.min(x, axis=0)
    x = (x-x_min)/(x_max-x_min)
    return x, x_max, x_min


# 数据去归一化
def denormalized_data(x, x_max, x_min):
    return x*(x_max-x_min)+x_min


def calculate_accuracy(x1, x2):
    a = np.abs(x1-x2)
    b = x2
    acc = 1.0-np.mean(np.divide(a, b, out=np.zeros_like(a), where=b!=0), axis=1)  # 如果b中的某个元素为零，则输出零，避免输出inf或None
    return acc


def load_data(filename):
    book = xlrd.open_workbook(filename)
    sheet1 = book.sheet_by_name('latent_vectors')
    sheet2 = book.sheet_by_name('soil_parameters')
    sheet3 = book.sheet_by_name('in_plane')
    m, n1, n2, n3 = sheet1.nrows, sheet1.ncols, sheet2.ncols, sheet3.ncols
    lvs = np.zeros((m, n1))
    sps = np.zeros((m, n2))
    bgs = np.zeros((m, n3))
    for i in range(m):
        for j in range(n1):
            lvs[i, j] = sheet1.cell(i, j).value
        for j in range(n2):
            sps[i, j] = sheet2.cell(i, j).value
        for j in range(n3):
            bgs[i, j] = sheet3.cell(i, j).value

    lvs, lvs_max, lvs_min = normalized_data(lvs)
    sps, sps_max, sps_min = normalized_data(sps)
    bgs, bgs_max, bgs_min = normalized_data(bgs)

    tr_lvs, va_lvs, te_vs = lvs[:int(m*0.8)], lvs[int(m*0.8):int(m*0.9)], lvs[int(m*0.9):m]
    tr_sps, va_sps, te_sps = sps[:int(m*0.8)], sps[int(m*0.8):int(m*0.9)], sps[int(m*0.9):m]
    tr_bgs, va_bgs, te_bgs = bgs[:int(m*0.8)], bgs[int(m*0.8):int(m*0.9)], bgs[int(m*0.9):m]

    return tr_lvs, va_lvs, te_vs,  tr_sps, va_sps, te_sps, tr_bgs, va_bgs, te_bgs, lvs_max, lvs_min, sps_max, sps_min, bgs_max, bgs_min


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


def training_model():
    tr_lvs, va_lvs, te_vs, tr_sps, va_sps, te_sps, tr_bgs, va_bgs, te_bgs, lvs_max, lvs_min, sps_max, sps_min, bgs_max, bgs_min = load_data('dataset/dataset_for_2D_binary_design.xlsx')
    print(lvs_max, lvs_min, sps_max, sps_min, bgs_max, bgs_min)
    x_lv = tf.placeholder(tf.float32, [None, tr_lvs.shape[1]])
    x_sp = tf.placeholder(tf.float32, [None, tr_sps.shape[1]])
    y = tf.placeholder(tf.float32, [None, tr_bgs.shape[1]])

    x = tf.concat([x_lv, x_sp], axis=1)

    output = MLP(x)

    loss = tf.reduce_mean(tf.square(output-y))

    optimizer = tf.train.AdamOptimizer(1e-3).minimize(loss)

    tr_acc, va_acc, tr_loss_history, va_loss_history = [], [], [], []

    saver = tf.train.Saver()

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for epoch in range(1000):
            sess.run(optimizer, feed_dict={x_lv: tr_lvs, x_sp: tr_sps, y: tr_bgs})

            if (epoch+1)%10 == 0:
                tr_loss_value = sess.run(loss, feed_dict={x_lv: tr_lvs, x_sp: tr_sps, y: tr_bgs})
                va_loss_value = sess.run(loss, feed_dict={x_lv: va_lvs, x_sp: va_sps, y: va_bgs})
                tr_loss_history.append(tr_loss_value)
                va_loss_history.append(va_loss_value)

                tr_p = sess.run(output, feed_dict={x_lv: tr_lvs, x_sp: tr_sps})
                va_p = sess.run(output, feed_dict={x_lv: va_lvs, x_sp: va_sps})
                tr_acc.append(np.mean(calculate_accuracy(denormalized_data(tr_p, bgs_max, bgs_min), denormalized_data(tr_bgs, bgs_max, bgs_min))))
                va_acc.append(np.mean(calculate_accuracy(denormalized_data(va_p, bgs_max, bgs_min), denormalized_data(va_bgs, bgs_max, bgs_min))))
                print(epoch, ' 训练集精度|验证集精度：', tr_acc[-1], '|', va_acc[-1])

            if (epoch+1)%100 ==0:
                saver.save(sess, 'pretrained_models/pretrained_forward_modeling_network_for_in_plane_waves.ckpt')
                print('Model has been saved!')


training_model()

















