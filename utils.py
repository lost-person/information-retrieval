# coding = utf-8

import pickle

def load_data_lines(data_path):
    '''
    以行的形式读取文件, utf-8格式

    Args:
        data_path str 数据路径
    Returns:
        cont list 数据
    '''
    with open(data_path, 'r', encoding = 'utf-8') as f:
        cont = f.readlines()
    return cont


def load_data_lines_v2(data_path):
    '''
    以行的形式读取文件, utf-8格式, 去除空行

    Args:
        data_path str 数据路径
    Returns:
        cont list 数据
    '''
    with open(data_path, 'r', encoding = 'utf-8') as f:
        cont = f.readlines()
        for i in range(len(cont)-1, -1, -1):
            # 删除文件中的空行
            if cont[i] == '\n' :
                cont.pop(i)
    return cont

def load_data_lines_bin(data_path):
    '''
    以行的形式读取文件, utf-8格式

    Args:
        data_path str 数据路径
    Returns:
        cont list 数据
    '''
    with open(data_path, 'rb') as f:
        cont = f.readlines()
    return cont

def save_data_lines(data_path, data):
    '''
    以行的形式存储数据, utf-8

    Args:
        data_path str 存储路径
        data list 存储数据
    '''
    with open(data_path, 'w', encoding = 'utf-8') as f:
        f.writelines(data)

def save_data_lines_bin(data_path, data):
    '''
    以行的形式存储数据, utf-8

    Args:
        data_path str 存储路径
        data list 存储数据
    '''
    with open(data_path, 'wb') as f:
        f.writelines(data)