# -*- coding: utf-8 -*-
"""
@ Created on 2024-07-23 14:28
---------
@summary: 
---------
@author: XiaoBai
"""
from typing import List

from geocoding.core.segmenter import Segmenter


class AsciiSegmenter(Segmenter):

    def segment(self, text: str) -> List[str]:
        segments = []
        if not text:
            return segments

        digit_num = 0
        ansi_char_num = 0
        for idx, char in enumerate(text):
            # for char in text:
            if char.isdigit():
                if ansi_char_num > 0:
                    segments.append(text[idx - ansi_char_num: idx])  # - 1
                    ansi_char_num = 0
                digit_num += 1
                continue

            if char.isalpha():
                if digit_num > 0:
                    segments.append(text[idx - digit_num: idx])  # - 1
                    digit_num = 0
                ansi_char_num += 1
                continue

            if digit_num > 0 or ansi_char_num > 0:
                segments.append(text[idx - digit_num - ansi_char_num: idx])  # - 1
                ansi_char_num = 0
                digit_num = 0
            # segments.append(char)

        if digit_num > 0 or ansi_char_num > 0:
            segments.append(text[len(text) - digit_num - ansi_char_num])

        return segments
