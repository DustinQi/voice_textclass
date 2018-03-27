'''
Created on 2018年3月16日

@author: qimy
该部分主要包括两部分，一是从磁盘读取向量化后的文本保存到numpy数组，将数据和类别分别存储，
数据保存为二维(text_line_num, 5000)的数组，text_line_num为数据集的文本数，5000为词典的维度，
也是后面模型输入参数的个数。类别保存为标签向量(label_line_num, 1)，label_line_num,同样为数据集的大小。
'''

import numpy
import subprocess
import tensorflow as tf

# d_dir1 = r"d:/Users/qimy/Desktop/qmy/training.txt"
# d_dir2 = r"d:/Users/qimy/Desktop/qmy/training_labels.txt"

class dataset(object):
    '''
        data set info readed in disk file
    '''
    def __init__(self,text,label,dtype=tf.float32):
        self._num_examples = text.shape[0]
        self._text = text
        self._label = label
        self._index_in_epoch = 0
        self._epochs_completed = 0
        
    @property
    def text(self):
        return self._text
    
    @property
    def label(self):
        return self._label
    
    def next_batch(self, batch_size):
        '''
            get next batch
        '''
        start = self._index_in_epoch
        self._index_in_epoch += batch_size
        if self._index_in_epoch > self._num_examples:
            #complete epochs
            self._epochs_completed += 1
            perm = numpy.arange(self._num_examples)
            numpy.random.shuffle(perm)
            self._text = self._text[perm]
            self._label = self._label[perm]
            
            start = 0
            self._index_in_epoch = batch_size
            assert batch_size <=self._num_examples
        
        end = self._index_in_epoch
        return self._text[start:end], self._label[start:end]
    
class datasets(object):
    '''
        read datasets from {train.txt test.txt cv.txt}
    '''
    def __init__(self):
        pass
    
    def read_train_data(self, data_dir, one_hot=False, dtype=tf.float32):
        '''
            read datasets from train.txt and train_labels.txt.
            read data separately to save mem and speed up code.
            save as numpy array such as train_texts and train_label.
        '''
        # read training set, text to train.text, label to train.label
        train_text, train_label = self.read_from_disk(data_dir, "training", one_hot)
        validation_size = int(train_text.shape[0] / 8)
        print("validation size is %d " %validation_size)
        cv_text = train_text[:validation_size]
        cv_label = train_label[:validation_size]
        
        train_text = train_text[validation_size:]
        train_label = train_label[validation_size:]
        
        self.train = dataset(train_text, train_label)
        self.cv = dataset(cv_text, cv_label)
        return
    
    def read_test_data(self, data_dir, one_hot=False, dtype=tf.float32):
        '''
            read datasets from test.txt and test_labels.txt.
            read data separately to save mem and speed up code.
            save as numpy array such as test_texts and test_lable.
        '''
        test_text, test_label = self.read_from_disk(data_dir, "test", one_hot)
        self.test = dataset(test_text,test_label)
        return
    
    def read_from_disk(self,data_dir, data_type, one_hot=False):
        '''
            read certain data from disk, data are been generated using data_preparation.py
        '''
        print("read %s data from disk." % data_type)
        data_path = data_dir + "/" + data_type+ ".txt"
        label_path = data_dir + "/" + data_type+ "_labels.txt"
        
        with open(data_path,'r', encoding ='UTF-8') as f1:
            with open(label_path, 'r', encoding = 'UTF-8') as f2:
                # get examples using shell
                sq1 = "type "+ data_path
                sq1 = sq1.replace('/','\\')
                _,stdout = subprocess.getstatusoutput(sq1 + " | find /v /c \"\"") # windows下用type XX | find /v /c ""统计所有行数
                text_line_num = int(stdout)
                print(text_line_num)
                sq2 = "type "+ label_path
                sq2 = sq2.replace('/','\\')                  
                _,stdout = subprocess.getstatusoutput(sq2 + " | find /v /c \"\"")
                label_line_num = int(stdout)
                print(label_line_num)
                
                assert label_line_num == text_line_num, "label num and text num must be equal"
                print("%s examples num is %d" %(data_type,text_line_num))
                
                text = numpy.zeros((text_line_num, 5000))
                text_count = 0
                for line in f1:
                    #word list from str to int
                    words = map(int, line.split())
                    l_words = list(words)
                    text[text_count,0:len(l_words)] = l_words
                    text_count += 1
                labels = numpy.zeros((label_line_num, 1), dtype=numpy.uint8)
                label_count = 0
                for line in f2:
                    label = map(int, line.split())
                    l_label = list(label)
                    labels[label_count, 0:len(l_label)] = l_label
                    label_count += 1
                labels[labels==0] = 0
                if one_hot:
                    labels = self.to_one_hot(labels, 8)
                return text, labels
    
    def to_one_hot(self, labels, class_num):
        '''
            dense labels to one_hot vectors
        '''
        label_num = labels.shape[0]
        offset = numpy.arange(label_num) * class_num
        labels_one_hot = numpy.zeros((label_num, class_num), dtype=numpy.uint8)
        labels_one_hot.flat[offset+labels.ravel()] = 1
        return labels_one_hot       
    
# d = datasets()
# d.read_from_disk("D:/Users/qimy/softWare/eclipse/workspace/voiceasr-tensorflow/training_set", "training", True)
    
if __name__ == '__main__':
    d = datasets()
    d.read_from_disk("D:/Users/qimy/softWare/eclipse/workspace/voiceasr-tensorflow/training_set", "training", True) 
    d.read_from_disk("D:/Users/qimy/softWare/eclipse/workspace/voiceasr-tensorflow/test_set", "test", True)   
    
    
    
    
    
    
    
    