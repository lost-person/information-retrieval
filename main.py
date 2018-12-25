# coding = utf-8

from query import build_query
from word2vec import load_model
from bm25 import BM25, computePrecision
import os
import time
from utils import *
import shutil

'''
query_path str 查询文件路径
w2v_path str 词向量路径
vocab_path str 词典文件
invert_table_path str 倒排表路径
doc_path str 文档路径
res_path str 结果存储路径
'''
query_path = './topic.xml'
w2v_path = '../data/w2v.model'
vocab_path = './vocab.pkl'
invert_table_path = '../data/invert_table/clinicaltrials_cleaned_txt.json'
doc_path = '../assignment/clinicaltrials_xml'
res_path = './res/'

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

# 返回的相关词个数
k1 = 5
k2 = 10

def start_query(bm, query_list, weight_list, k):
    '''
    开始查询

    Args:
        bm cls bm25模型
        query_list list 全部查询
        weight_list list 查询字段权重
        k int 返回前k个文档
    Returns:
        res list 查询结果
    '''
    res = []
    for query_tmp_list in query_list:
        res_tmp = bm.query(query_tmp_list, weight_list, k)
        res.append(res_tmp)
    return res

def get_doc(doc_id_list, res_file_path):
    '''
    根据doc_id，获取对应的文本内容（目前是摘要），并存储

    Args:
        doc_id_list list 文档id列表
        res_file_path str 文档存储路径
    '''
    query_dict = {'brief_title' : [], 'brief_summary' : [], 'detailed_description' : []}
    doc_list = os.listdir(doc_path)
    for doc_id in doc_id_list:
        doc_id += '.xml'
        query_dict = xml_parse(os.path.join(doc_path, doc_id), query_dict, query_dict.keys(), 0)
        query_dict['doc_id'] = [doc_id]
        save_data_dict(res_file_path, query_dict)

if __name__ == '__main__':
    start = time.time()
    # 构建查询
    query_list = build_query(query_path, w2v_path, vocab_path, k1)
    # bm模型
    bm = BM25()
    # 导入倒排表
    bm.build(invert_table_path)
    # 查询
    weight_list = [diease_w, gene_w, demographic_w, other_w]
    res = start_query(bm, query_list, weight_list, k2)
    # if os.path.exists(res_path):
    #     shutil.rmtree(res_path)
    # os.makedirs(res_path)
    # for i, doc_id_list in enumerate(res):
    #     get_doc(doc_id_list, os.path.join(res_path, str(i) + '.txt'))+
    # 计算p@10
    from test import eval_file
    eval_file(res)
    computePrecision(0, res[0][0][:10])
    end = time.time()
    print(end - start)