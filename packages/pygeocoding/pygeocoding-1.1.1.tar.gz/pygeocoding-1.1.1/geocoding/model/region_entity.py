# -*- coding: utf-8 -*-
"""
@ Created on 2024-07-23 14:25
---------
@summary: 
---------
@author: XiaoBai
"""
from typing import List, Optional

from geocoding.model.region_type import RegionType


class RegionEntity:
    def __init__(self, **kwargs):
        self.id: int = kwargs.get('id') or 0
        self.parentId: int = kwargs.get('parentId') or 0
        self.name: str = kwargs.get('name') or ""
        self.alias: str = kwargs.get('alias') or ""
        self.type: RegionType = RegionType[kwargs.get('type') or "Undefined"]
        self.zip: str = kwargs.get('zip', "") or ""
        self.children: Optional[List["RegionEntity"]] = kwargs.get('children', None)
        self._orderedNames: Optional[List[str]] = None

    @property
    def ordered_names(self):
        if self._orderedNames is not None:
            return self._orderedNames
        self._orderedNames = self.build_ordered_names()
        return self._orderedNames

    def build_ordered_names(self):
        fields = [self.name]
        if self.alias.strip() == "":
            return fields
        for item in self.alias.split(";"):
            if item.strip() != "":
                fields.append(item.strip())
        fields.sort(key=lambda x: len(x), reverse=True)
        return fields

    def is_town(self):
        if self.type == RegionType.Town:
            return True
        elif self.type == RegionType.Street:
            if self.name.strip() == "":
                return False
            return len(self.name) <= 4 and (self.name[-1] == '镇' or self.name[-1] == '乡')
        else:
            return False

    def __eq__(self, other):
        if other is None or isinstance(other, RegionEntity):
            return False
        region = other
        return self.id == region.id

    def __hash__(self):
        return hash(self.id)

    def equals_without_id(self, other):
        if other is None or isinstance(other, RegionEntity):
            return False
        other = other
        if self.parentId != other.parentId:
            return False
        if self.name != other.name:
            return False
        if self.alias != other.alias:
            return False
        if self.type != other.type:
            return False
        if self.zip != other.zip:
            return False
        return True

    def __str__(self):
        return (f"RegionEntity(id={self.id}, "
                f"parentId={self.parentId}, "
                f"name='{self.name}', "
                f"alias='{self.alias}', "
                f"type={self.type}, "
                f"children={len(self.children or [])}, "
                f"zip='{self.zip}')")
