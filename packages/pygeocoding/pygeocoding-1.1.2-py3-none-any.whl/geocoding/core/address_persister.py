# -*- coding: utf-8 -*-
"""
@ Created on 2024-07-23 14:27
---------
@summary: 
---------
@author: XiaoBai
"""
from geocoding.core.region_cache import RegionCache
from geocoding.model.region_entity import RegionEntity


class AddressPersister:

    def __init__(self, region_cache):
        # 行政规划准地址库
        self.regionCache: RegionCache = region_cache

    # 获取行政规划地址树状结构关系
    def get_root_region(self) -> RegionEntity:
        return self.regionCache.get()

    def get_region(self, id: int) -> RegionEntity:
        # 根据id获取
        return self.regionCache.get_cache()[id]

    def add_region_entity(self, entity: RegionEntity):
        """ 新增一个region信息 """
        self.regionCache.add_region_entity(entity)

    def save(self, path: str):
        """ 保存一个新的dat文件 """
        self.regionCache.save(path)
