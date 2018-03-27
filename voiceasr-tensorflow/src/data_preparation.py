'''
Created on 2018年3月7日
See https://www.leiphone.com/news/201705/4CFBFH5szAubNQiK.html

@author: qimy
该部分是预处理文本，训练/测试数据的保存目录需要满足一定规则。
本项目中，训练集的保存目录为d_dir1;测试集的保存目录为d_dir2;最终训练好的模型保存在 model_dir中。
'''

import jieba
import os
import math
import shutil

d_dir1 = r"d:\Users\qimy\Desktop\qmy\training_set"
d_dir2 = r"d:\Users\qimy\Desktop\qmy\test_set"
d_dir3 = r"d:\Users\qimy\Desktop\qmy\training.txt"
d_dir4 = r"d:\Users\qimy\Desktop\qmy\stopwords.txt"
d_dir5 = r"d:\Users\qimy\Desktop\qmy"
d_dir6 = r"d:\Users\qimy\Desktop\qmy\word_dict.txt"
d_dir7 = r"D:\Users\qimy\Desktop\qmy\training"
model_dir = "D:/Users/qimy/softWare/eclipse/workspace/voiceasr-tensorflow"

#中文分词，去除停用词，生成词典和数据
class DataProcessor():
    def __init__(self):
        print("enter data processor......")
        
    def get_unique_id(self,data_dir):     
        dir_list = data_dir.split("/")
        class_id = dir_list[2].split("_")[0]
        type_id = dir_list[2].split("_")[1]
        text_id = dir_list[3].split(".")[0]
#         print(class_id + "_" + type_id + "_" +text_id)
        return class_id + "_" + type_id + "_" +text_id
     
    # 中文分词，需要安装jieba库
    def splitwords(self,data_dir,data_type):
        if os.path.exists(data_dir+"/"+data_type+".txt"):
            os.remove(data_dir+"/"+data_type+".txt")
        
        list_dirs = os.walk(data_dir)
        for root,_,files in list_dirs:
            print("对 "+root+" 进行分词") # root即data_dir
            # 获取目录下的所有文件
            for fp in files:
                file_path = os.path.join(root,fp)
                file_path = file_path.replace('\\','/')
                print(file_path)
                file_id = self.get_unique_id(file_path)  
                # 分词
                with open(file_path,"r+",encoding='UTF-8') as f1:
                    with open(data_dir + '/' + data_type+".txt","a+",encoding='UTF-8') as f2:
                        data = f1.read()
                        seg_list = jieba.cut(data, cut_all=False)
                        f2.write(file_id + " " + " ".join(seg_list).replace("\n"," ")+"\n")
        print("%s 的数据分词结束" %data_type)
        return

    # 删除停用词
    def rmstopwords(self,file_path,word_dict):
        #read stop word dict and save in stop_dict
        stop_dict = {}
        with open(word_dict,'r+',encoding='UTF-8') as d:
            for word in d:
                stop_dict[word.strip("\n")] = 1
        
        #remove tmp file file if exists
        if os.path.exists(file_path+".tmp"):
            os.remove(file_path+".tmp")
        print("去除%s中的停用词" % file_path)
        
        #read source file and rm stop word for each line.
        with open(file_path,'r',encoding='UTF-8') as f1:
            with open(file_path+".tmp", "a+",encoding = 'UTF-8') as f2:
                for line in f1:
                    tmp_list = []
                    words = line.split()
                    idd = words[0]
                    for word in words[1:]:
                        if word not in stop_dict:
                            tmp_list.append(word)
                    words_withoutstop_stop = " ".join(tmp_list)
                    f2.write(idd + " " + words_withoutstop_stop + "\n")
                    
        # overwrite original file with file been removed stop words
        shutil.move(file_path+".tmp",file_path)
        print("%s中的停用词已经去除" % file_path) 
        return 
    def get_dict(self, file_path, save_path):
        #生成能表征各类文本的汉语词典
        class_dict = {}
        text_num = 0
        word_in_files = {}
        with open(file_path,'r',encoding = 'UTF-8') as f:
            for line in f:
                text_num += 1
                words = line.split()
                class_id = words[0].split("_")[0]
                if class_id not in class_dict:
                    class_dict[class_id] = textinfo()   
                class_dict[class_id].update(words[1:])
                
                flags={}
                for w in words[1:]:
                    if w not in word_in_files:
                        word_in_files[w] = 0
                    if w not in flags:
                        flags[w] = False
                        
                    if flags[w] is False:
                        word_in_files[w] += 1
                        flags[w] = True
        print("根据文本类别保存文本信息textinfo")
        
        if os.path.exists(save_path):
            os.remove(save_path)
            
        for k, text_info in class_dict.items():
            # 计算词频
            for w in text_info.wordmap:
                text_info.tf_idf(w, word_in_files[w], text_num)
            main_words = []
            with open(save_path,'a+',encoding='UTF-8') as f:
                main_words = text_info.get_mainwords()
                print("class %s :main words num: %d" %(k,len(main_words)))
                f.write("\n".join(main_words) + "\n")
        print("在 %s 下生成词典" %save_path)
        return
    def get_wordbag(self, file_path, data_type, word_dict):
        #生成词袋，实现向量化文本
        
        #读取word_dict.txt
        dict_list = []
        with open(word_dict,'r',encoding = 'UTF-8') as d:
            for line in d:
                dict_list.append(line.strip("\n"))
                
        if os.path.exists(file_path+".tmp"):
            os.remove(file_path+".tmp")
        if os.path.exists(data_type+"_labels.txt"):
            os.remove(data_type+"_labels.txt")
            
        class_ids = []
        with open(file_path,'r',encoding='UTF-8') as f1:
            with open(file_path+".tmp","a+",encoding='UTF-8') as f2:
                for line in f1:
                    word_vector = []
                    for i in range(0,len(dict_list)):
                        word_vector.append(0)
                    words = line.split()
                    class_id = words[0].split("_")[0]
                    class_ids.append(class_id)
                    
                    for w in words[1:]:
                        if w in dict_list:
                            word_vector[dict_list.index(w)] += 1
                            
                    f2.write(" ".join(map(str,word_vector)) + "\n")
                    
        print(len(class_ids))
        with open(data_type+"_labels.txt","a+",encoding='UTF-8') as l:
            l.write("\n".join(class_ids))
            
        shutil.move(file_path+".tmp",file_path)
        print("通过%s生成了词袋" % file_path)
        return

