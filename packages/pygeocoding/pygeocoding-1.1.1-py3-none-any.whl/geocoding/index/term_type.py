# -*- coding: utf-8 -*-
"""
@ Created on 2024-07-23 14:26
---------
@summary: 
---------
@author: XiaoBai
"""
from enum import Enum


class TermType(Enum):
    Undefined = '0'
    Country = 'C'
    Province = '1'
    City = '2'
    District = '3'
    Street = '4'
    Town = 'T'
    Village = 'V'
    Road = 'R'
    RoadNum = 'N'
    Building = 'B'
    Text = 'X'
    Ignore = 'I'

    @staticmethod
    def to_enum(type_char: str):
        for term_type in TermType:
            if term_type.value == type_char:
                return term_type

        return TermType.Undefined
