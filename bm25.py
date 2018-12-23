import math
import json
import operator
from collections import Counter
import pandas as pd
import numpy as np

class BM25 :
    '''
    BM25模型
    '''
    def __init__(self, k1 = 2, k3 = 8, b = 0.75, N = 241006, avg_l = 300):
        '''
        BM25模型超参数

        Args:
            b float BM25模型中的b
            k1 int BM25模型中的k1
            k3 int BM25模型中的k3
            N int 文档数
            avg_l int 平均文档长度
        '''
        self.b = b
        self.k1 = k1
        self.k3 = k3
        self.N = N
        self.avg_l = avg_l

    def build(self, file):
        '''
        导入倒排表
        '''
        with open(file,"r",encoding="utf-8") as f:
            data = f.read()
        self.invert_index_table = json.loads(data)

    def query(self, word_group, weight_group):
        '''
        根据BM25模型计算得分并排序

        Args:
            word_group list 查询词
            weight_group list 查询词的权重
        '''
        # 查询中词与词频字典
        qtf_dict = dict(Counter(word_group))
        # 结果集合
        res = {}
        # 倒排表（第0个元素：文档id，第1个元素：文档词频，第2个元素：文档长度）
        table = self.invert_index_table
        for i, word in enumerate(word_group):
            if word in table:
                # 查询中词频
                qtf = float(qtf_dict[word])
                # 文档集（id）
                doc_group = table[word]
                # 文档频率
                df = float(len(doc_group))
                for item in doc_group:
                    id_tf_ld = item.split()
                    Doc_id = id_tf_ld[0]
                    tf = float(id_tf_ld[1])
                    # 文档长度
                    ld = float(id_tf_ld[2])
                    score = qtf / (self.k3 + qtf) * (self.k1 + tf) / (tf + self.k1 * (1 - self.b + self.b * ld / self.avg_l)) * math.log2((self.N - df + 0.5) / (df + 0.5))
                    if Doc_id not in res:
                        res[Doc_id] = score*weight_group[i]
                    else:
                        res[Doc_id] += score*weight_group[i]
        # 排序
        res = sorted(res.items(), key=operator.itemgetter(1))
        res.reverse()
        res = ["NCT0" + num[0] for num in res]
        return res

def computePrecision(query_id, top_k, k = 10):
    '''
    计算p@10

    Args:
        query_id int 查询id
        top_k list 前k个文档的id
        k int k的值
    '''
    label = pd.read_csv('clinical_trials.judgments.2017.csv')
    label = label[['trec_topic_number','trec_doc_id']]
    true_doc = label[label.trec_topic_number ==(query_id+1)].trec_doc_id
    true_doc = list(true_doc)
    positive_true = 0
    for i in top_k:
        if i in true_doc:
            positive_true+=1
    print(positive_true / k)

if __name__ == '__main__':
    bm_model = BM25(k1 = 2, k3 = 1, b = 0.75, N = 241006, avg_l = 300)
    bm_model.build("./clinicallevel_cleaned_txt.json")
    res = bm_model.query(["Liposarcoma","CDK4","Amplification","38-year-old","male","GERD"],[5,5,5,5,5,5])
    # 查询([查询词项],[各词项权重])
    computePrecision(0, res[:10], 10)
    # 计算准确率(查询id,res[:k],k)
