# -*- coding: utf-8 -*-
"""
@ Created on 2024-07-23 14:29
---------
@summary: 
---------
@author: XiaoBai
"""
import os

import jieba.posseg
import jieba.analyse

from geocoding.core.segmenter import Segmenter

dirname = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


# jieba.load_userdict(os.path.join(dirname, r"resources\dic\region.txt"))
# jieba.load_userdict(os.path.join(dirname, r"resources\dic\community.txt"))


class JiebaAnalyzerSegmenter(Segmenter):
    stopwords: list = None

    def __init__(self, path=r'resources\dic\stop.txt'):
        if not self.stopwords:
            self.set_stopwords(path)

    def segment(self, text):
        # 使用 jieba 进行分词
        segs = list(jieba.cut(text))  # 精确模式
        filtered_words = [word for word in segs if word not in self.stopwords]
        print(segs, filtered_words)
        return filtered_words

    @classmethod
    def set_stopwords(cls, path):
        if path != r'resources\dic\stop.txt':
            if not os.path.exists(path):
                raise FileExistsError(path)
        else:
            path = os.path.join(dirname, path)

        with open(path, 'r', encoding='utf8') as f:
            print(f"加载停用词: {path}")
            cls.stopwords = f.read().strip().split('\n')
