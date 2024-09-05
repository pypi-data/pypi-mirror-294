# -*- coding: utf-8 -*-
"""
@ Created on 2024-07-23 14:24
---------
@summary: 
---------
@author: XiaoBai
"""
from geocoding.similarity.term import Term


class MatchedTerm:

    def __init__(self, term: Term):
        # 匹配的词条
        self.term: Term = term

        # 匹配率
        self.coord: float = 0.0

        # 稠密度
        self.density: float = 0.0

        # 权重
        self.boost: float = 0.0

        # 特征值 TF-IDF
        self.tfidf: float = 0.0
