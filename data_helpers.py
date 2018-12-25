# coding = utf-8

import os
from string import punctuation
import re
import multiprocessing
import math
from utils import *
from tqdm import tqdm

# 文件路径
doc_path = '../data/medline_txt'
# 文档集目录数
doc_list = os.listdir(doc_path)
# 进程锁
lock = multiprocessing.Lock()

def start_load(rate = 0.5, process_num = 4):
    '''
    根据文档集数创建相应个数的IO线程，指定它们读取文档集的范围

    Args:
        rate int 读取文档集文件夹比例（太大了，读不动啊）
        process_num int 进程数
    '''
    # 待读取的文档集目录数
    doc_size = int(len(doc_list) * rate)
    # 每个进程读取的文档集目录数
    range_num = math.ceil(doc_size / process_num)
    pool = multiprocessing.Pool(processes = process_num)
    result_list = []
    cont_list = []
    i = 0
    print('create ' + str(process_num) + ' processes')
    print('start loading data...')
    while True:
        start = i * range_num
        if start > doc_size:
            break
        end = min((i + 1) * range_num, doc_size) 
        result_list.append(pool.apply_async(load_doc, (start, end)))
        i += 1
    pool.close()
    pool.join()
    for res in result_list:
        cont_list.extend(res.get())
    save_data_lines(os.path.join('../data', 'medline.txt'), cont_list)
    print('data loaded!')

def preprocess(cont):
    '''
    对文档内容进行预处理，用于map函数

    Args:
        cont str 未预处理的文档内容中的一行
    Returns:
        cont str 预处理之后的文档内容中的一行
    '''
    cont = re.sub(r'[{%s}]+'%punctuation, '', cont)
    return cont

def load_doc(start, end):
    '''
    读取文档集，并进行预处理，写入文件

    Args:
        start int 起始的文档id
        end int 结束的文档id
    Returns:
        cont_list list 文档内容列表
    '''
    cont_list = []
    for i in range(start, end + 1):
        doc_dir = doc_list[i]
        print('reading... ' + doc_dir)
        file_list = os.listdir(os.path.join(doc_path, doc_dir))
        for doc in file_list:
            cont_list.extend(load_data_lines_v2(os.path.join(doc_path, doc_dir, doc)))
    # 对数据进行预处理
    cont_list = list(map(preprocess, cont_list))
    save_data_lines(os.path.join('../data', 'medline' + str(start) + '.txt'), cont_list)
    return cont_list

def data_clean(sent_list):
    '''
    对文本的清理

    Args:
        sent_list list 列表形式的文本内容
    Returns:
        sent_list list 处理好的文本内容
    '''
    for i in range(len(sent_list)-1, -1, -1):
        sent_list[i] = sent_list[i].strip(' ')
        # 删除文件中的空行
        if sent_list[i] == '\n' :
            sent_list.pop(i)
    return sent_list

def process_doc(src_path, des_path):
    '''
    文件清理，并写入指定文件
    
    Args:
        src_path str 原路径
        des_path str 目标路径
    '''
    # cont_list = []
    # doc_list = os.listdir(src_path)
    # for doc in doc_list:
    #     print('reading doc:' + doc)
    #     cont_list.extend(load_data_lines(os.path.join(src_path, doc)))
    # save_data_lines(os.path.join(des_path, 'corpus.txt'), cont_list)
    cont_list = load_data_lines(src_path)
    for i in tqdm(range(len(cont_list))):
        cont_tmp_list = cont_list[i].split(' ')
        cont_tmp_list = clean_data(cont_tmp_list)
        cont_list[i] = ''
        for cont in cont_tmp_list:
            cont_list[i] += cont + ' '
        cont_list[i] = cont_list[i].strip(' ')
    save_data_lines(des_path, cont_list)
    
if __name__ == '__main__':
    # 根据文件夹数创建对应的IO进程
    # start_load(process_num = 4)
    process_doc('../data/test/corpus.txt', '../data/test/corpus_stem.txt')