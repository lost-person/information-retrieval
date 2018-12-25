# coding = utf-8

import xml.etree.ElementTree as et
import os
import pickle
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords

def load_data(data_path):
    '''
    以行的形式读取文件, utf-8格式

    Args:
        data_path str 数据路径
    Returns:
        cont list 数据
    '''
    with open(data_path, 'r', encoding = 'utf-8') as f:
        cont = f.read()
    return cont

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

def save_data(data_path, data):
    '''
    以行的形式存储数据, utf-8

    Args:
        data_path str 存储路径
        data list 存储数据
    '''
    with open(data_path, 'w', encoding = 'utf-8') as f:
        f.write(data)

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

def save_data_dict(data_path, data):
    '''
    存储字典, utf-8

    Args:
        data_path str 存储路径
        data dict 存储数据
    '''
    with open(data_path, 'a+', encoding = 'utf-8') as f:
        doc_id = data['doc_id']
        if len(data['brief_title']) == 0:
            brief_title = ''
        else:
            brief_title = data['brief_title'][0]
        if len(data['brief_summary']) == 0:
            brief_summary = ''
        else:
            brief_summary = data['brief_summary'][0]
            brief_summary_list = brief_summary.split('\n')
            brief_summary = clean(brief_summary_list)
            brief_summary = brief_summary.strip(' ')
        if len(data['detailed_description']) == 0:
            detailed_description = ''
        else:
            detailed_description = data['detailed_description'][0]
            detailed_description_list = detailed_description.split('\n')
            detailed_description = clean(detailed_description_list)
            detailed_description = detailed_description.strip(' ')
        f.write('doc_id:' + doc_id[0] + '\n' + 'brief_title:' + brief_title + '\n' + 'brief_summary:' + brief_summary 
            + '\n' +'detailed_description:' + detailed_description + '\n' + '\n')
        
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

def traverseXML(element, qurey_dict, keys):
    '''
    递归遍历xml文件

    Args:
        element xml中的结点
        keys set/list 需要获取的结点
    '''
    if len(element) > 0:
        for child in element:
            if child.tag in keys:
                if child.tag == 'brief_summary' or child.tag == 'detailed_description':
                    for son in child:
                        qurey_dict[child.tag].append(son.text)
                else:
                    qurey_dict[child.tag].append(child.text)
                continue
            traverseXML(child, qurey_dict, keys)
    return qurey_dict

def xml_parse(data_path, query_dict, keys, flag = 1):
    '''
    xml文件解析

    Args:
        data_path str xml文件路径
    Returns:
        query_dict dict 查询字典
    '''
    tree = et.parse(data_path)
    root = tree.getroot()
    traverseXML(root, query_dict, keys)
    return query_dict

def cut_file(src_path, des_path):
    '''
    剪切文件

    Args:
        src_path str 原数据路径
        des_path str 目标数据路径
    '''
    if not os.path.isdir(des_path):
        os.mkdir(des_path)
    for root, sub_dirs, files in os.walk(src_path):
        for target_file in files:
            if os.path.isfile(os.path.join(des_path, target_file)):
                os.remove(os.path.join(des_path, target_file))
            os.rename(os.path.join(root, target_file), os.path.join(des_path, target_file))

def clean_data(query_list):
    '''
    对查询进行词干还原与去停用词

    Args:
        query_list list 原始的查询
    Returns:
        query_clean_list list 词干还原和去停用词之后的查询
    '''
    # 导入词性还原与停用词
    wnl = WordNetLemmatizer()
    sw = stopwords.words('english')
    # 扩展后的查询
    query_clean_list = []
    for query in query_list:
        query = query.lower()
        query = wnl.lemmatize(query)
        if query not in sw:
            query_clean_list.append(query)
    return query_clean_list

def clean(data):
    '''
    清理数据
    Args:
        data list 待清理的数据
    Returns
        cont str 清除完毕的数据
    '''
    cont = ''
    for sent in data:
        sent = sent.strip(' ')
        cont += sent + ' '
    return cont