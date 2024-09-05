# -*- coding: utf-8 -*-
"""
@ Created on 2024-07-23 14:26
---------
@summary: 
---------
@author: XiaoBai
"""
from enum import Enum
from typing import Optional, Dict, List

from geocoding.core.term_index_visitor import TermIndexVisitor
from geocoding.index.term_index_entry import TermIndexEntry
from geocoding.index.term_index_item import TermIndexItem
from geocoding.index.term_type import TermType
from geocoding.model.region_entity import RegionEntity
from geocoding.model.region_entity import RegionType


class TermIndexBuilder:
    def __init__(self, rootRegion: RegionEntity, ignoringRegionNames: List[str]):
        self.indexRoot = TermIndexEntry()
        self.index_regions(rootRegion.children or [])
        self.index_ignoring(ignoringRegionNames)

    def index_regions(self, regions: List[RegionEntity], replace: bool = False):
        """ 为行政区划(标准地址库建立倒排索引) """
        if not regions:
            return
        for region in regions:
            index_item = TermIndexItem(self.convert_region_type(region), region)
            for alias in region.ordered_names if region.ordered_names else []:
                self.indexRoot.build_index(alias, 0, index_item, replace)

            r_name = region.name
            auto_alias = len(r_name) <= 5 and not region.alias and (region.is_town() or r_name.endswith("街道"))
            if auto_alias and len(r_name) == 5:
                if r_name[2] in ['路', '街', '门', '镇', '村', '区']:
                    auto_alias = False

            if auto_alias:
                if region.is_town():
                    short_name = r_name[:len(r_name) - 1]
                else:
                    short_name = r_name[:len(r_name) - 2]
                # 简历索引
                if len(short_name) >= 2:
                    self.indexRoot.build_index(short_name, 0, index_item, replace)
                if r_name.endswith("街道") or r_name.endswith("镇"):
                    self.indexRoot.build_index(short_name + "乡", 0, index_item, replace)
                if r_name.endswith("街道") or r_name.endswith("乡"):
                    self.indexRoot.build_index(short_name + "镇", 0, index_item, replace)

            if region.children:
                self.index_regions(region.children)

    def index_ignoring(self, ignoringRegionNames: List[str], replace: bool = False):
        if not ignoringRegionNames:
            return
        for ignore in ignoringRegionNames:
            self.indexRoot.build_index(ignore, 0, TermIndexItem(TermType.Ignore, None), replace)

    @staticmethod
    def convert_region_type(region) -> TermType:
        if region.type == RegionType.Country:
            return TermType.Country
        elif region.type == RegionType.Province or region.type == RegionType.ProvinceLevelCity1:
            return TermType.Province
        elif region.type == RegionType.City or region.type == RegionType.ProvinceLevelCity2:
            return TermType.City
        elif region.type == RegionType.District or region.type == RegionType.CityLevelDistrict:
            return TermType.District
        elif region.type == RegionType.PlatformL4:
            return TermType.Street
        elif region.type == RegionType.Town:
            return TermType.Town
        elif region.type == RegionType.Village:
            return TermType.Village
        elif region.type == RegionType.Street:
            if region.is_town():
                return TermType.Town
            else:
                return TermType.Street
        else:
            return TermType.Undefined

    def deep_most_query(self, text: str, visitor: TermIndexVisitor):
        """ 深度优先匹配词条 """
        if not text:
            return
        # 判断是否有中国开头
        p = 0
        if text.startswith("中国") or text.startswith("天朝"):
            p += 2
        self.deep_most_query_recursive(text, p, visitor)

    def deep_most_query_recursive(self, text: str, pos: int, visitor: TermIndexVisitor):
        if not text:
            return
        visitor.start_round()
        self.deep_first_query_round(text, pos, self.indexRoot.children or {}, visitor)
        visitor.end_round()

    def deep_first_query_round(
            self, text: str, pos: int, entries: Dict[str, TermIndexEntry], visitor: TermIndexVisitor):
        if pos > len(text) - 1:
            return

        entry = entries.get(text[pos])
        if entry is None:
            return

        if entry.children and pos + 1 <= len(text) - 1:
            self.deep_first_query_round(text, pos + 1, entry.children or {}, visitor)

        if entry.has_item():
            if visitor.visit(entry, text, pos):
                p = visitor.position()
                if p + 1 <= len(text) - 1:
                    self.deep_most_query_recursive(text, p + 1, visitor)

                visitor.end_visit(entry, text, p)

    def full_match(self, text: Optional[str]) -> Optional[List[TermIndexItem]]:
        if not text:
            return None

        return self.full_match_recursive(text, 0, self.indexRoot.children)

    def full_match_recursive(
            self, text: str, pos: int, entries: Dict[str, TermIndexEntry]
    ) -> Optional[List[TermIndexItem]]:
        if entries is None:
            return None

        c = text[pos]
        entry = entries.get(c)
        if entry is None:
            return None

        if pos == len(text) - 1:
            return entry.items

        return self.full_match_recursive(text, pos + 1, entry.children)
