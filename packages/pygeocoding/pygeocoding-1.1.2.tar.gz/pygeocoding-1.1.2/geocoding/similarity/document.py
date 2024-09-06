# -*- coding: utf-8 -*-
"""
@ Created on 2024-07-23 14:24
---------
@summary: 
---------
@author: XiaoBai
"""
from threading import Lock
from typing import List, Dict, Optional

from geocoding.similarity.term import Term


class Document:

    def __init__(self):
        # 文档所有词条, 按照文档顺序, 未去重
        self.terms: Optional[List[Term]] = None
        # Term.text -> Term
        self.termsMap: Optional[Dict[str, Term]] = None

        # 乡镇相关的词条信息
        self.town: Optional[Term] = None
        self.village: Optional[Term] = None

        # 道路信息
        self.road: Optional[Term] = None
        self.road_num: Optional[Term] = None
        self.road_num_value = 0

    """
     * 获取 Term
    """
    def get_term(self, text) -> Optional[Term]:
        if not self.terms or len(self.terms) == 0:
            return None
        if self.termsMap is None:
            # build cache
            lock = Lock()
            with lock:
                if self.termsMap is None:
                    self.termsMap = {}
                    for term in self.terms:
                        if term.text:
                            self.termsMap[term.text] = term
        return self.termsMap.get(text)

    def __str__(self):
        return (f"Document(terms={self.terms.__str__()}, town={self.town}, village={self.village},"
                f" road={self.road}, road_num={self.road_num}, road_num_value={self.road_num_value})")
