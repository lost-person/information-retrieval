import math
import json
import operator
from collections import Counter
import pandas as pd
import numpy as np

class BM25 :
    invert_index_table = None
    N=0
    k1=0
    k3=0
    b=0
    avg_l=0
    def __init__(self,k1,k3,b,N,avg_l):
        self.b=b
        self.k1=k1
        self.k3=k3
        self.N=N
        self.avg_l=avg_l

    def build(self,file):
        f= open(file,"r",encoding="utf-8")
        data = f.read()
        self.invert_index_table = json.loads(data)

    def query(self,word_group,weight_group):
        qtf_dict = dict(Counter(word_group))
        res={}
        table = self.invert_index_table
        for i,word in enumerate(word_group):
            if word in table:
                qtf = float(qtf_dict[word])
                doc_group = table[word]
                df = float(len(doc_group))
                for item in doc_group:
                    id_tf_ld = item.split()
                    Doc_id = id_tf_ld[0]
                    tf = float(id_tf_ld[1])
                    ld = float(id_tf_ld[2])
                    score = qtf / (self.k3 + qtf) * (self.k1 + tf) / (tf + self.k1 * (1 - self.b + self.b * ld / self.avg_l)) * math.log2((self.N - df + 0.5) / (df + 0.5))
                    if Doc_id not in res:
                        res[Doc_id]=score*weight_group[i]
                    else:
                        res[Doc_id]+=score*weight_group[i]
        res = sorted(res.items(), key=operator.itemgetter(1))
        res.reverse()
        res = ["NCT0"+num[0] for num in res]
        return res

def computePrecision(query_id,top_k,k):
# if __name__ == "__main__":
    label = pd.read_csv('clinical_trials.judgments.2017.csv')
    label = label[['trec_topic_number','trec_doc_id']]
    true_doc = label[label.trec_topic_number ==(query_id+1)].trec_doc_id
    true_doc = list(true_doc)
    positive_true=0
    for i in top_k:
        if i in true_doc:
            positive_true+=1
    print(positive_true/k)

if __name__ == '__main__':
    bm_model = BM25(k1=2, k3=1, b=0.75,N = 241006,avg_l = 300)
    bm_model.build("./clinicallevel_cleaned_txt.json")
    res = bm_model.query(["Liposarcoma","CDK4","Amplification","38-year-old","male","GERD"],[5,5,5,5,5,5])
    # 查询([查询词项],[各词项权重])
    computePrecision(0,res[:10],10)
    # 计算准确率(查询id,res[:k],k)

