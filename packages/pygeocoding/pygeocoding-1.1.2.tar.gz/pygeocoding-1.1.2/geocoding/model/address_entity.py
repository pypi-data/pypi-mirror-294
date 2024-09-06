# -*- coding: utf-8 -*-
"""
@ Created on 2024-07-23 14:25
---------
@summary: 
---------
@author: XiaoBai
"""
from geocoding.model.division import Division


class AddressEntity(Division):
    def __init__(self, address=None):
        super().__init__()
        self._text = None
        self._road = None
        self._road_num = None
        self._building_num = None
        self.hash = None
        self.address = address
        self.text = address

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        if value is None:
            self._text = ""
        else:
            self._text = value.strip()

    @property
    def road(self):
        return self._road

    @road.setter
    def road(self, value):
        if value is None:
            self._road = ""
        else:
            self._road = value.strip()

    @property
    def road_num(self):
        return self._road_num

    @road_num.setter
    def road_num(self, value):
        if value is None:
            self._road_num = ""
        else:
            self._road_num = value.strip()

    @property
    def building_num(self):
        return self._building_num

    @building_num.setter
    def building_num(self, value):
        if value is None:
            self._building_num = ""
        else:
            self._building_num = value.strip()
