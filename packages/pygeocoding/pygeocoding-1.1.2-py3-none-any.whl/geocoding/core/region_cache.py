# -*- coding: utf-8 -*-
"""
@ Created on 2024-07-23 14:27
---------
@summary: 
---------
@author: XiaoBai
"""
import base64
import gzip
import json
from io import BytesIO
from typing import Dict
from typing import Optional

from geocoding.model.region_entity import RegionEntity
from geocoding.model.region_type import RegionType


class RegionCache:
    def __init__(self, data_class_path: str):
        self.regions: Optional[RegionEntity] = None
        self.REGION_CACHE: Dict[int, RegionEntity] = {}

        # Load region data
        if self.regions is None:
            with open(data_class_path, 'r') as input_file:
                data = input_file.read()
                decoded_data = self.decode(data)
                self.regions: RegionEntity = json.loads(decoded_data, object_hook=lambda d: RegionEntity(**d))

        # Load cache
        self.REGION_CACHE[self.regions.id] = self.regions
        self.load_children_in_cache(self.regions)

    def load_children_in_cache(self, parent: RegionEntity):
        # 已经到最底层，结束
        if parent is None or parent.type in {RegionType.Street, RegionType.Village, RegionType.PlatformL4,
                                             RegionType.Town}:
            return

        for child in parent.children or []:
            self.REGION_CACHE[child.id] = child
            self.load_children_in_cache(child)

    def decode(self, dat: str) -> str:
        """ 解压缩数据 """
        decoded_bytes = base64.b64decode(dat)
        with gzip.GzipFile(fileobj=BytesIO(decoded_bytes)) as gzip_file:
            return gzip_file.read().decode()

    def get(self) -> RegionEntity:
        """ 加载全部区域列表，按照行政区域划分构建树状结构关系 """
        if self.regions is None:
            raise ValueError("行政规划区域数据加载失败!")
        return self.regions

    def get_cache(self) -> Dict[int, RegionEntity]:
        """ 加载区域map结构, key是区域id, 值是区域实体 """
        return self.REGION_CACHE

    def add_region_entity(self, entity: RegionEntity):
        """ 新增一个region信息 """
        self.load_children_in_cache(entity)
        self.REGION_CACHE[entity.id] = entity
        if entity.parentId in self.REGION_CACHE:
            self.REGION_CACHE[entity.parentId].children.append(entity)

    def save(self, path: str):
        region_data = json.dumps(self.regions, default=lambda o: o.__dict__, ensure_ascii=False).encode('utf-8')
        compressed_data = BytesIO()
        with gzip.GzipFile(fileobj=compressed_data, mode='wb') as gzip_file:
            gzip_file.write(region_data)

        encoded_data = base64.b64encode(compressed_data.getvalue())
        with open(path, 'wb') as output_file:
            output_file.write(encoded_data)
