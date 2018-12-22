# coding = utf-8

import os
from string import punctuation
import re
import multiprocessing
import math
from utils import *

# 文件路径
doc_path = '../data/medline_txt'
# 文档集目录数
doc_list = os.listdir(doc_path)
# 进程锁
lock = multiprocessing.Lock()

def start_load(rate = 0.025, process_num = 4):
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

# def preprocess(cont):
#     '''
#     对文档内容进行预处理，用于map函数

#     Args:
#         cont str 未预处理的文档内容中的一行
#     Returns:
#         cont str 预处理之后的文档内容中的一行
#     '''
#     cont = re.sub(r'[%s]+'%punctuation, '', cont)
#     return cont

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
        file_list = os.listdir(os.path.join(doc_path, doc_dir))
        for doc in file_list:
            # lock.acquire()
            cont_list.extend(load_data_lines_v2(os.path.join(doc_path, doc_dir, doc)))
            # lock.release()
    # 对数据进行预处理
    # cont_list = list(map(preprocess, cont_list))
    save_data_lines(os.path.join('../data', 'medline' + str(start) + '.txt'), cont_list)
    return cont_list

if __name__ == '__main__':
    # 根据文件夹数创建对应的IO进程
    print('start loading data...')
    start_load()