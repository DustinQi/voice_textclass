'''
Created on 2018年3月21日

@author: qimy
该部分利用softmax训练后的结果进行测试。
'''

import tensorflow as tf
from dataset import datasets

test_text_dir = "D:/Users/qimy/softWare/eclipse/workspace/voiceasr-tensorflow/test_set"
model_dir = "D:/Users/qimy/softWare/eclipse/workspace/voiceasr-tensorflow"

data_sets = datasets()
data_sets.read_test_data(test_text_dir, True)

sess = tf.InteractiveSession()

x = tf.placeholder(tf.float32, [None, 5000])  #None占位符标示输入样本的数量，5000为单个样本的输入维度，对应字典维度
w = tf.Variable(tf.zeros([5000, 8]))  # 权重矩阵，行为输入维度，列为输出维度，这里为类别的数目8
b = tf.Variable(tf.zeros([8]))  # 偏重为8对应输出的维度
y = tf.nn.softmax(tf.matmul(x, w)+b)  # 定义训练输出结果，使用softmax作为激励函数，tf.matmul(x, W) + b为输入参数，tf.matmul为矩阵乘
y_ = tf.placeholder(tf.float32, [None, 8])

saver = tf.train.Saver()
saver.restore(sess, model_dir+"/model2/model.md")

correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
acc = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print(acc.eval({x: data_sets.test.text, y_: data_sets.test.label}))
