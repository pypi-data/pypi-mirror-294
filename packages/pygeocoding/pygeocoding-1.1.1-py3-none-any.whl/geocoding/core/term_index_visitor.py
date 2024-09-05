# -*- coding: utf-8 -*-
"""
@ Created on 2024-07-23 14:28
---------
@summary: 
---------
@author: XiaoBai
"""
from typing import List, Optional

from geocoding.core.address_persister import AddressPersister
from geocoding.index.term_index_entry import TermIndexEntry
from geocoding.index.term_index_item import TermIndexItem
from geocoding.index.term_type import TermType
from geocoding.model.division import Division
from geocoding.model.region_entity import RegionEntity
from geocoding.model.region_type import RegionType


# 基于词条倒排索引搜索的访问者
class TermIndexVisitor:

    def start_round(self) -> None:
        """开始一轮词条匹配"""

    def visit(self, entry: TermIndexEntry, text: str, pos: int) -> bool:
        """
        *匹配到一个索引条目，由访问者确定是否是可接受的匹配项。
        *索引条目[entry] 下的items一定包含一个或多个索引对象
        * @ return 可以接受返回true, 否则返回false。对于可以接受的索引条目调用[endVisit]
        结束访问
        """

    def position(self) -> int:
        """ 接受某个索引项之后当前匹配的指针位置 """

    def end_visit(self, entry: TermIndexEntry, text: str, pos: int):
        """ 结束索引访问 """

    def end_round(self):
        """ 结束一轮词条匹配"""

    def has_result(self) -> bool:
        """ 是否匹配上了结果 """

    def devision(self) -> Division:
        """ 获取访问后最终匹配结果"""

    def match_count(self) -> int:
        """ """

    def full_match_count(self) -> int:
        """ """

    def end_position(self) -> int:
        """ 获取最终匹配结果的终止位置 """

    def reset(self):
        """ 状态复位 """


