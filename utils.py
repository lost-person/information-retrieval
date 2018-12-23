# coding = utf-8

import xml.etree.ElementTree as et
import pickle

qurey_dict = {'disease' : [], 'gene' : [], 'demographic' : [], 'other' : []}
keys = qurey_dict.keys()

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

def pickle_load(data_path):
    '''
    pickle载入数据

    Args:
        data_path str 数据路径
    Returns:
        cont dict 读取内容
    '''
    with open(data_path, 'rb') as f:
        cont = pickle.load(f)
    return cont

def pickle_dump(data_path, data):
    '''
    pickle存储数据
    '''
    with open(data_path, 'wb') as f:
        pickle.dump(data, f)

def traverseXML(element):
    '''
    递归遍历xml文件

    Args:
        element xml中的结点
    '''
    if len(element) > 0:
        for child in element:
            if child.tag in keys:
                qurey_dict[child.tag].append(child.text)
                continue
            traverseXML(child)

def xml_parse(data_path):
    '''
    xml文件解析

    Args:
        data_path str xml文件路径
    Returns:
        qurey_dict dict 查询字典
    '''
    tree = et.parse(data_path)
    root = tree.getroot()
    traverseXML(root)
    return qurey_dict