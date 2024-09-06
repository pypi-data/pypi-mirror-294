# -*- coding: utf-8 -*-
"""
@ Created on 2024-07-23 14:27
---------
@summary: 
---------
@author: XiaoBai
"""
import re
from abc import ABC, abstractmethod
from typing import Optional

from geocoding.core.address_persister import AddressPersister
from geocoding.core.term_index_visitor import TermIndexVisitor, RegionInterpreterVisitor
from geocoding.index.term_index_builder import TermIndexBuilder
from geocoding.index.term_type import TermType
from geocoding.model.address_entity import AddressEntity
from geocoding.model.region_entity import RegionEntity
from geocoding.utils import string_helper


class AddressInterpreterABC(ABC):
    @abstractmethod
    def interpret(self, address: str) -> AddressEntity:
        # 将`脏`地址进行标准化处理, 解析成 [AddressEntity]
        pass

    @abstractmethod
    def get_term_index_builder(self) -> TermIndexBuilder:
        # 获取 [TermIndexBuilder]
        pass


class AddressInterpreter(AddressInterpreterABC):

    def __init__(self, persister: AddressPersister, strict: bool):
        self.persister = persister
        self.strict = strict
        self.ignoring_region_names = [
            # JD, Tmall
            "其它区", "其他地区", "其它地区", "全境", "城区", "城区以内", "城区以外", "郊区", "县城内", "内环以内",
            "开发区", "经济开发区", "经济技术开发区",
            # ehaier (from TMall or HP)
            "省直辖", "省直辖市县",
            # Others
            "地区", "市区"
        ]
        # Initialize index builder
        self.index_builder = TermIndexBuilder(persister.get_root_region(), self.ignoring_region_names)

        # 特殊字符1
        self.specialChars1 = list("　 \r\n\t,，。·.．;；:：、！@$%*^`~=+&'\"|_-\\/")

        # 包裹的特殊字符2
        self.specialChars2 = list("{}【】〈〉<>[]「」“”（）()")

        # 匹配没有路号的情况
        # xx路xx号楼
        # xx路xx - xx
        self.P_BUILDING_NUM0 = re.compile(
            # "((路|街|巷)[0-9]+号([0-9A-Z一二三四五六七八九十][\\#\\-一－/\\\\]|楼)?)?([0-9A-Z一二三四五六七八九十]+(栋|橦|幢|座|号楼|号|\\#楼?)){0,1}([一二三四五六七八九十东西南北甲乙丙0-9]+([\\#\\-一－/\\\\]|单元|门|梯|层|座))?([0-9]+(室|房)?)?"
            r"((路|街|巷)[0-9]+号([0-9A-Z一二三四五六七八九十][\\#\\-一－—/\\]|楼)?)?([0-9A-Z一二三四五六七八九十]+(栋|橦|幢|座|号楼|号|楼|\\#楼?)){0,"
            r"1}([一二三四五六七八九十东西南北甲乙丙0-9]+([\\#\\-一－—/\\]|单元|门|梯|层|座|组))?([0-9]+([\\#\\-一－—/\\]|室|房|层|楼|号|户)?)?(["
            r"0-9]+号?)?"
        )

        # *标准匹配building的模式：xx栋xx单元xxx。 < br / >
        # *注1：山东青岛市南区宁夏路118号4号楼6单元202。如果正则模式开始位置不使用(
        #     路[0 - 9] + 号)?，则第一个符合条件的匹配结果是【118
        # 号4】,
        # *按照逻辑会将匹配结果及之后的所有字符当做building，导致最终结果为：118
        # 号4号楼6单元202
        # *所以需要先匹配(路[0 - 9] + 号)?
        self.P_BUILDING_NUM1 = re.compile(
            r"((路|街|巷)[0-9]+号)?([0-9A-Z一二三四五六七八九十]+(栋|橦|幢|座|号楼|号|\\#楼?)){0,1}([一二三四五六七八九十东西南北甲乙丙0-9]+(单元|门|梯|层|座))?(["
            r"0-9]+(室|房)?)?"
        )

        # *校验building的模式。building1M能够匹配到纯数字等不符合条件的文本，使用building1V排除掉
        self.P_BUILDING_NUM_V = re.compile(
            "(栋|幢|橦|号楼|号|\\#|\\#楼|单元|室|房|门)+"
        )

        # *匹配building的模式：12 - 2 - 302，12
        # 栋3单元302
        self.P_BUILDING_NUM2 = re.compile(
            r"[A-Za-z0-9]+([#\-一－/\\]+[A-Za-z0-9]+)+"
        )

        # *匹配building的模式：10
        # 组21号，农村地址
        self.P_BUILDING_NUM3 = re.compile(
            "[0-9]+(组|通道)[A-Z0-9\\-一]+号?"
        )

        # 简单括号匹配
        self.BRACKET_PATTERN = re.compile(
            r"(?P<bracket>([\(（\{\<〈\\[【「][^\)）\}\>〉\]】」]*[\)）\}\>〉\]】」]))"
        )

        # 道路信息
        self.P_ROAD = re.compile(
            r"^(?P<road>([\u4e00-\u9fa5]{2,6}(路|街坊|街|道|大街|大道)))(?P<ex>[甲乙丙丁])?(?P<roadnum>[0-9０１２３４５６７８９一二三四五六七八九十]+("
            r"号院|号楼|号大院|号|號|巷|弄|院|区|条|\\#院|\\#))?"
        )

        # 道路中未匹配到的building信息
        self.P_ROAD_BUILDING = re.compile(
            "[0-9A-Z一二三四五六七八九十]+(栋|橦|幢|座|号楼|号|\\#楼?)"
        )

        # 村信息
        self.P_TOWN1 = re.compile(r"^((?P<z>[\u4e00-\u9fa5]{2,2}(镇|乡))(?P<c>[\u4e00-\u9fa5]{1,3}村)?)")

        self.P_TOWN2 = re.compile(
            r"^((?P<z>[\u4e00-\u9fa5]{1,3}镇)?(?P<x>[\u4e00-\u9fa5]{1,3}乡)?(?P<c>[\u4e00-\u9fa5]{1,3}村(?!(村|委|公路|("
            r"东|西|南|北)?(大街|大道|路|街))))?)"
        )

        self.P_TOWN3 = re.compile(r"^(?P<c>[\u4e00-\u9fa5]{1,3}村(?!(村|委|公路|(东|西|南|北)?(大街|大道|路|街))))?")

        self.inidTown: set = {
            "新村", "外村", "大村", "后村", "东村", "南村", "北村", "西村", "上村", "下村",
            "一村", "二村", "三村", "四村", "五村", "六村", "七村", "八村", "九村", "十村", "中村",
            "街村", "头村", "店村", "桥村", "楼村", "老村", "户村", "山村", "才村", "子村", "旧村",
            "文村", "全村", "和村", "湖村", "甲村", "乙村", "丙村", "邻村", "乡村", "村二村", "中关村",
            "城乡", "县乡", "头乡", "牌乡", "茶乡", "水乡", "港乡", "巷乡", "七乡", "站乡", "西乡", "宝乡",
            "还乡", "古镇", "小镇", "街镇", "城镇", "环镇", "湾镇", "岗镇", "镇镇", "场镇", "新镇", "乡镇",
            "屯镇", "大镇", "南镇", "店镇", "铺镇", "关镇", "口镇", "和镇", "建镇", "集镇", "庙镇", "河镇",
            "村镇"
        }

        self.invalidTownFollowings: set = {
            "政府", "大街", "大道", "社区", "小区", "小学", "中学", "医院",
            "银行", "中心", "卫生", "一小", "一中", "政局", "企局"
        }

    def interpret(self, address: str) -> Optional[AddressEntity]:
        """ 将`脏`地址进行标准化处理, 解析成 [AddressEntity] """
        if not address:
            return None
        visitor: TermIndexVisitor = RegionInterpreterVisitor(self.persister, self.strict)
        entity = AddressEntity(address)

        # 清洗下开头垃圾数据, 针对用户数据
        self.prepare(entity)
        # extractBuildingNum, 提取建筑物号
        self.extract_building_num(entity)
        # 去除特殊字符
        self.remove_special_chars(entity)
        # 提取包括的数据
        brackets = self.extract_brackets(entity)
        # 去除包括的特殊字符
        brackets = string_helper.remove(brackets, self.specialChars2)
        self.remove_brackets(entity)
        # 提取行政规划标准地址
        self.extract_region(entity, visitor)
        # 规整省市区街道等匹配的结果
        self.remove_redundancy(entity, visitor)
        # 提取道路信息
        self.extract_road(entity)
        # 提取农村信息
        # extractTownVillage(entity)

        entity.text = entity.text.replace("[0-9A-Za-z\\#]+(单元|楼|室|层|米|户|\\#)", "")
        entity.text = entity.text.replace("[一二三四五六七八九十]+(单元|楼|室|层|米|户)", "")
        if brackets:
            entity.text = entity.text + brackets
            # 如果没有道路信息, 可能存在于 Brackets 中
            if not entity.road:
                self.extract_road(entity)

        return entity

    @staticmethod
    def prepare(entity: AddressEntity):
        """ 清洗下开头垃圾数据 """
        # 去除开头的数字, 字母, 空格等
        if not entity.text:
            return

        p = re.compile(r'[ \da-zA-Z\r\n\t,，。·.．;；:：、！@$%*^`~=+&\'"|_\\\-\\/]')
        for idx, i in enumerate(entity.text):
            result = p.match(i)
            if not result:
                entity.text = entity.text[idx:]
                break

        # 将地址中的 ー－—- 等替换为-
        entity.text = re.sub(r'[ー_－—/]|(--)', '-', entity.text)

    def extract_building_num(self, entity: AddressEntity) -> bool:
        if not entity.text:
            return False

        found = False  # 是否找到的标志
        # building = None  # 最后匹配的文本

        # 使用 P_BUILDING_NUM0 进行匹配
        matcher = self.P_BUILDING_NUM0.finditer(entity.text)
        for match in matcher:
            if match.start() == match.end():
                continue
            building = string_helper.take(entity.text, match.start(), match.end() - 1)

            # 计算非空组的数量
            not_empty_groups = sum(1 for i in range(len(match.groups())) if match.group(i) is not None)

            # 如果匹配group的数量大于3，并且匹配到了building
            # 去除前面的 `xx路xx号` 前缀
            if self.P_BUILDING_NUM_V.search(building) and not_empty_groups > 3:
                pos = match.start()
                if building.startswith("路") or building.startswith("街") or building.startswith("巷"):
                    if "号楼" in building:
                        pos += building.index("路") + 1
                    else:
                        pos += building.index("号") + 1
                    building = string_helper.take(entity.text, pos, match.end() - 1)
                entity.building_num = building
                entity.text = entity.text[:pos] + entity.text[match.end():]
                found = True
                break

        if not found:
            for matcher in self.P_BUILDING_NUM1.finditer(entity.text):
                if matcher.start() == matcher.end():
                    continue
                building = string_helper.take(entity.text, matcher.start(), matcher.end() - 1)

                # 查看匹配数量, 对building进行最小匹配
                not_empty_groups = sum(1 for i in range(1, matcher.lastindex + 1) if matcher.group(i) is not None)

                if self.P_BUILDING_NUM_V.search(building) and not_empty_groups > 3:
                    pos = matcher.start()
                    if building.startswith("路") or building.startswith("街") or building.startswith("巷"):
                        pos += building.index("号") + 1
                        building = string_helper.take(entity.text, pos, matcher.end() - 1)
                    entity.building_num = building
                    entity.text = entity.text[:pos] + entity.text[matcher.end():]
                    found = True
                    break

        if not found:
            # xx - xx - xx（xx栋xx单元xxx）
            matcher = self.P_BUILDING_NUM2.search(entity.text)
            if matcher:
                entity.building_num = string_helper.take(entity.text, matcher.start(), matcher.end() - 1)
                entity.text = entity.text[:matcher.start()] + entity.text[matcher.end():]
                found = True

        if not found:
            matcher = self.P_BUILDING_NUM3.search(entity.text)
            if matcher:
                entity.building_num = string_helper.take(entity.text, matcher.start(), matcher.end() - 1)
                entity.text = entity.text[:matcher.start()] + entity.text[matcher.end():]
                found = True

        return found

    def remove_special_chars(self, entity: AddressEntity):
        if not entity.text or entity.text.strip() == "":
            return
        text: str = entity.text
        # 1. 删除特殊字符1
        text = string_helper.remove(text, self.specialChars1)

        # 2. 删除连续出现6个以上的数字
        text = string_helper.remove_repeat_num(text, 6)
        entity.text = text

        building = entity.building_num
        if not building:
            return
        building = string_helper.remove(building, self.specialChars1, "-一－_#")
        building = string_helper.remove_repeat_num(building, 6)
        entity.buildingNum = building

    def remove_brackets(self, entity: AddressEntity):
        """ 去除包裹的特殊字符 """
        if not entity.text or entity.text.strip() == "":
            return

        # 移除特殊字符
        entity.text = string_helper.remove(entity.text, self.specialChars2)

    def extract_brackets(self, entity: AddressEntity) -> str:
        """ 提取包括的数据 """

        if not entity.text or entity.text.strip() == "":
            return ""

        found = False
        brackets = []

        for matcher in self.BRACKET_PATTERN.finditer(entity.text):
            bracket = matcher.group("bracket")
            if len(bracket) <= 2:  # 如果没有文字
                continue

            brackets.append(string_helper.take(bracket, 1, len(bracket) - 2))
            found = True

        if found:
            result = "".join(brackets)
            entity.text = self.BRACKET_PATTERN.sub("", entity.text)
            return result

        return ""

    def extract_region(self, entity: AddressEntity, visitor: TermIndexVisitor) -> bool:
        """ 提取标准4级地址 """
        if not entity.text:
            return False

        visitor.reset()
        self.index_builder.deep_most_query(entity.text, visitor)
        entity.province = visitor.devision().province
        entity.city = visitor.devision().city
        entity.district = visitor.devision().district
        entity.street = visitor.devision().street
        entity.town = visitor.devision().town
        entity.village = visitor.devision().village
        entity.text = entity.text[visitor.end_position() + 1:]

        return visitor.has_result()

    def remove_redundancy(self, entity: AddressEntity, visitor: TermIndexVisitor) -> bool:
        if not entity.text or not entity.has_province() or not entity.has_city():
            return False

        removed = False
        end_idx = len(entity.text) - 2
        i = 0
        while i < end_idx:
            visitor.reset()
            self.index_builder.deep_most_query_recursive(entity.text, i, visitor)
            if visitor.match_count() < 2 or visitor.full_match_count() < 1:
                # 没有匹配上，或者匹配上的行政区域个数少于2个认当做无效匹配
                i += 1
                continue

            # 匹配上的省份、地级市不正确
            if entity.province != visitor.devision().province or entity.city != visitor.devision().city:
                i += 1
                continue

            # 正确匹配，进行回馈
            devision = visitor.devision()
            if (not entity.has_district() and devision.has_district()
                    and devision.district.parentId == entity.city.id):
                entity.district = devision.district

            # 修复街道信息
            if (entity.has_district() and not entity.has_street()
                    and devision.has_street()
                    and devision.street.parentId == entity.district.id):
                entity.street = devision.street

            # 修复乡镇信息
            if (entity.has_district() and not entity.has_town()
                    and devision.has_town() and devision.town.parentId == entity.district.id):
                entity.town = devision.town
            elif (entity.has_district() and entity.has_town() and entity.town == entity.street
                  and devision.has_town()
                  and devision.town != devision.street
                  and devision.town.parentId == entity.district.id):
                entity.town = devision.town

            if (entity.has_district() and not entity.has_village() and devision.has_village()
                    and devision.village.parentId == entity.district.id):
                entity.village = devision.village

            entity.text = entity.text[visitor.end_position() + 1:]
            end_idx = len(entity.text)
            i = 0
            removed = True

        return removed

    def extract_road(self, entity: AddressEntity) -> bool:
        """ 提取道路信息 """
        if not entity.text:
            return False
        # 如果已经提取过了
        if entity.road:
            return True
        matcher = self.P_ROAD.search(entity.text)
        if matcher:
            road = matcher.group("road")
            ex = matcher.group("ex")
            road_num = matcher.group("roadnum")
            road_num = (ex or "") + ("" if (road_num is None) else road_num)

            left_text = entity.text[len(road) + len(road_num):]
            if left_text.startswith("小区"):
                return False
            entity.road = self.fix_road(road)

            # 仅包含【甲乙丙丁】单个汉字，不能作为门牌号
            if len(road_num) == 1:
                entity.text = road_num + left_text
            else:
                entity.road_num = road_num
                entity.text = left_text

            # 修复road中存在building的问题
            if not entity.building_num:
                self.fix_road_building(entity)

            return True
        return False

    @staticmethod
    def fix_road(road: str) -> str:
        if not road or len(road) % 2 == 1:
            return road
        first = road[0: len(road) // 2]
        second = road[len(road) // 2]
        if first == second:
            return first
        return road

    def fix_road_building(self, entity: AddressEntity) -> bool:
        if not entity.text:
            return False

        matcher = self.P_ROAD_BUILDING.search(entity.text)
        if matcher and matcher.start() == 0:
            entity.building_num = string_helper.take(entity.text, matcher.start(), matcher.end() - 1)
            entity.text = entity.text[:matcher.start()] + entity.text[matcher.end():]
            return True

        return False

    def extract_town_village(
            self,
            addr: AddressEntity,
            pattern: re.Pattern,
            gz: Optional[str],
            gx: Optional[str],
            gc: Optional[str]
    ) -> int:
        """

        :param addr:
        :param pattern:
        :param gz:
        :param gx:
        :param gc:
        :return:  1: 执行了匹配操作，匹配成功
                 -1: 执行了匹配操作，未匹配上
                  0: 未执行匹配操作
        """
        if not addr.text or not addr.has_district():
            return 0

        result = -1
        matcher = pattern.search(addr.text)
        if matcher:
            text = addr.text
            c: str = None if gc is None else matcher.group("c")
            ic = -1 if gx is None else matcher.end("c")

            if gz is not None:
                z = matcher.group(gz)
                iz = matcher.end(gz)
                if z:
                    if len(z) == 2 and text.startswith("村", len(z)):
                        c = z + "村"
                        ic = iz + 1
                    elif self.is_acceptable_town_following_chars(z, text, len(z)):
                        if self.accept_town(z, addr.district) >= 0:
                            addr.text = text[iz:]
                            result = 1

            if gx is not None:
                x = matcher.group(gx)
                ix = matcher.end(gx)
                if x:
                    if len(x) == 2 and text.startswith("村", len(x)):
                        c = x + "村"
                        ic = ix + 1
                    elif self.is_acceptable_town_following_chars(x, text, len(x)):
                        if self.accept_town(x, addr.district) >= 0:
                            addr.text = text[ix:]
                            result = 1

            if c:
                if c.endswith("农村"):
                    return result
                left_str: str = text[ic:]
                if c.endswith("村村"):
                    c = c[:len(c) - 1]
                    left_str = "村" + left_str
                if left_str.endswith("委") or left_str.startswith("民委员"):
                    left_str = "村" + left_str
                if len(c) >= 4 and (c[0] == '东' or c[0] == '西' or c[0] == '南' or c[0] == '北'):
                    c = string_helper.tail(c, len(c) - 1)
                if len(c) == 2 and self.is_acceptable_town_following_chars(c, left_str, 0):
                    return ic
                if self.accept_town(c, addr.district) >= 0:
                    addr.text = left_str
                    result = 1

        return result

    def is_acceptable_town_following_chars(self, matched: str, text: str, start: int) -> bool:
        if text is None or start >= len(text):
            return True

        if len(matched) == 4 and text[start] in ["区", "县", "乡", "镇", "村", "街", "路"]:
            return False

        s1 = string_helper.take(text, start, start + 1)
        s2 = string_helper.take(text, start, start + 2)
        if s1 in self.invalidTownFollowings or s2 in self.invalidTownFollowings:
            return False

        return True

    def accept_town(self, town: str, district: RegionEntity) -> int:
        """

        :param town:
        :param district:
        :return: -1: 无效的匹配;  0: 有效的匹配，无需执行添加操作;  1: 有效的匹配，已经执行添加操作
        """
        if not town or district is None:
            return -1

        # 已加入bas_region表，不再添加
        items = self.index_builder.full_match(town)
        for item in items or []:
            if item.type != TermType.Town and item.type != TermType.Street and item.type != TermType.Village:
                continue
            region = item.value
            if isinstance(region, RegionEntity) and region.parentId == district.id:
                return 0

        # 排除一些特殊情况：草滩街镇、西乡街镇等
        if len(town) == 4 and town[2] == '街':
            return -1

        return 1

    def get_term_index_builder(self) -> TermIndexBuilder:
        return self.index_builder