# 基于倒排索引搜索匹配省市区行政区划的访问者
class RegionInterpreterVisitor(TermIndexVisitor):

    def __init__(self, persister: AddressPersister, strict: bool):
        self.persister = persister  # 地址持久层对象
        self.strict = strict

        self.currentLevel = 0
        self.deepMostLevel = 0
        self.currentPos = -1
        self.deepMostPos = -1

        self.fullMatchCount = 0
        self.deepMostFullMatchCount = 0

        self.deepMostDivision = Division()
        self.curDivision = Division()
        self.stack: List[TermIndexItem] = []
        self.ambiguousChars = ['市', '县', '区', '镇', '乡']

    def start_round(self) -> None:
        self.currentLevel += 1

    def visit(self, entry: TermIndexEntry, text: str, pos: int) -> bool:
        """
        匹配到一个索引条目，由访问者确定是否是可接受的匹配项。
        :param entry: 索引条目 [entry] 下的items一定包含一个或多个索引对象
        :param text:
        :param pos:
        :return: 可以接受返回true, 否则返回false。对于可以接受的索引条目调用 [endVisit] 结束访问
        """
        # 找到最匹配的 被索引对象. 没有匹配对象，匹配不成功，返回
        acceptable_item = self.find_acceptable_item(entry, text, pos)
        if not acceptable_item:
            return False

        # acceptableItem可能为TermType.Ignore类型，此时其value并不是RegionEntity对象，因此下面region的值可能为null
        region = acceptable_item.value if isinstance(acceptable_item.value, RegionEntity) else None

        # 更新当前状态
        self.stack.append(acceptable_item)  # 匹配项压栈
        # 使用全名匹配的词条数
        if self.is_full_match(entry, region):
            self.fullMatchCount += 1

        self.currentPos = self.positioning(region, entry, text, pos)  # 当前结束的位置
        self.update_current_division_state(region, entry)  # 刷新当前已经匹配上的省市区

        return True

    def find_acceptable_item(self, entry: TermIndexEntry, text: str, pos: int) -> TermIndexItem:
        mostPriority = -1
        acceptable_item: Optional[TermIndexItem] = None
        # 每个 被索引对象循环，找出最匹配的
        for item in entry.items:
            # 仅处理省市区类型的 被索引对象，忽略其它类型的
            if not self.is_acceptable_item_type(item.type):
                continue

            # 省市区中的特殊名称
            if item.type == TermType.Ignore:
                if acceptable_item is None:
                    mostPriority = 4
                    acceptable_item = item
                continue

            region = item.value if item and isinstance(item.value, RegionEntity) else None
            # 从未匹配上任何一个省市区，则从全部被索引对象中找出一个级别最高的
            if not self.curDivision.has_province():
                # 在为匹配上任务省市区情况下, 由于 `xx路` 的xx是某县区/市区/省的别名, 如江苏路, 绍兴路等等, 导致错误的匹配。
                # 如 延安路118号, 错误匹配上了延安县
                if not self.is_full_match(entry, region) and pos + 1 <= len(text) - 1:
                    if (region.type == RegionType.Province
                            or region.type == RegionType.City
                            or region.type == RegionType.CityLevelDistrict
                            or region.type == RegionType.District
                            or region.type == RegionType.Street
                            or region.type == RegionType.PlatformL4
                            or region.type == RegionType.Town):  # 县区或街道
                        if text[pos + 1] in ["路", "街", "巷", "道"]:
                            continue

                if mostPriority == -1:
                    mostPriority = region.type.value
                    acceptable_item = item
                if region.type.value < mostPriority:
                    mostPriority = region.type.value
                    acceptable_item = item
                continue

            # 对于省市区全部匹配, 并且当前term属于非完全匹配的时候
            # 需要忽略掉当前term, 以免污染已经匹配的省市区
            if not self.is_full_match(entry, region) and self.has_three_division():
                if region.type == RegionType.Province:
                    if region.id != self.curDivision.province.id:
                        continue
                elif region.type == RegionType.City or region.type == RegionType.CityLevelDistrict:
                    if region.id != self.curDivision.city.id:
                        continue
                elif region.type == RegionType.District:
                    if region.id != self.curDivision.district.id:
                        continue

            # 已经匹配上部分省市区，按下面规则判断最匹配项
            # 高优先级的排除情况
            if not self.is_full_match(entry, region) and pos + 1 <= len(text) - 1:  # 使用别名匹配，并且后面还有一个字符
                # 1. 湖南益阳沅江市万子湖乡万子湖村
                #   错误匹配方式：提取省市区时，将【万子湖村】中的字符【万子湖】匹配成【万子湖乡】，剩下一个【村】。
                # 2. 广东广州白云区均和街新市镇
                #   白云区下面有均和街道，街道、乡镇使用别名匹配时，后续字符不能是某些行政区域和道路关键字符
                if (region.type == RegionType.Province
                        or region.type == RegionType.City
                        or region.type == RegionType.CityLevelDistrict
                        or region.type == RegionType.District
                        or region.type == RegionType.Street
                        or region.type == RegionType.Town):  # 县区或街道
                    if text[pos + 1] in ["区", "县", "乡", "镇", "村", "街", "路"]:
                        continue
                    elif text[pos + 1] == "大" and pos + 2 < len(text) - 1:
                        c = text[pos + 2]
                        if c == '街' or c == '道':
                            continue

            # 1. 匹配度最高的情况，正好是下一级行政区域
            if region.parentId == self.curDivision.least_region().id:
                acceptable_item = item
                break

            # 2. 中间缺一级的情况。
            if mostPriority == -1 or mostPriority > 2:
                parent = self.persister.get_region(region.parentId)
                # 2.1 缺地级市
                if (not self.curDivision.has_city()
                        and self.curDivision.has_province()
                        and region.type == RegionType.District
                        and self.curDivision.province.id == parent.parentId):
                    mostPriority = 2
                    acceptable_item = item
                    continue
                # 2.2 缺区县
                if (not self.curDivision.has_district()
                        and self.curDivision.has_city()
                        and (region.type == RegionType.Street
                             or region.type == RegionType.Town
                             or region.type == RegionType.PlatformL4
                             or region.type == RegionType.Village)
                        and self.curDivision.city.id == parent.parentId):
                    mostPriority = 2
                    acceptable_item = item
                    continue

            # 3. 地址中省市区重复出现的情况
            if mostPriority == -1 or mostPriority > 3:
                if (self.curDivision.has_province() and self.curDivision.province.id == region.id or
                        self.curDivision.has_city() and self.curDivision.city.id == region.id or
                        self.curDivision.has_district() and self.curDivision.district.id == region.id or
                        self.curDivision.has_street() and self.curDivision.street.id == region.id or
                        self.curDivision.has_town() and self.curDivision.town.id == region.id or
                        self.curDivision.has_village() and self.curDivision.village.id == region.id):
                    mostPriority = 3
                    acceptable_item = item
                    continue

            # 4. 容错
            if mostPriority == -1 or mostPriority > 4:
                # 4.1 新疆阿克苏地区阿拉尔市
                # 到目前为止，新疆下面仍然有地级市【阿克苏地区】
                # 【阿拉尔市】是县级市，以前属于地级市【阿克苏地区】，目前已变成新疆的省直辖县级行政区划
                # 即，老的行政区划关系为：新疆->阿克苏地区->阿拉尔市
                # 新的行政区划关系为：
                # 新疆->阿克苏地区
                # 新疆->阿拉尔市
                # 错误匹配方式：新疆 阿克苏地区 阿拉尔市，会导致在【阿克苏地区】下面无法匹配到【阿拉尔市】
                # 正确匹配结果：新疆 阿拉尔市
                if (region.type == RegionType.CityLevelDistrict
                        and self.curDivision.has_province() and self.curDivision.province.id == region.parentId):
                    mostPriority = 4
                    acceptable_item = item
                    continue

                # 4.2 地级市 - 区县从属关系错误，但区县对应的省份正确，则将使用区县的地级市覆盖已匹配的地级市
                # 主要是地级市的管辖范围有调整，或者由于外部系统地级市与区县对应关系有调整导致
                if (region.type == RegionType.District  # 必须是普通区县
                        and self.curDivision.has_city() and self.curDivision.has_province()
                        and self.is_full_match(entry, region)  # 使用的全名匹配
                        and self.curDivision.city.id != region.parentId):
                    city = self.persister.get_region(region.parentId)  # 区县的地级市
                    if city.parentId == self.curDivision.province.id and not self.has_three_division():
                        mostPriority = 4
                        acceptable_item = item
                        continue

            #  5. 街道、乡镇，且不符合上述情况
            if (region.type == RegionType.Street
                    or region.type == RegionType.Town
                    or region.type == RegionType.Village
                    or region.type == RegionType.PlatformL4):
                if not self.curDivision.has_district():
                    parent = self.persister.get_region(region.parentId)  # parent为区县
                    parent = self.persister.get_region(parent.parentId)  # parent为地级市
                    if self.curDivision.has_city() and self.curDivision.city.id == parent.id:
                        mostPriority = 5
                        acceptable_item = item
                        continue
                elif region.parentId == self.curDivision.district.id:
                    # 已经匹配上区县
                    mostPriority = 5
                    acceptable_item = item
                    continue

        return acceptable_item

    @staticmethod
    def is_full_match(entry: TermIndexEntry, region: RegionEntity) -> bool:
        if region is None:
            return False

        if len(entry.key) == len(region.name):
            return True

        if region.type == RegionType.Street and region.name.endswith("街道") and len(region.name) == len(entry.key) + 1:
            return True  # #xx街道，使用别名xx镇、xx乡匹配上的，认为是全名匹配
        return False

    @staticmethod
    def is_acceptable_item_type(term_type: TermType) -> bool:
        """ 索引对象是否是可接受的省市区等类型 """
        if term_type in [TermType.Province, TermType.City, TermType.District,
                         TermType.Street, TermType.Town, TermType.Village, TermType.Ignore]:
            return True
        else:
            return False

    def has_three_division(self) -> bool:
        """ 当前是否已经完全匹配了省市区了 """
        return ((self.curDivision.has_province() and self.curDivision.has_city()
                 and self.curDivision.has_district())
                and self.curDivision.city.parentId == self.curDivision.province.id
                and self.curDivision.district.parentId == self.curDivision.city.id)

    def positioning(self, accepted_region: RegionEntity, entry: TermIndexEntry, text: str, pos: int) -> int:
        if accepted_region is None:
            return pos
        # 需要调整指针的情况
        # 1. 山东泰安肥城市桃园镇桃园镇山东省泰安市肥城县桃园镇东伏村
        # 错误匹配方式：提取省市区时，将【肥城县】中的字符【肥城】匹配成【肥城市】，剩下一个【县】
        if ((accepted_region.type == RegionType.City
             or accepted_region.type == RegionType.District
             or accepted_region.type == RegionType.Street)
                and not self.is_full_match(entry, accepted_region) and pos + 1 > len(text) - 1):
            c = text[pos + 1]
            if c in self.ambiguousChars:  # 后续跟着特殊字符
                for child in accepted_region.children:
                    if child.name[0] == c:
                        return pos

                return pos + 1

            # fix: 如果已经匹配最低等级
            if self.curDivision.has_town() or self.curDivision.has_street():
                # 如果不是特殊字符的, 由于存在 `xx小区, xx苑,  xx是以镇名字命名的情况`
                if c not in self.ambiguousChars:
                    self.deepMostPos = self.currentPos  # 则不移动当前指针

        return pos

    def update_current_division_state(self, region: RegionEntity, entry: TermIndexEntry):
        """ 更新当前已匹配区域对象的状态 """
        if region is None:
            return

        # region为重复项，无需更新状态
        if (region == self.curDivision.province or region == self.curDivision.city
                or region == self.curDivision.district or region == self.curDivision.street
                or region == self.curDivision.town or region == self.curDivision.village):
            return

        # 非严格模式 || 只有一个父项
        need_update_city_and_province = not self.strict or len(entry.items) == 1
        if region.type in [RegionType.Province, RegionType.ProvinceLevelCity1]:
            self.curDivision.province = region
            self.curDivision.city = None
        elif region.type in [RegionType.City, RegionType.ProvinceLevelCity2]:
            self.curDivision.city = region
            if not self.curDivision.has_province():
                self.curDivision.province = self.persister.get_region(region.parentId)
        elif region.type == RegionType.CityLevelDistrict:
            self.curDivision.city = region
            self.curDivision.district = region
            if not self.curDivision.has_province():
                self.curDivision.province = self.persister.get_region(region.parentId)
        elif region.type == RegionType.District:
            self.curDivision.district = region
            # 成功匹配了区县，则强制更新地级市
            self.curDivision.city = self.persister.get_region(self.curDivision.district.parentId)
            if not self.curDivision.has_province():
                self.curDivision.province = self.persister.get_region(self.curDivision.city.parentId)
        elif region.type in [RegionType.Street, RegionType.PlatformL4]:
            if not self.curDivision.has_street():
                self.curDivision.street = region
            if not self.curDivision.has_district():
                self.curDivision.district = self.persister.get_region(region.parentId)
            if need_update_city_and_province:
                self.update_city_and_province(self.curDivision.district)
        elif region.type == RegionType.Town:
            if not self.curDivision.has_town():
                self.curDivision.town = region
            if not self.curDivision.has_district():
                self.curDivision.district = self.persister.get_region(region.parentId)
            if need_update_city_and_province:
                self.update_city_and_province(self.curDivision.district)
        elif region.type == RegionType.Village:
            if not self.curDivision.has_village():
                self.curDivision.village = region
            if not self.curDivision.has_district():
                self.curDivision.district = self.persister.get_region(region.parentId)
            if need_update_city_and_province:
                self.update_city_and_province(self.curDivision.district)

    def update_city_and_province(self, distinct: RegionEntity):
        if distinct is None:
            return

        if not self.curDivision.has_city():
            self.curDivision.city = city = self.persister.get_region(distinct.parentId)
            if city:
                if not self.curDivision.has_province():
                    self.curDivision.province = self.persister.get_region(city.parentId)

    def position(self) -> int:
        """ 接受某个索引项之后当前匹配的指针位置 """
        return self.currentPos

    def end_visit(self, entry: TermIndexEntry, text: str, pos: int):
        self.check_deep_most()

        index_term = self.stack.pop()  # 当前访问的索引对象出栈
        self.currentPos = pos - len(entry.key)  # 恢复当前位置指针
        region = index_term.value if isinstance(index_term.value, RegionEntity) else None

        if self.is_full_match(entry, region):
            self.fullMatchCount += 1  # 更新全名匹配的数量

        if index_term.type == TermType.Ignore:
            return  # 如果是忽略项，无需更新当前已匹配的省市区状态

        # 扫描 stack，找出街道 street、乡镇 town、村庄 village，以及省市区中级别最低的一个 least
        least: Optional[RegionEntity] = None
        street: Optional[RegionEntity] = None
        town: Optional[RegionEntity] = None
        village: Optional[RegionEntity] = None

        for item in self.stack:
            if item.type == TermType.Ignore:
                break
            r = item.value
            if isinstance(r, RegionEntity):
                if r.type in [RegionType.Street, RegionType.PlatformL4]:
                    street = r
                    break
                elif r.type == RegionType.Town:
                    town = r
                    break
                elif r.type == RegionType.Village:
                    village = r
                    break
                if least is None:
                    least = r
                    break

        if street is None:
            self.curDivision.street = None  # 剩余匹配项中没有街道了
        if town is None:
            self.curDivision.town = None  # 剩余匹配项中没有乡镇了
        if village is None:
            self.curDivision.village = None  # 剩余匹配项中没有村庄了

        # 只有街道、乡镇、村庄都没有时，才开始清空省市区
        if self.curDivision.has_street() or self.curDivision.has_town() or self.curDivision.has_village():
            return

        if least is not None:
            if least.type in [RegionType.Province, RegionType.ProvinceLevelCity1]:
                self.curDivision.city = None
                self.curDivision.district = None
                return
            elif least.type in [RegionType.City, RegionType.ProvinceLevelCity2]:
                self.curDivision.district = None
                return
            else:
                return

        # least 为 None，说明 stack 中什么都不剩了
        self.curDivision.province = None
        self.curDivision.city = None
        self.curDivision.district = None

    def end_round(self):
        """ 结束一轮词条匹配 """
        self.check_deep_most()
        self.currentLevel -= 1

    def check_deep_most(self):
        if len(self.stack) > self.deepMostLevel:
            self.deepMostLevel = len(self.stack)
            self.deepMostPos = self.currentPos
            self.deepMostFullMatchCount = self.fullMatchCount
            self.deepMostDivision.province = self.curDivision.province
            self.deepMostDivision.city = self.curDivision.city
            self.deepMostDivision.district = self.curDivision.district
            self.deepMostDivision.street = self.curDivision.street
            self.deepMostDivision.town = self.curDivision.town
            self.deepMostDivision.village = self.curDivision.village

    def has_result(self) -> bool:
        """ 是否匹配上了结果 """
        return self.deepMostPos > 0 and self.deepMostDivision.has_district()

    def devision(self) -> Division:
        """ 获取访问后的对象 """
        return self.deepMostDivision

    def match_count(self) -> int:
        return self.deepMostLevel

    def full_match_count(self) -> int:
        return self.deepMostFullMatchCount

    def end_position(self) -> int:
        """ 获取最终匹配结果的终止位置 """
        return self.deepMostPos

    def reset(self):
        """ 状态复位 """
        self.currentLevel = 0
        self.deepMostLevel = 0
        self.currentPos = -1
        self.deepMostPos = -1
        self.fullMatchCount = 0
        self.deepMostFullMatchCount = 0
        # self.deepMostDivision.province = None
        # self.deepMostDivision.city = None
        # self.deepMostDivision.district = None
        # self.deepMostDivision.street = None
        # self.deepMostDivision.town = None
        # self.deepMostDivision.village = None
        # self.curDivision.province = None
        # self.curDivision.city = None
        # self.curDivision.district = None
        # self.curDivision.street = None
        # self.curDivision.town = None
        # self.curDivision.village = None
        self.deepMostDivision = Division()
        self.curDivision = Division()
