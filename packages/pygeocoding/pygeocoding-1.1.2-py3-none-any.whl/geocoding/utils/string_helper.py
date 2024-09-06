# -*- coding: utf-8 -*-
"""
@ Created on 2024-07-23 14:24
---------
@summary: 
---------
@author: XiaoBai
"""


def head(string: str, length: int) -> str:
    if not string or len(string.strip()) <= length:
        return string
    if length <= 0:
        return ""
    return string[:length]


def tail(string, length) -> str:
    if not string or len(string.strip()) <= length:
        return string
    if length <= 0:
        return ""
    return string[-length:]


def take(string: str, begin: int, end: int = None) -> str:
    if not string:
        return string
    if end is None:
        if begin <= 0:
            return ''
        return string[begin:]
    else:
        if begin <= 0:
            begin = 0
        if end >= len(string) - 1:
            end = len(string) - 1
        if begin > end:
            return ""
        if begin == 0 and end == len(string) - 1:
            return string
        return string[begin:end + 1]


def remove(string: str, array: list, exclude: str = '') -> str:
    if not string or not array:
        return string

    # 去除字符
    sb = []
    rm: bool = False
    for char in string:
        if char in array and char not in exclude:
            rm = True
            continue
        sb.append(char)

    return ''.join(sb) if rm else string


def remove_repeat_num(string, length):
    if not string or len(string) < length:
        return string

    sb = []
    count = 0
    i = 0
    while i < len(string):
        c: str = string[i]
        if c.isdigit():
            count += 1
            i += 1
            continue

        # 如果数字连续出现的长度小于指定长度
        if 1 <= count < length:
            sb.append(string[i - count: i])

        # 添加当前字符到结果中
        sb.append(c)
        count = 0
        i += 1

    # 处理末尾的数字连续出现
    if 1 <= count < length:
        sb.append(tail(string, count))

    return ''.join(sb)
