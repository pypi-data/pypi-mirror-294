# -*- coding: utf-8 -*-
"""
@ Created on 2024-07-23 14:25
---------
@summary: 
---------
@author: XiaoBai
"""
from geocoding.model.address_entity import AddressEntity


class Address:

    def __init__(
            self,
            provinceId: int = None,
            province: str = None,
            cityId: int = None,
            city: str = None,
            districtId: int = None,
            district: str = None,
            streetId: int = None,
            street: str = None,
            townId: int = None,
            town: str = None,
            villageId: int = None,
            village: str = None,
            road: str = None,
            roadNum: str = None,
            buildingNum: str = None,
            text: str = None
    ):
        self.provinceId = provinceId
        self.province = province
        self.cityId = cityId
        self.city = city
        self.districtId = districtId
        self.district = district
        self.streetId = streetId
        self.street = street
        self.townId = townId
        self.town = town
        self.villageId = villageId
        self.village = village
        self.road = road
        self.roadNum = roadNum
        self.buildingNum = buildingNum
        self.text = text

    @classmethod
    def build(cls, entity: AddressEntity):
        if entity is None or not entity.has_province():
            return None

        address = cls()
        address.provinceId = getattr(entity.province, 'id', None)
        address.province = getattr(entity.province, "name", None)
        address.cityId = getattr(entity.city, "id", None)
        address.city = getattr(entity.city, "name", None)
        address.districtId = getattr(entity.district, "id", None)
        address.district = getattr(entity.district, "name", None)
        address.streetId = getattr(entity.street, "id", None)
        address.street = getattr(entity.street, "name", None)
        address.townId = getattr(entity.town, "id", None)
        address.town = getattr(entity.town, "name", None)
        address.villageId = getattr(entity.village, "id", None)
        address.village = getattr(entity.village, "name", None)
        address.road = entity.road
        address.roadNum = entity.road_num
        address.buildingNum = entity.building_num
        address.text = entity.text
        return address

    def __str__(self):
        return f"Address(\n\tprovinceId={self.provinceId}, province={self.province}, " + \
            f"\n\tcityId={self.cityId}, city={self.city}, " + \
            f"\n\tdistrictId={self.districtId}, district={self.district}, " + \
            f"\n\tstreetId={self.streetId}, street={self.street}, " + \
            f"\n\ttownId={self.townId}, town={self.town}, " + \
            f"\n\tvillageId={self.villageId}, village={self.village}, " + \
            f"\n\troad={self.road}, " + \
            f"\n\troad_num={self.roadNum}, " + \
            f"\n\tbuilding_num={self.buildingNum}, " + \
            f"\n\ttext={self.text}\n)"

    def equals(self, other) -> bool:
        if self is other:
            return True
        if not isinstance(other, Address):
            return False

        # 定义需要比较的属性列表
        properties_to_compare = [
            'provinceId', 'province', 'cityId', 'city', 'districtId', 'district',
            'streetId', 'street', 'townId', 'town', 'villageId', 'village',
            'road', 'roadNum', 'buildingNum', 'text'
        ]

        # 使用zip()函数同时迭代两个对象的属性，并进行比较
        for prop_self, prop_other in zip(properties_to_compare, properties_to_compare):
            if getattr(self, prop_self) != getattr(other, prop_other):
                return False

        return True

    def __hash__(self) -> int:
        result = hash(self.provinceId) if self.provinceId is not None else 0
        result = 31 * result + hash(self.province) if self.province is not None else 0
        result = 31 * result + hash(self.cityId) if self.cityId is not None else 0
        result = 31 * result + hash(self.city) if self.city is not None else 0
        result = 31 * result + hash(self.districtId) if self.districtId is not None else 0
        result = 31 * result + hash(self.district) if self.district is not None else 0
        result = 31 * result + hash(self.streetId) if self.streetId is not None else 0
        result = 31 * result + hash(self.street) if self.street is not None else 0
        result = 31 * result + hash(self.townId) if self.townId is not None else 0
        result = 31 * result + hash(self.town) if self.town is not None else 0
        result = 31 * result + hash(self.villageId) if self.villageId is not None else 0
        result = 31 * result + hash(self.village) if self.village is not None else 0
        result = 31 * result + hash(self.road) if self.road is not None else 0
        result = 31 * result + hash(self.roadNum) if self.roadNum is not None else 0
        result = 31 * result + hash(self.buildingNum) if self.buildingNum is not None else 0
        result = 31 * result + hash(self.text) if self.text is not None else 0
        return result
