# -*- coding: utf-8 -*-
"""
@ Created on 2024-07-23 10:12
---------
@summary: 
---------
@author: XiaoBai
"""
import os
from typing import Union, Optional, List

from geocoding.core.address_interpreter import AddressInterpreter
from geocoding.core.address_persister import AddressPersister
from geocoding.core.region_cache import RegionCache
from geocoding.core.similarity_computer import Computer, SimilarityComputer
from geocoding.model.address import Address
from geocoding.model.region_entity import RegionEntity
from geocoding.model.region_type import RegionType
from geocoding.similarity.document import Document
from geocoding.similarity.matched_result import MatchedResult

STR_ADDR = Union[str, Address]


class Geocoding:
    def __init__(self, data_class_path='resources/core/new_dict.dat', strict: bool = False):
        """
        :param data_class_path:自定义地址文件路径
        :param strict:模式设置
        """
        dirname = os.path.dirname(os.path.abspath(__file__))
        self.persister = AddressPersister(RegionCache(os.path.join(dirname, data_class_path)))
        self.interpreter: AddressInterpreter = AddressInterpreter(self.persister, strict)
        self.computer: Computer = SimilarityComputer()

    def normalizing(self, address: str) -> Address:
        """ 地址的标准化, 将不规范的地址清洗成标准的地址格式 """
        return Address.build(self.interpreter.interpret(address))

    def analyze(self, address: STR_ADDR) -> Optional[Document]:
        """ 将地址进行切分 """
        if not address:
            return None
        address = self.normalizing(address) if isinstance(address, str) else address
        return self.computer.analyze(address)

    def similarity(self, address1: STR_ADDR, address2: STR_ADDR) -> float:
        """ 地址的相似度计算 """
        return self.similarity_with_result(address1, address2).similarity

    def similarity_with_result(self, address1: STR_ADDR, address2: STR_ADDR) -> MatchedResult:
        """ 地址相似度计算, 包含匹配的所有结果 """
        address1 = self.normalizing(address1) if isinstance(address1, str) else address1
        address2 = self.normalizing(address2) if isinstance(address2, str) else address2
        return self.computer.compute(address1, address2)

    def match_similarity(self, address1: STR_ADDR, address2: STR_ADDR) -> MatchedResult:
        """ 地址相似度计算, 包含匹配的所有结果 """
        address1 = self.normalizing(address1) if isinstance(address1, str) else address1
        address2 = self.normalizing(address2) if isinstance(address2, str) else address2
        return self.computer.compute_project(address1, address2)

    def match(self, text: str) -> List[RegionEntity]:
        """ 深度优先匹配符合[text]的地址信息 """
        terms = self.interpreter.get_term_index_builder().full_match(text) or []
        return terms

    def add_region_entry(
            self,
            Id: int,
            parentId: int,
            name: str,
            region_type: RegionType = RegionType.Undefined,
            alias: str = "",
            replace: bool = True
    ) -> "Geocoding":
        """
        * 设置自定义地址
        *
        * @param id          地址的ID
        * @param parentId    地址的父ID, 必须存在
        * @param name        地址的名称
        * @param type        地址类型, [RegionType]
        * @param alias       地址的别名
        * @param replace     是否替换旧地址, 当除了[id]之外的字段, 如果相等就替换
        """
        # self.add_region_entry(id, parentId, name, type, alias, replace)
        if not self.persister.get_region(parentId):
            raise ValueError(f"Parent Address is not exists, parentId is {parentId}")

        if not name:
            raise ValueError("name should not be blank.")
        # 构建 region 对象
        region = RegionEntity()
        region.id = Id
        region.parentId = parentId
        region.name = name
        region.alias = alias
        region.type = region_type
        # 暂时在这里初始化下级行政区划列表
        region.children = []
        # 1. Add to cache (id -> Region)
        self.persister.add_region_entity(region)
        # 2. Build term index
        index_builder = self.interpreter.get_term_index_builder()
        index_builder.index_regions([region], replace)
        return self

    def save(self, path: str):
        self.persister.save(path)

    @staticmethod
    def check_pca_data_is_same(A: Address, B: Address):
        return A.cityId == B.cityId and A.districtId == B.districtId

    similarityWithResult = similarity_with_result
    addRegionEntry = add_region_entry
