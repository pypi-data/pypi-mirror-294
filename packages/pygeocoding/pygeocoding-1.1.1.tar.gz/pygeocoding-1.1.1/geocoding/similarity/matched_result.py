# -*- coding: utf-8 -*-
"""
@ Created on 2024-07-23 14:24
---------
@summary: 
---------
@author: XiaoBai
"""
from typing import List

from geocoding.similarity.document import Document
from geocoding.similarity.matched_term import MatchedTerm


class MatchedResult:
    def __init__(self, doc1: Document = None, doc2: Document = None,
                 terms: List[MatchedTerm] = None, similarity: float = 0.0):
        # 两个地址分析出的文档
        self.doc1: Document = doc1
        self.doc2: Document = doc2

        # 匹配的词条信息
        self.terms: List[MatchedTerm] = terms if terms is not None else []

        # 相似度值
        self.similarity: float = similarity

    def __str__(self):
        return (f"MatchedResult(\n\tdoc1={self.doc1}, \n\tdoc2={self.doc2}, "
                f"\n\tterms={self.terms}, \n\tsimilarity={self.similarity}\n)")