class textinfo():
    def __init__(self):
        self.file_num = 0
        self.wordmap = {}
        self.max_word_num = 0    
    def update(self,words):
        self.file_num += 1
        flags = {}
        for w in words:
            if w not in self.wordmap:
                self.wordmap[w] = [0, 0]
            self.wordmap[w][0] += 1 
            if self.wordmap[w][0] > self.max_word_num:
                self.max_word_num = self.wordmap[w][0]
        return
    def tf_idf(self,w,number_in_set,text_num):
        tf = 1.0 * self.wordmap[w][0] / self.max_word_num
        idf = math.log(1.0*text_num/(number_in_set+1))
        self.wordmap[w][1] = tf * idf
        return
    def get_mainwords(self,n=7):
        sorted_list = sorted(self.wordmap.items(), key=lambda d:d[1][1], reverse = True)
        words_list = []
        #print("len of sorted list is: %d" %len(sorted_list))
        assert len(sorted_list) >= n, "main words num n must >all words num in text."
        for i in range(0,n):
            #print(sorted_list[i][0])
            words_list.append(sorted_list[i][0])
        return words_list
    
a = DataProcessor()            

'''
    绝对路径
'''       
# a.splitwords(d_dir1, "training")
# a.rmstopwords(d_dir3, d_dir4)            
# a.get_dict(d_dir3,d_dir6)            
# a.get_wordbag(d_dir3, d_dir7, d_dir6)   

'''   
    相对路径(using here)
'''     
# a.splitwords("../training_set", "training")
# a.splitwords("../test_set", "test")

# a.rmstopwords("../training_set/training.txt", "../dict/stopwords.txt")
# a.rmstopwords("../test_set/test.txt", "../dict/stopwords.txt")

# a.get_dict("../training_set/training.txt","../dict/word_dict.txt")

# a.get_wordbag("../test_set/test.txt", "../test_set/test","../dict/word_dict.txt")
# a.get_wordbag("../training_set/training.txt", "../training_set/training","../dict/word_dict.txt")                 
            
    
        