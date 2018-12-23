# coding = utf-8

from query import build_query
from word2vec import load_model

'''
query_path str 查询文件路径
w2v_path str 词向量路径
vocab_path str 词典文件
'''
query_path = './topic.xml'
w2v_path = './w2v.model'
vocab_path = './vocab.pkl'

'''
查询权重
disease_w int disease字段权重
gene_w int gene字段权重
demographic_w int demographic字段权重
other_w int other字段权重
'''
diease_w = 3
gene_w = 2
demographic_w = 1
other_w = 1

# 词向量模型路径


# 返回的相关词个数
k = 5

if __name__ == '__main__': 
    # 构建查询
    query_list = build_query(query_path, w2v_path, vocab_path, k)
    print(query_list)