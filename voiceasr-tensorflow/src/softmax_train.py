'''
Created on 2018年3月20日

@author: qimy
该部分利用softmax回归对数据进行训练。
'''

import tensorflow as tf
from dataset import datasets

train_text_dir = "D:/Users/qimy/softWare/eclipse/workspace/voiceasr-tensorflow/training_set"
model_dir = "D:/Users/qimy/softWare/eclipse/workspace/voiceasr-tensorflow"

data_sets = datasets()
data_sets.read_train_data(train_text_dir, True)

sess = tf.InteractiveSession()

x = tf.placeholder(tf.float32, [None, 5000])  #None占位符标示输入样本的数量，5000为单个样本的输入维度，对应字典维度
w = tf.Variable(tf.zeros([5000, 8]))  # 权重矩阵，行为输入维度，列为输出维度，这里为类别的数目8
b = tf.Variable(tf.zeros([8]))  # 偏重为8对应输出的维度
y = tf.nn.softmax(tf.matmul(x, w)+b)  # 定义训练输出结果，使用softmax作为激励函数，tf.matmul(x, W) + b为输入参数，tf.matmul为矩阵乘
  
y_ = tf.placeholder(tf.float32, [None, 8])
cross_entropy = -tf.reduce_sum(y_ * tf.log(y + 1e-10))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
  
# 训练模型
tf.global_variables_initializer().run()
saver = tf.train.Saver()

for i in range(1000):
    batch_xs,batch_ys = data_sets.train.next_batch(100)
    train_step.run({x: batch_xs, y_:batch_ys})
    
print(w.eval())
print(b.eval())
  
path = saver.save(sess, model_dir+"/model2/model.md")









