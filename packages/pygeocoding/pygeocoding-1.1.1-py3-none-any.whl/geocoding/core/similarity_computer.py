# -*- coding: utf-8 -*-
"""
@ Created on 2024-07-23 14:27
---------
@summary: 
---------
@author: XiaoBai
"""
from abc import ABC, abstractmethod
from math import sqrt, fabs
from typing import List, Optional

from geocoding.core.segment.ascii_segmenter import AsciiSegmenter
from geocoding.core.segment.jieba_analyzer_segmenter import JiebaAnalyzerSegmenter
from geocoding.index.term_type import TermType
from geocoding.model.address import Address
from geocoding.similarity.document import Document
from geocoding.similarity.matched_result import MatchedResult
from geocoding.similarity.matched_term import MatchedTerm
from geocoding.similarity.term import Term


class Computer(ABC):
    @abstractmethod
    def analyze(self, address: Address) -> Document:
        """
         * 将标准地址转化成文档对象
         * 1. 对text进行分词
         * 2. 对每个部分计算 IDF
        :param address:
        :return:
        """

    @abstractmethod
    def compute(self, addr1: Address, addr2: Address) -> MatchedResult:
        """
         * 计算两个标准地址的相似度
         * 1. 将两个地址形成 Document
         * 2. 为每个Document的Term设置权重
         * 3. 计算两个分词组的余弦相似度, 值为0~1，值越大表示相似度越高，返回值为1则表示完全相同
         :param addr1:
         :param addr2:
         :return:
         """

    @abstractmethod
    def compute_project(self, addr1: Address, addr2: Address) -> MatchedResult:
        """ """


