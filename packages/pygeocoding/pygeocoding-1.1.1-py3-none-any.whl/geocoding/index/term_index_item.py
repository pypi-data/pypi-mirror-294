# -*- coding: utf-8 -*-
"""
@ Created on 2024-07-23 14:26
---------
@summary: 
---------
@author: XiaoBai
"""
from dataclasses import dataclass
from typing import Optional

from geocoding.index.term_type import TermType
from geocoding.model.region_entity import RegionEntity


@dataclass
class TermIndexItem:
    type: TermType
    value: Optional[RegionEntity]
