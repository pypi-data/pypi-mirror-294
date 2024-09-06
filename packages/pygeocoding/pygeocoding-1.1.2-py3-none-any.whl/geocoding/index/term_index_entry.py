# -*- coding: utf-8 -*-
"""
@ Created on 2024-07-23 14:26
---------
@summary: 
---------
@author: XiaoBai
"""
from typing import Optional, List, Dict

from geocoding.index.term_index_item import TermIndexItem


class TermIndexEntry:
    def __init__(self):
        self.key: Optional[str] = None  # 条目的key
        self.items: List[TermIndexItem] = []  # 每个条目下的所有索引对象
        self.children: Dict[str, "TermIndexEntry"] = {}  # 子条目

    def add_item(self, item: TermIndexItem) -> "TermIndexEntry":
        self.items.append(item)
        return self

    def has_item(self) -> bool:
        return len(self.items) > 0

    def build_index(self, text: str, pos: int, item: TermIndexItem, replace: bool):
        """ 初始化倒排索引 """
        if not text or pos < 0 or pos >= len(text):
            return

        c = text[pos]
        entry = self.children.get(c)

        if entry is None:
            entry = TermIndexEntry()
            entry.key = text[:pos + 1]
            self.children[c] = entry

        if pos == len(text) - 1:
            if replace and item.value:
                entry.items = [i for i in entry.items if item.value != i.value]
            entry.add_item(item)
            return

        entry.build_index(text, pos + 1, item, replace)
