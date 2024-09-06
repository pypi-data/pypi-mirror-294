# -*- coding: utf-8 -*-
"""
@ Created on 2024-07-23 14:24
---------
@summary: 
---------
@author: XiaoBai
"""
from typing import Optional

from geocoding.index.term_type import TermType


class Term:

    def __init__(self, _type: TermType, text):
        self._idf = None
        self.text: Optional[str] = text
        self.type: TermType = _type
        self.ref: Optional["Term"] = None

    @property
    def idf(self) -> float:
        if self.type in [TermType.Province, TermType.City, TermType.District]:
            return 0.0
        elif self.type == TermType.Street:
            return 1.0
        else:
            return self._idf

    @idf.setter
    def idf(self, value: float):
        self._idf = value

    def __eq__(self, other):
        if not isinstance(other, Term):
            return False
        if self.text is None:
            return other.text is None
        return self.text == other.text

    def __hash__(self):
        if self.text is None:
            return 0
        return hash(self.text)

    def __str__(self):
        return f"Term({repr(self.text)})"

    def __repr__(self):
        return f"Term({repr(self.text)})"
