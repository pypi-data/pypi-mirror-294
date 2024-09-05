# -*- coding: utf-8 -*-
"""
@ Created on 2024-07-23 14:25
---------
@summary: 
---------
@author: XiaoBai
"""
from enum import Enum


class RegionType(Enum):
    # 未定义区域类型
    Undefined = 0
    # 国家
    Country = 10
    # 省份
    Province = 100
    # 直辖市-与省份并行的一级
    ProvinceLevelCity1 = 150
    # 直辖市-与城市并行的一级
    ProvinceLevelCity2 = 151
    # 地级市
    City = 200
    # 省直辖县级市
    CityLevelDistrict = 250
    # 县、区
    District = 300
    # 街道乡镇一级
    Street = 450
    # 特定平台的4级地址
    PlatformL4 = 460
    # 附加：乡镇
    Town = 400
    # 附加：村
    Village = 410