class SimilarityComputer(Computer):
    segmenter = JiebaAnalyzerSegmenter()  # text的分词, 默认 ik 分词器
    simple_segmenter = AsciiSegmenter()  # 暂时用于处理 building 的分词

    def __init__(self):
        # 中文数字字符
        self.NUMBER_CN = [
            '一', '二', '三', '四', '五', '六', '七', '八', '九', '０',
            '１', '２', '３', '４', '５', '６', '７', '８', '９',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        ]

        self.TRANSLATE_DIC = {
            '一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6',
            '七': '7', '八': '8', '九': '9', '十': True, '０': '0', '１': '1',
            '２': '2', '３': '3', '４': '4', '５': '5', '６': '6', '７': '7',
            '８': '8', '９': '9'
        }
        # 权重值常量
        self.BOOST_M = 1.0  # 正常权重
        self.BOOST_L = 2.0  # 加权高值
        self.BOOST_XL = 4.0  # 加权高值
        self.BOOST_S = 0.5  # 降权
        self.BOOST_XS = 0.25  # 降权

    def analyze(self, address: Address) -> Document:
        doc = Document()

        tokens: List[str] = []
        # 1. 对 text (地址解析后剩余文本) 进行分词
        if address.text is not None and address.text.strip():
            tokens = self.segmenter.segment(address.text)

        terms: List[Term] = []
        # 2. 生成 term
        # 2.1 town
        town = address.town or address.street
        if town:
            doc.town = Term(TermType.Town, town)
            terms.append(doc.town)

        # 2.2 village
        village = address.village
        if village and village.strip():
            doc.village = Term(TermType.Village, village)
            terms.append(doc.village)

        # 2.3 road
        road = address.road
        if road and road.strip():
            doc.road = Term(TermType.Road, road)
            terms.append(doc.road)

        # 2.4 road num
        road_num = address.roadNum
        if road_num and road_num.strip():
            road_num_term = Term(TermType.RoadNum, road_num)
            doc.road_num = road_num_term
            doc.road_num_value = self.translate_road_num(road_num)
            road_num_term.ref = doc.road
            terms.append(doc.road_num)

        # 2.5 building num
        building_num = address.buildingNum
        if building_num:
            # 转换 building串
            for building in self.translate_building(building_num):
                terms.append(Term(TermType.Building, building))

        # 3. 将分词放置到token中
        term_texts = [term.text for term in terms]
        for token in tokens:
            # 如果 terms 中不包含
            # 并且乡镇道路中不包含
            if token not in term_texts and token != town and token != village and token != road:
                terms.append(Term(TermType.Text, token))

        # 4. 设置每个 Term 的 IDF
        # 由于 TF-IDF 在计算地址相似度上意义不是特别明显
        self.put_idfs(terms)

        doc.terms = terms
        return doc

    def compute(self, addr1: Address, addr2: Address) -> MatchedResult:
        if addr1 is None or addr2 is None:
            return MatchedResult()

        # 如果两个地址不在同一个省市区, 则认为是不相同地址
        if addr1.provinceId != addr2.provinceId or addr1.cityId != addr2.cityId or addr1.districtId != addr2.districtId:
            return MatchedResult()

        # 为每个address计算词条
        doc1 = self.analyze(addr1)
        doc2 = self.analyze(addr2)

        # 计算两个document的相似度
        cp1 = self.compute_similarity(doc1, doc2)
        cp2 = self.compute_similarity(doc2, doc1)

        # 暂时获取计算结果最小的那个
        if cp1.similarity < cp2.similarity:
            return cp1
        return cp2

    def compute_project(self, addr1: Address, addr2: Address) -> MatchedResult:
        if addr1 is None or addr2 is None:
            return MatchedResult()

        if addr1.provinceId and addr2.provinceId and addr1.provinceId != addr2.provinceId:
            return MatchedResult()
        if addr1.cityId and addr2.cityId and addr1.cityId != addr2.cityId:
            return MatchedResult()

        # 为每个address计算词条
        doc1 = self.analyze(addr1)
        doc2 = self.analyze(addr2)

        # 计算两个document的相似度
        cp1 = self.compute_similarity(doc1, doc2)
        cp2 = self.compute_similarity(doc2, doc1)

        # 暂时获取计算结果最小的那个
        if cp1.similarity < cp2.similarity:
            return cp1
        return cp2

    def translate_road_num(self, road_num: str) -> int:
        if not road_num or road_num.strip() == "":
            return 0

        sb = []
        is_ten = False

        for c in road_num:
            if is_ten:
                pre = len(sb) > 0
                post = (c in self.NUMBER_CN) or c.isnumeric()
                if pre:
                    if not post:
                        sb.append('0')
                else:
                    sb.append('1' if post else "10")
                is_ten = False

            if (val := self.TRANSLATE_DIC.get(c, None)) is True:
                is_ten = True
            elif val is not None:
                sb.append(val)
            elif c.isdigit():
                sb.append(c)

        if is_ten:
            sb.append('0' if len(sb) > 0 else "10")

        if len(sb) > 0:
            return int("".join(sb))
        return 0

    @staticmethod
    def put_idfs(terms: List[Term]):
        for term in terms:
            # 计算 IDF
            key = term.text
            if key.isdigit() or key.isascii():
                term.idf = 2.0
            else:
                term.idf = 4.0  # 由于未进行语料库的统计, 默认4

    def translate_building(self, building: str) -> List[str]:
        if not building or building.strip() == "":
            return []
        return self.simple_segmenter.segment(building)

    def compute_similarity(self, doc1: Document, doc2: Document) -> MatchedResult:
        #  1. 计算Terms中 text类型词条 的匹配率
        q_text_term_count = 0  # 文档1的Text类型词条数目
        d_text_term_match_count = 0  # 与文档2的Text类型词条匹配数目

        # 匹配此处之间的词数间隔
        match_start = -1
        match_end = -1
        for term1 in doc1.terms or []:
            if term1.type != TermType.Text:
                continue
            q_text_term_count += 1
            for i, term2 in enumerate(doc2.terms or []):
                if term2.type != TermType.Text:
                    continue
                if term1.text == term2.text:
                    d_text_term_match_count += 1
                    if match_start == -1:
                        match_end = i
                        match_start = match_end
                        break
                    if i > match_end:
                        match_end = i
                    elif i < match_start:
                        match_start = i
                    break

        # 1.1 计算匹配率
        term_coord = 1.0
        if q_text_term_count > 0:
            # Math.sqrt( 匹配上的词条数 / doc1的Text词条数 ) * 0.5 + 0.5
            term_coord = sqrt(d_text_term_match_count * 1.0 / q_text_term_count) * 0.5 + 0.5
        # 1.2 计算稠密度
        term_density = 1.0
        if q_text_term_count >= 2 and d_text_term_match_count >= 2:
            # Math.sqrt( 匹配上的词条数 / doc2匹配词条之间的距离 ) * 0.5 + 0.5
            term_density = sqrt(d_text_term_match_count * 1.0 / (match_end - match_start + 1)) * 0.5 + 0.5

        # 2. 计算 TF-IDF(非标准) 和 余弦相似度的中间值
        result = MatchedResult()
        result.doc1 = doc1
        result.doc2 = doc2

        # 余弦相似度的中间值
        sum_qd = 0.0
        sum_qq = 0.0
        sum_dd = 0.0
        for qterm in doc1.terms or []:
            q_boost = self.get_boost_value(False, doc1, qterm, doc2, None)
            q_tf_idf = q_boost * qterm.idf
            # 文档2的term
            dterm = doc2.get_term(qterm.text)
            if dterm is None and TermType.RoadNum == qterm.type:
                # 从文档2中找门牌号词条
                if doc2.road_num and doc2.road and doc2.road == qterm.ref:
                    dterm = doc2.road_num
            d_boost = 0.0 if dterm is None else self.get_boost_value(True, doc1, qterm, doc2, dterm)
            coord = term_coord if dterm and TermType.Text == dterm.type else 1.0
            density = term_density if dterm and TermType.Text == dterm.type else 1.0
            d_tf_idf = (dterm.idf if dterm else qterm.idf) * d_boost * coord * density

            # 计算相似度
            if dterm:
                matched_term = MatchedTerm(dterm)
                matched_term.boost = d_boost
                matched_term.tfidf = d_tf_idf
                if TermType.Text == dterm.type:
                    matched_term.density = density
                    matched_term.coord = coord
                else:
                    matched_term.density = -1.0
                    matched_term.coord = -1.0
                result.terms.append(matched_term)

            sum_qq += q_tf_idf * q_tf_idf
            sum_qd += q_tf_idf * d_tf_idf
            sum_dd += d_tf_idf * d_tf_idf

        if sum_dd == 0.0 or sum_qq == 0.0:
            return result

        # 计算余弦相似度
        result.similarity = sum_qd / sqrt(sum_qq * sum_dd)

        return result

    def get_boost_value(self, for_doc: bool, q_doc: Document, qterm: Term, d_doc: Document, dterm: Optional[Term]):
        """
          根据不同的词条设置不同的权重
        :param for_doc: true 则计算 [d_doc] 的权重, 此时 [q_doc], [qterm], [d_doc], [dterm] 不为空
                        false 则计算 [q_doc] 的权重, 此时 [q_doc], [qterm], [d_doc] 不为空, [dterm] 为空
        :param q_doc:
        :param qterm:
        :param d_doc:
        :param dterm:
        :return:
        """
        term_type = dterm.type if for_doc else qterm.type
        # 权重值
        boost = self.BOOST_M
        # 省市区、道路出现频次高, IDF值较低, 但重要程度最高, 因此给予比较高的加权权重
        if term_type == TermType.Province or term_type == TermType.City or term_type == TermType.District:
            boost = self.BOOST_XL
        # 一般人对于城市街道范围概念不强，在地址中随意选择街道的可能性较高，因此降权处理
        elif term_type == TermType.Street:
            boost = self.BOOST_XS
        # 乡镇和村庄
        elif term_type == TermType.Town or term_type == TermType.Village:
            boost = self.BOOST_XS
            # 乡镇
            if term_type == TermType.Town:
                # 查询两个文档之间都有乡镇, 为乡镇加权。注意：存在乡镇相同、不同两种情况。
                # > 乡镇相同：查询文档和地址库文档都加权BOOST_L，提高相似度
                # > 乡镇不同：只有查询文档的词条加权BOOST_L, 地址库文档的词条因无法匹配不会进入该函数。结果是拉开相似度的差异
                if q_doc.town is not None and d_doc.town is not None:
                    boost = self.BOOST_L
            else:
                # 两个文档都有乡镇且乡镇相同，且查询文档和地址库文档都有村庄时，为村庄加权
                # 与上述乡镇类似，存在村庄相同和不同两种情况
                if q_doc.village is not None and d_doc.village is not None and q_doc.town is not None:
                    if q_doc.town == d_doc.town:  # 镇相同
                        boost = self.BOOST_XL if q_doc.village == d_doc.village else self.BOOST_L
                    elif d_doc.town is not None:
                        boost = self.BOOST_L if not for_doc else self.BOOST_S
        # 道路信息
        elif term_type == TermType.Road or term_type == TermType.RoadNum or term_type == TermType.Building:
            # 有乡镇有村庄，不再考虑道路、门牌号的加权
            if q_doc.town is None or q_doc.village is None:
                # 道路
                if term_type == TermType.Road:
                    if q_doc.road is not None and d_doc.road is not None:
                        boost = self.BOOST_L
                else:
                    # 门牌号。注意：查询文档和地址库文档的门牌号都会进入此处执行, 这一点跟Road、Town、Village不同。
                    # TODO: building 暂时和道路号的权重一致, 后期需优化单独处理
                    if (q_doc.road_num_value > 0 and d_doc.road_num_value > 0
                            and q_doc.road is not None and q_doc.road == d_doc.road):
                        if q_doc.road_num_value == d_doc.road_num_value:
                            boost = 3.0
                        else:
                            if for_doc:
                                boost = 1 / sqrt(
                                    sqrt(
                                        float(fabs(q_doc.road_num_value - d_doc.road_num_value) + 1)
                                    )
                                ) * self.BOOST_L
                            else:
                                boost = 3.0
        # elif term_type == TermType.Text:
        #     boost = self.BOOST_M

        return boost
