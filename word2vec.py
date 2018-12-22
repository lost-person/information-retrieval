# coding = utf-8

from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from utils import *

def word_embedding(data_path, model_path, size = 128, window = 10, min_cnt = 3):
    '''
    读取语料，训练词向量，并存储模型

    Args:
        data_path str 语料路径
        model_path str 模型存储路径
        size int 词向量温度
        window int word2vec的窗口大小
        min_cnt int 最小词频
    '''
    model = Word2Vec(LineSentence(data_path), size = size, window = window, min_count = min_cnt)
    model.save(model_path)

def load_model(model_path):
    '''
    读取模型

    Args:
        model_path str 载入模型
    '''
    model = Word2Vec.load(model_path)
    return model

if __name__ == '__main__':
    data_path = './medline.txt'
    model_path = './w2v.model'
    word_embedding(data_path, model_path)