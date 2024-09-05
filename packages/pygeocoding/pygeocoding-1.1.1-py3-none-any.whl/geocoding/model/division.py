# -*- coding: utf-8 -*-
"""
@ Created on 2024-07-23 14:25
---------
@summary: 
---------
@author: XiaoBai
"""
from typing import Optional
from geocoding.model.region_type import RegionType
from geocoding.model.region_entity import RegionEntity


class Division:
    def __init__(self):
        self.province: Optional[RegionEntity] = None  # 省
        self.city: Optional[RegionEntity] = None  # 市
        self.district: Optional[RegionEntity] = None  # 区
        self.street: Optional[RegionEntity] = None  # 街道
        self._town: Optional[RegionEntity] = None  # 乡镇
        self.village: Optional[RegionEntity] = None  # 村

    @property
    def town(self):
        return self._town

    @town.setter
    def town(self, town: RegionEntity):
        if not town:
            return
        if town.type == RegionType.Town:
            self._town = town
        elif town.type == RegionType.Street or town.type == RegionType.PlatformL4:
            self.street = town
        else:
            return

    def has_province(self):
        return self.province is not None

    def has_city(self):
        return self.city is not None

    def has_district(self):
        return self.district is not None

    def has_street(self):
        return self.street is not None

    def has_town(self):
        return self._town is not None

    def has_village(self):
        return self.village is not None

    def least_region(self):
        if self.has_village():
            return self.village
        if self.has_town():
            return self._town
        if self.has_street():
            return self.street
        if self.has_district():
            return self.district
        if self.has_city():
            return self.city
        return self.province
