from utils import *
from string import punctuation
import re

def preprocess(cont):
    '''
    对文档内容进行预处理，用于map函数

    Args:
        cont str 未预处理的文档内容中的一行
    Returns:
        cont str 预处理之后的文档内容中的一行
    '''
    cont = cont.strip('\n')
    cont = re.sub(r'[%s]+'%punctuation, '', cont)
    return cont

cont_list = load_data_lines('../data/medline0.txt')
cont_list = list(map(preprocess, cont_list))
print(cont_list)