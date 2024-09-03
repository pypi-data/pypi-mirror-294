# cryptography 관련 경고 메시지 억제하는 코드
import warnings
from cryptography.utils import CryptographyDeprecationWarning

warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

# 이후에 pymongo를 임포트하거나 관련 코드를 실행합니다.

from pymongo import errors, database, collection, MongoClient, ASCENDING, DESCENDING, TEXT

import copy
import math
import datetime
from typing import List, Tuple
from collections import OrderedDict
from abc import ABC, abstractmethod
from utils_hj3415 import utils
import pandas as pd


import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s.%(funcName)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.WARNING)

"""
db구조 비교 - 통일성을 위해 몽고 클래스에서 사용하는 용어를 RDBMS로 사용한다.
RDBMS :     database    / tables        / rows      / columns
MongoDB :   database    / collections   / documents / fields
"""


class UnableConnectServerException(Exception):
    """
    몽고 서버 연결 에러를 처리하기 위한 커스텀 익셉션
    """
    def __init__(self, message="현재 서버에 접속할 수 없습니다.."):
        self.message = message
        super().__init__(self.message)


class DataIsNotInServerException(Exception):
    """
    원하는 데이터가 없는 경우 발생하는 익셉션
    """
    def __init__(self, message="테이블이나 데이터베이스가 서버에 없습니다."):
        self.message = message
        super().__init__(self.message)


def connect_to_mongo(addr: str, timeout=5) -> MongoClient:
    """
    몽고 클라이언트를 만들어주는 함수.
    resolve conn error - https://stackoverflow.com/questions/54484890/ssl-handshake-issue-with-pymongo-on-python3
    :param addr:
    :param timeout:
    :return:
    """
    import certifi
    ca = certifi.where()
    if addr.startswith('mongodb://'):
        # set a some-second connection timeout
        client = MongoClient(addr, serverSelectionTimeoutMS=timeout * 1000)
    elif addr.startswith('mongodb+srv://'):
        client = MongoClient(addr, serverSelectionTimeoutMS=timeout * 1000, tlsCAFile=ca)
    else:
        raise Exception(f"Invalid address: {addr}")
    try:
        srv_info = client.server_info()
        conn_str = f"Connect to Mongo Atlas v{srv_info['version']}..."
        print(conn_str, f"Server Addr : {addr}")
        return client
    except Exception:
        raise UnableConnectServerException()


class Base:
    from db_hj3415 import cli as db_cli
    mongo_client: MongoClient = connect_to_mongo(db_cli.load_mongo_addr())

    def __init__(self, db: str, table: str):
        if Base.mongo_client is None:
            raise ValueError("mymongo.Base.mongo_client has not been initialized!")
        if Base.is_there(db=db, table=table):
            self._db = self.mongo_client[db]
            self._col = self._db[table]
        else:
            raise Exception(f"{db} or {table} name is incorrect.(Base.__init__())")

    def __str__(self):
        return f"db: {self.db}, table: {self.table}"

    @property
    def db(self) -> str:
        return self._db.name

    @db.setter
    def db(self, db: str):
        if Base.is_there(db=db):
            # print(f"change db : {db}")
            self._db = self.mongo_client[db]
            # db를 바꾸면 table도 한번 리프레시해줘야한다.
            self._col = self._db[self.table]
        else:
            raise DataIsNotInServerException(f"db : {db} is not in server.")

    @property
    def table(self) -> str:
        return self._col.name

    @table.setter
    def table(self, table: str):
        assert isinstance(self._db, database.Database), "You should set database first."
        if Base.is_there(db=self.db, table=table):
            # print(f"change table : {table}")
            self._col = self._db[table]
        else:
            raise DataIsNotInServerException(f"table : {table} is not in {self.db}")

    # ========================End Properties=======================

    @classmethod
    def is_there(cls, **kwargs) -> bool:
        """
        kwargs에 db나 table명을 넣어서 조회하면 서버에 있는지 확인하고 참거짓반환
        :param kwargs:
        :return:
        """
        db = kwargs.get('db', '')
        table = kwargs.get('table', '')

        if db == '' and table != '':
            raise Exception("table을 유무를 조회하려면 db명이 반드시 필요합니다.")
        elif db == '' and table == '':
            raise Exception("인자로 db명과 table명이 필요합니다.(Base.is_there())")

        is_there = False

        if db != '' and table == '':
            dbs = cls.list_db_names()
            if db in dbs:
                is_there = True
        elif db != '' and table != '':
            try:
                tables = cls.list_table_names(db)
            except DataIsNotInServerException:
                logger.warning(f"{db} 데이테베이스명이 서버에 없습니다.")
            else:
                if table in tables:
                    is_there = True
        return is_there

    @classmethod
    def list_db_names(cls) -> list:
        return sorted(cls.mongo_client.list_database_names())

    @classmethod
    def list_table_names(cls, db: str) -> list:
        if cls.is_there(db=db):
            return sorted(cls.mongo_client[db].list_collection_names())
        else:
            raise DataIsNotInServerException(f"{db} 이름을 가진 데이터베이스가 서버에 없습니다.")

    @classmethod
    def drop(cls, **kwargs) -> bool:
        db = kwargs.get('db', '')
        table = kwargs.get('table', '')

        if db == '' and table != '':
            raise Exception("table을 삭제하려면 db명이 반드시 필요합니다.")
        elif db == '' and table == '':
            raise Exception("인자로 db명과 table명이 필요합니다.(Base.drop()")

        if db != '' and table == '':
            return cls.drop_db(db)
        elif db != '' and table != '':
            try:
                tables = Base.list_table_names(db)
            except DataIsNotInServerException:
                logger.warning(f"{db} 데이테베이스명이 서버에 없습니다.")
                return False
            else:
                if table in tables:
                    cls.mongo_client[db].drop_collection(table)
                    return True
                else:
                    logger.warning(f"{table} is not in server.")
                    return False

    @classmethod
    def drop_db(cls, db: str) -> bool:
        if Base.is_there(db=db):
            cls.mongo_client.drop_database(db)
            print(f"Drop '{db}' database..")
            return True
        else:
            logger.warning(f"{db} is not in server.")
            return False

    def drop_table(self):
        self._db.drop_collection(self.table)
        print(f"Drop '{self.table}' table..")

    def list_rows(self, show_id=False) -> list:
        assert isinstance(self._col, collection.Collection), "You should set table first."
        rows = []
        if show_id:
            for row in self._col.find():
                rows.append(row)
        else:
            for row in self._col.find():
                del row['_id']
                rows.append(row)
        return rows

    def clear_table(self):
        """
        현재 설정된 컬렉션 안의 도큐먼트를 전부 삭제한다.
        (컬렉션 자체를 삭제하지는 않는다.)
        """
        assert isinstance(self._col, collection.Collection), "You should set table first."
        self._col.delete_many({})
        print(f"Delete all rows in {self.table} table..")

    def count_rows(self) -> int:
        assert isinstance(self._col, collection.Collection), "You should set table first."
        return self._col.count_documents({})

    def delete_row(self, query: dict):
        """
        query에 해당하는 도큐먼트를 삭제한다.
        """
        assert isinstance(self._col, collection.Collection), "You should set table first."
        self._col.delete_one(query)


class Corps(Base):
    """
    mongodb의 데이터 중 기업 코드로 된 데이터 베이스를 다루는 클래스
    """
    COLLECTIONS = ('c101', 'c104y', 'c104q', 'c106y', 'c106q', 'c108',
                   'c103손익계산서q', 'c103재무상태표q', 'c103현금흐름표q',
                   'c103손익계산서y', 'c103재무상태표y', 'c103현금흐름표y',
                   'dart', 'etc')

    def __init__(self, code: str = '', page: str = ''):
        super().__init__(db=code, table=page)

    @property
    def code(self) -> str:
        return self.db

    @code.setter
    def code(self, code: str):
        assert utils.is_6digit(code), f'Invalid value : {code}'
        self.db = code

    @property
    def page(self) -> str:
        return self.table

    @page.setter
    def page(self, page: str):
        assert page in self.COLLECTIONS, f'Invalid value : {page}({self.COLLECTIONS})'
        self.table = page

    # ========================End Properties=======================

    @classmethod
    def list_all_codes(cls) -> list:
        """
        기업 코드를 데이터베이스명으로 가지는 모든 6자리 숫자 코드의 db 명 반환
        """
        codes = []
        for db_name in cls.list_db_names():
            if utils.is_6digit(db_name):
                codes.append(db_name)
        return sorted(codes)

    @classmethod
    def drop_all_codes(cls):
        codes = cls.list_all_codes()
        for code in codes:
            cls.drop_db(code)

    @classmethod
    def drop_page_in_all_codes(cls, page):
        assert page in cls.COLLECTIONS, f'Invalid value : {page}({cls.COLLECTIONS})'
        codes = cls.list_all_codes()
        print(f"Drop {page} page in all codes..")
        for code in codes:
            Base.mongo_client[code].drop_collection(page)
            try:
                print(code, '-', cls.list_table_names(code))
            except DataIsNotInServerException:
                # 데이터베이스의 마자막 테이블이 삭제되면 데이테베이스가 삭제되어 에러가 발생함. 이럴 경우 처리 코드
                print(code, '-', '[]')

    @classmethod
    def get_name(cls, code: str) -> str | None:
        """
        code를 입력받아 종목명을 반환한다.
        """
        c101 = C101(code)
        try:
            name = c101.get_recent()['종목명']
        except KeyError:
            logger.warning(f"There is no name data on {code} in server")
            name = None
        return name

    @classmethod
    def _save_df(cls, code: str, page: str, df: pd.DataFrame, clear_table: bool):
        # c103, c104, c106, c108에서 주로 사용하는 저장방식
        if df.empty:
            logger.warning(f'{code}/{page} df is empty..So we will skip saving to db..')
            return

        if clear_table:
            # 페이지가 비어 있지 않으면 먼저 지운다.
            print(f"Before save data, cleaning the collection {code} / {page}...")
            cls.mongo_client[code][page].delete_many({})
            import time
            time.sleep(1)

        cls.mongo_client[code][page].insert_many(df.to_dict('records'))


    @staticmethod
    def refine_data(data: dict, refine_words: list) -> dict:
        """
        주어진 딕셔너리에서 refine_words에 해당하는 키를 삭제해서 반환하는 유틸함수.
        c10346에서 사용
        refine_words : 정규표현식 가능
        """
        copy_data = data.copy()
        import re
        for regex_refine_word in refine_words:
            # refine_word에 해당하는지 정규표현식으로 검사하고 매치되면 삭제한다.
            p = re.compile(regex_refine_word)
            for title, _ in copy_data.items():
                # data 내부의 타이틀을 하나하나 조사한다.
                m = p.match(title)
                if m:
                    del data[title]
        return data

    def _load_df(self) -> pd.DataFrame:
        try:
            df = pd.DataFrame(self.list_rows())
        except KeyError:
            logger.warning(f"There is no data on {self.db} / {self.table}")
            df = pd.DataFrame()
        return df

    def _load_list(self) -> List[dict]:
        items = []
        for doc in self._col.find():
            del doc['_id']
            items.append(doc)
        return items

    def load(self, to: str = 'df'):
        """
        데이터베이스에 저장된 페이지를 다양한 형식으로 반환한다.
        """
        types = ('df', 'list')
        assert to in types, f"to의 형식이 맞지 않습니다.{types}"

        if to == 'df':
            return self._load_df()
        elif to == 'list':
            return self._load_list()


class C101(Corps):

    PAGES = ('c101',)

    def __init__(self, code: str):
        super().__init__(code=code, page='c101')

    @classmethod
    def save(cls, code: str,  c101_data: dict) -> bool:
        """
        c101의 구조에 맞는 딕셔너리값을 받아서 구조가 맞는지 확인하고 맞으면 저장한다.
        """
        assert utils.is_6digit(code), f'Invalid value : {code}'
        page = 'c101'

        c101_template = ['date', 'code', '종목명', '업종', '주가', '거래량', 'EPS', 'BPS', 'PER', '업종PER', 'PBR',
                         '배당수익률', '최고52주', '최저52주', '거래대금', '시가총액', '베타52주', '발행주식', '유동비율', '외국인지분율']

        # 리스트 비교하기
        # reference from https://codetorial.net/tips_and_examples/compare_two_lists.html
        if c101_data['code'] != code:
            raise Exception("Code isn't equal input data and db data..")
        logger.debug(c101_data.keys())
        # c101 데이터가 c101_template의 내용을 포함하는가 확인하는 if문
        # refered from https://appia.tistory.com/101
        if (set(c101_template) - set(c101_data.keys())) == set():
            # 스크랩한 날짜 이후의 데이터는 조회해서 먼저 삭제한다.
            del_query = {'date': {"$gte": c101_data['date']}}
            Base.mongo_client[code][page].create_index([('date', ASCENDING)], unique=True)
            try:
                result = Base.mongo_client[code][page].insert_one(c101_data)
            except errors.DuplicateKeyError:
                Base.mongo_client[code][page].delete_many(del_query)
                result = Base.mongo_client[code][page].insert_one(c101_data)
            return result.acknowledged
        else:
            raise Exception('Invalid c101 dictionary structure..')

    @staticmethod
    def merge_intro(c101_dict: dict) -> dict:
        # intro를 합치기 위해 내부적으로 사용
        c101_dict['intro'] = c101_dict.get('intro1', '') + c101_dict.get('intro2', '') + c101_dict.get('intro3', '')
        try:
            del c101_dict['intro1']
        except KeyError:
            pass
        try:
            del c101_dict['intro2']
        except KeyError:
            pass
        try:
            del c101_dict['intro3']
        except KeyError:
            pass
        return c101_dict

    def get_recent(self, merge_intro=False) -> dict:
        """
        저장된 데이터에서 가장 최근 날짜의 딕셔너리를 반환한다.
        """
        try:
            d = dict(self._col.find({'date': {'$exists': True}}, {"_id": 0}).sort('date', DESCENDING).next())
            # del doc['_id'] - 위의 {"_id": 0} 으로 해결됨.
            if merge_intro:
                d = C101.merge_intro(d)
        except StopIteration:
            logger.warning("There is no data on C101")
            d = {}
        return d

    def find(self, date: str, merge_intro=False) -> dict:
        """
        해당 날짜의 데이터를 반환한다.
        만약 리턴값이 없으면 {} 을 반환한다.

        Args:
            date (str): 예 - 20201011(6자리숫자)
            merge_intro: intro를 합칠 것인지
        """
        assert utils.isYmd(date), f'Invalid date format : {date}(ex-20201011(8자리숫자))'
        converted_date = date[:4] + '.' + date[4:6] + '.' + date[6:]
        try:
            d = dict(self._col.find_one({'date': converted_date}))
        except TypeError:
            logger.warning(f"There is no data (date:{date}) on C101")
            return {}

        if merge_intro:
            d = C101.merge_intro(d)
        del d['_id']
        return d

    def get_trend(self, title: str) -> dict:
        """
        title에 해당하는 데이터베이스에 저장된 모든 값을 {날짜: 값} 형식의 딕셔너리로 반환한다.

        title should be in ['BPS', 'EPS', 'PBR', 'PER', '주가', '배당수익률', '베타52주', '거래량']

        리턴값 - 주가
        {'2023.04.05': '63900',
         '2023.04.06': '62300',
         '2023.04.07': '65000',
         '2023.04.10': '65700',
         '2023.04.11': '65900',
         '2023.04.12': '66000',
         '2023.04.13': '66100',
         '2023.04.14': '65100',
         '2023.04.17': '65300'}
        """
        titles = ['BPS', 'EPS', 'PBR', 'PER', '주가', '배당수익률', '베타52주', '거래량']
        assert title in titles, f"title should be in {titles}"
        items = dict()
        for doc in self._col.find({'date': {'$exists': True}}, {"_id": 0, "date": 1, f"{title}": 1}).sort('date', ASCENDING):
            items[doc['date']] = doc[f'{title}']
        return items


class C106(Corps):

    PAGES = ('c106y', 'c106q')

    def __init__(self, code: str, page: str):
        """
        page 는 c106y 또는 c106q
        :param code:
        :param page:
        """
        super().__init__(code=code, page=page)

    @classmethod
    def save(cls, code: str, page: str, c106_df: pd.DataFrame):
        assert utils.is_6digit(code), f'Invalid code : {code}'
        assert page in ['c106q', 'c106y'], f'Invalid page : {page}'

        clear_table = False
        if Base.mongo_client[code][page].count_documents({}) != 0:
            clear_table = True

        Base.mongo_client[code][page].create_index([('항목', TEXT)], unique=True)
        cls._save_df(code=code, page=page, df=c106_df, clear_table=clear_table)

    def list_row_titles(self) -> list:
        titles = []
        for item in self.list_rows():
            titles.append(item['항목'])
        return list(set(titles))

    def find(self, row_title: str) -> dict:
        """
        title에 해당하는 항목을 딕셔너리로 반환한다.
        """
        data = self._col.find_one({'항목': {'$eq': row_title}})
        if data is None:
            logger.warning(f'{row_title} is not in {self.table}')
            data = {}
        return Corps.refine_data(data, ['_id', '항목'])


class C1034(Corps, ABC):
    def __init__(self, code: str, page: str):
        super().__init__(code=code, page=page)

    def list_row_titles(self) -> list:
        titles = []
        for item in self.list_rows():
            titles.append(item['항목'])
        return list(set(titles))

    def _find(self, row_title: str, refine_words=None) -> Tuple[int, List[dict]]:
        """
        _id는 내부에서 제거하기때문에 refine 하지 않아도 됨.
        c103의 경우는 중복되는 이름의 항목이 있기 때문에
        이 함수는 반환되는 딕셔너리 리스트와 갯수로 구성되는 튜플을 반환한다.
        :param row_title: 해당하는 항목을 검색하여 딕셔너리를 포함한 리스트로 반환
        :param refine_words: 리스트 형식으로 없애자하는 col_title을 넣어준다.
        :return:
        """
        if refine_words is None:
            # 빈리스트는 아무 col_title도 없애지 않는다는 뜻임
            refine_words = []
        else:
            assert isinstance(refine_words, List), "refine_words 는 리스트 형식이어야 합니다."

        # _id는 삭제하기 위해 넣어준다.
        refine_words.append('_id')

        count = 0
        data_list = []
        for data in self._col.find({'항목': {'$eq': row_title}}):
            # 도큐먼트에서 title과 일치하는 항목을 찾아낸다.
            count += 1
            # refine_data함수를 통해 삭제를 원하는 필드를 제거하고 data_list에 추가한다.
            data_list.append(Corps.refine_data(data, refine_words))
        return count, data_list

    @abstractmethod
    def find(self, row_title: str, remove_yoy) -> Tuple[int, dict]:
        """
        :param row_title: 해당하는 항목을 반환한다.
        :param remove_yoy: 전분기대비, 전년대비를 삭제할지 말지
        :return: Tuple[int, dict]
        """
        pass

    @staticmethod
    def sum_each_data(data_list: List[dict]) -> dict:
        """
        검색된 딕셔너리를 모은 리스트를 인자로 받아서 각각의 기간에 맞춰 합을 구해 하나의 딕셔너리로 반환한다.
        """
        # 전분기에 관련항목은 더하는 것이 의미없어서 제거한다.
        new_data_list = []
        for data in data_list:
            new_data_list.append(C1034.refine_data(data, ['^전.+대비.*', ]))

        sum_dict = {}
        periods = list(new_data_list[0].keys())
        # 여러딕셔너리를 가진 리스트의 합 구하기
        for period in periods:
            sum_dict[period] = sum(utils.nan_to_zero(data[period]) for data in new_data_list)
        return sum_dict

    @staticmethod
    def latest_dict_value(data: dict, pop_count=2) -> Tuple[str, float]:
        """
        가장 최근 년/분기 값 - evaltools에서도 사용할수 있도록 staticmethod로 뺐음.

        해당 타이틀의 가장 최근의 년/분기 값을 튜플 형식으로 반환한다.

        Args:
            data (dict): 찾고자하는 딕셔너리 데이터
            pop_count: 유효성 확인을 몇번할 것인가

        Returns:
            tuple: ex - ('2020/09', 39617.5) or ('', 0)

        Note:
            만약 최근 값이 nan 이면 찾은 값 바로 직전 것을 한번 더 찾아 본다.\n
            데이터가 없는 경우 ('', nan) 반환한다.\n
        """

        def is_valid_value(value) -> bool:
            """
            숫자가 아닌 문자열이나 nan 또는 None의 경우 유효한 형식이 아님을 알려 리턴한다.
            """
            if isinstance(value, str):
                # value : ('Unnamed: 1', '데이터가 없습니다.') 인 경우
                is_valid = False
            elif math.isnan(value):
                # value : float('nan') 인 경우
                is_valid = False
            elif value is None:
                # value : None 인 경우
                is_valid = False
            else:
                is_valid = True
            """
            elif value == 0:
                is_valid = False
            """
            return is_valid

        # print(f'raw data : {data}')
        # remove_yoy
        data = Corps.refine_data(data,['^전.+대비.*'])
        # print(f'after remove_yoy : {data}')

        # 데이터를 추출해서 사용하기 때문에 원본 데이터는 보존하기 위해서 카피해서 사용
        data_copied = copy.deepcopy(data)

        for i in range(pop_count):
            try:
                d, v = data_copied.popitem()
            except KeyError:
                # when dictionary is empty
                return '', float('nan')
            if str(d).startswith('20') and is_valid_value(v):
                logger.debug(f'last_one : {v}')
                return d, v

        return '', float('nan')

    def latest_value(self, title: str, pop_count=2) -> Tuple[str, float]:
        """
        해당 타이틀의 가장 최근의 년/분기 값을 튜플 형식으로 반환한다.

        Args:
            title (str): 찾고자 하는 타이틀
            pop_count: 유효성 확인을 몇번할 것인가

        Returns:
            tuple: ex - ('2020/09', 39617.5) or ('', 0)

        Note:
            만약 최근 값이 nan 이면 찾은 값 바로 직전 것을 한번 더 찾아 본다.\n
            데이터가 없는 경우 ('', nan) 반환한다.\n
        """
        c, row_data = self.find(title, remove_yoy=True)
        # print(row_data)
        od = OrderedDict(sorted(row_data.items(), reverse=False))
        # print(f'{title} : {od}')
        return C1034.latest_dict_value(od, pop_count)

    def sum_recent_4q(self, title: str) -> Tuple[str, float]:
        """최근 4분기 합

        분기 페이지 한정 해당 타이틀의 최근 4분기의 합을 튜플 형식으로 반환한다.

        Args:
            title (str): 찾고자 하는 타이틀

        Returns:
            tuple: (계산된 4분기 중 최근분기, 총합)

        Raises:
            TypeError: 페이지가 q가 아닌 경우 발생

        Note:
            분기 데이터가 4개 이하인 경우 그냥 최근 연도의 값을 찾아 반환한다.
        """
        if self.page.endswith('q'):
            # 딕셔너리 정렬 - https://kkamikoon.tistory.com/138
            # reverse = False 이면 오래된것부터 최근순으로 정렬한다.
            od_q = OrderedDict(sorted(self.find(title, remove_yoy=True)[1].items(), reverse=False))
            logger.debug(f'{title} : {od_q}')

            if len(od_q) < 4:
                # od_q의 값이 4개 이하이면 그냥 최근 연도의 값으로 반환한다.
                self.page = self.page[:-1] + 'y'
                return self.latest_value(title)
            else:
                q_sum = 0
                date_list = list(od_q.keys())
                while True:
                    try:
                        latest_period = date_list.pop()
                    except IndexError:
                        latest_period = ""
                        break
                    else:
                        if str(latest_period).startswith('20'):
                            break

                for i in range(4):
                    # last = True 이면 최근의 값부터 꺼낸다.
                    d, v = od_q.popitem(last=True)
                    logger.debug(f'd:{d} v:{v}')
                    q_sum += 0 if math.isnan(v) else v
                return str(latest_period), round(q_sum, 2)
        else:
            raise TypeError(f'Not support year data..{self.page} on sum_recent_4q')

    def find_yoy(self, title: str) -> float:
        """

        타이틀에 해당하는 전년/분기대비 값을 반환한다.\n

        Args:
            title (str): 찾고자 하는 타이틀

        Returns:
            float: 전년/분기대비 증감율

        Note:
            중복되는 title 은 첫번째것 사용\n
        """

        c, dict_list = self._find(title, ['항목'])

        if c == 0:
            return math.nan
        else:
            # C103의 경우 합치지 않고 그냥 첫번째 것을 사용한다.
            data = dict_list[0]
        #print(data)
        if self.page.endswith('q'):
            return data['전분기대비']
        else:
            return data['전년대비 1']


class C103(C1034):

    PAGES = ('c103손익계산서q', 'c103재무상태표q', 'c103현금흐름표q', 'c103손익계산서y', 'c103재무상태표y', 'c103현금흐름표y')

    def __init__(self, code: str, page: str):
        """
        :param code:
        :param page: 'c103손익계산서q', 'c103재무상태표q', 'c103현금흐름표q', 'c103손익계산서y', 'c103재무상태표y', 'c103현금흐름표y'
        """
        super().__init__(code=code, page=page)

    @classmethod
    def save(cls, code: str, page: str, c103_df: pd.DataFrame):
        """데이터베이스에 저장

        Example:
            c103_list 예시\n
            [{'항목': '자산총계', '2020/03': 3574575.4, ... '전분기대비': 3.9},
            {'항목': '유동자산', '2020/03': 1867397.5, ... '전분기대비': 5.5}]

        Note:
            항목이 중복되는 경우가 있기 때문에 c104처럼 각 항목을 키로하는 딕셔너리로 만들지 않는다.
        """
        assert utils.is_6digit(code), f'Invalid code : {code}'
        assert page in ['c103손익계산서q', 'c103재무상태표q', 'c103현금흐름표q', 'c103손익계산서y', 'c103재무상태표y', 'c103현금흐름표y'], f'Invalid page : {page}'

        clear_table = False
        if Base.mongo_client[code][page].count_documents({}) != 0:
            clear_table = True

        Base.mongo_client[code][page].create_index([('항목', TEXT)], unique=False)
        cls._save_df(code=code, page=page, df=c103_df, clear_table=clear_table)

    def find(self, row_title: str, remove_yoy=False) -> Tuple[int, dict]:
        """
        :param row_title: 해당하는 항목을 반환한다.
        :param remove_yoy: 전분기대비, 전년대비를 삭제할지 말지
        :return: 중복된 항목은 합쳐서 딕셔너리로 반환하고 중복된 갯수를 정수로 반환
        """
        if remove_yoy:
            refine_words = ['항목', '^전.+대비.*']
        else:
            refine_words = ['항목']

        c, dict_list = super(C103, self)._find(row_title=row_title, refine_words=refine_words)
        if c > 1:
            return c, self.sum_each_data(dict_list)
        elif c == 0:
            return c, {}
        else:
            return c, dict_list[0]


class C104(C1034):

    PAGES = ('c104y', 'c104q')

    def __init__(self, code: str, page: str):
        """
        :param code:
        :param page: c104q, c104y
        """
        super().__init__(code=code, page=page)

    @classmethod
    def save(cls, code: str, page: str, c104_df: pd.DataFrame):
        """데이터베이스에 저장

        c104는 4페이지의 자료를 한 컬렉션에 모으는 것이기 때문에
        stamp 를 검사하여 12시간 전보다 이전에 저장된 자료가 있으면
        삭제한 후 저장하고 12시간 이내의 자료는 삭제하지 않고
        데이터를 추가하는 형식으로 저장한다.

        Example:
            c104_data 예시\n
            [{'항목': '매출액증가율',...'2020/12': 2.78, '2021/12': 14.9, '전년대비': 8.27, '전년대비1': 12.12},
            {'항목': '영업이익증가율',...'2020/12': 29.62, '2021/12': 43.86, '전년대비': 82.47, '전년대비1': 14.24}]
        """
        assert utils.is_6digit(code), f'Invalid code : {code}'
        assert page in ['c104q', 'c104y'], f'Invalid page : {page}'

        time_now = datetime.datetime.now()
        clear_table = False
        try:
            stamp = Base.mongo_client[code][page].find_one({'항목': 'stamp'})['time']
            if stamp < (time_now - datetime.timedelta(days=.005)):  # 약 7분
                # 스템프가 약 10분 이전이라면..연속데이터가 아니라는 뜻이므로 컬렉션을 초기화한다.
                clear_table = True
        except TypeError:
            # 스템프가 없다면...
            clear_table = True

        Base.mongo_client[code][page].create_index([('항목', TEXT)], unique=True)
        cls._save_df(code=code, page=page, df=c104_df, clear_table=clear_table)
        # 항목 stamp를 찾아 time을 업데이트하고 stamp가 없으면 insert한다.
        Base.mongo_client[code][page].update_one({'항목': 'stamp'}, {"$set": {'time': time_now}}, upsert=True)

    def list_row_titles(self) -> list:
        """
        c104는 stamp항목이 있기 때문에 삭제하고 리스트로 반환한다.
        """
        titles = super().list_row_titles()
        try:
            titles.remove('stamp')
        except ValueError:
            # stamp 항목이 없는 경우 그냥넘어간다.
            pass
        return titles
    
    def list_rows(self) -> list:
        """
        Base.list_rows()에서 항목 stamp를 제한다.
        :return: 
        """
        return [x for x in super().list_rows() if x['항목'] != 'stamp']

    def find(self, row_title: str, remove_yoy=False) -> Tuple[int, dict]:
        """
        :param row_title: 해당하는 항목을 반환한다.
        :param remove_yoy: 전분기대비, 전년대비를 삭제할지 말지
        :return: 중복된 항목은 합쳐서 딕셔너리로 반환하고 중복된 갯수를 정수로 반환
        """
        if remove_yoy:
            refine_words = ['항목', '^전.+대비.*']
        else:
            refine_words = ['항목']

        c, l = super(C104, self)._find(row_title=row_title, refine_words=refine_words)

        if c == 0:
            return c, {}
        else:
            return c, l[0]

    def get_stamp(self) -> datetime.datetime:
        """
        c104y, c104q가 작성된 시간이 기록된 stamp 항목을 datetime 형식으로 리턴한다.
        """
        return self._col.find_one({"항목": "stamp"})['time']

    def modify_stamp(self, days_ago: int):
        """
        인위적으로 타임스템프를 수정한다 - 주로 테스트 용도
        """
        try:
            before = self._col.find_one({'항목': 'stamp'})['time']
        except TypeError:
            # 이전 타임 스탬프가 없는 경우
            before = None
        time_2da = datetime.datetime.now() - datetime.timedelta(days=days_ago)
        self._col.update_one({'항목': 'stamp'}, {"$set": {'time': time_2da}}, upsert=True)
        after = self._col.find_one({'항목': 'stamp'})['time']
        logger.info(f"Stamp changed: {before} -> {after}")


class C108(Corps):
    def __init__(self, code: str):
        super().__init__(code=code, page='c108')

    @classmethod
    def save(cls, code: str, c108_data: pd.DataFrame):
        assert utils.is_6digit(code), f'Invalid value : {code}'
        page = 'c108'

        Base.mongo_client[code][page].create_index([('날짜', ASCENDING)], unique=False)
        cls._save_df(code=code, page=page, df=c108_data, clear_table=True)

    def get_recent_date(self) -> datetime.datetime | None:
        # 저장되어 있는 데이터베이스의 최근 날짜를 찾는다.
        try:
            r_date = self._col.find({'날짜': {'$exists': True}}).sort('날짜', DESCENDING).next()['날짜']
        except StopIteration:
            # 날짜에 해당하는 데이터가 없는 경우
            return None

        return datetime.datetime.strptime(r_date, '%y/%m/%d')

    def get_recent(self) -> List[dict] | None:
        """

        저장된 데이터에서 가장 최근 날짜의 딕셔너리를 가져와서 리스트로 포장하여 반환한다.

        Returns:
            list: 한 날짜에 c108 딕셔너리가 여러개 일수 있어서 리스트로 반환한다.
        """
        try:
            r_date = self.get_recent_date().strftime('%y/%m/%d')
        except AttributeError:
            # 최근데이터가 없어서 None을 반환해서 에러발생한 경우
            return None
        # 찾은 날짜를 바탕으로 데이터를 검색하여 리스트로 반환한다.
        r_list = []
        for r_c108 in self._col.find({'날짜': {'$eq': r_date}}):
            del r_c108['_id']
            r_list.append(r_c108)
        return r_list


class Dart(Corps):
    def __init__(self, code: str):
        super().__init__(code=code, page='dart')

    @classmethod
    def save(cls, code: str, dart_data: dict) -> bool:
        """
        dart overview의 구조에 맞는 딕셔너리값을 받아서 구조가 맞는지 확인하고 맞으면 저장한다.
        공시 dart_data 예시
        {'corp_cls': 'Y',
        'corp_code': '00414850',
        'corp_name': '효성 ITX',
        'flr_nm': '효성 ITX',
        'rcept_dt': '20240830',
        'rcept_no': '20240830800804',
        'report_nm': '[기재정정]거래처와의거래중단',
        'rm': '유',
        'stock_code': '094280'}
        :param code:
        :param dart_data:
        :return:
        """
        assert utils.is_6digit(code), f'Invalid value : {code}'
        page = 'dart'

        dart_template = ['corp_cls', 'corp_code', 'corp_name', 'flr_nm', 'rcept_dt', 'rcept_no', 'report_nm', 'rm', 'stock_code', 'link']

        # 리스트 비교하기
        # reference from https://codetorial.net/tips_and_examples/compare_two_lists.html
        if dart_data['stock_code'] != code:
            raise Exception("Code isn't equal input data and db data..")
        logger.debug(dart_data.keys())

        # dart 데이터가 dart_template의 내용을 포함하는가 확인하는 if문
        # refered from https://appia.tistory.com/101
        if (set(dart_template) - set(dart_data.keys())) == set():
            Base.mongo_client[code][page].create_index([('rcept_no', ASCENDING)], unique=True)
            try:
                result = Base.mongo_client[code][page].insert_one(dart_data)
            except errors.DuplicateKeyError:
                Base.mongo_client[code][page].delete_one({'rcept_no': dart_data['rcept_no']})
                result = Base.mongo_client[code][page].insert_one(dart_data)
            return result.acknowledged
        else:
            raise Exception('dart 딕셔너리 구조가 맞지 않습니다. 혹시 link를 추가하는 것을 잊었을까요..')






class MI(Base):
    """mi 데이터베이스 클래스

    Note:
        db - mi\n
        col - 'aud', 'chf', 'gbond3y', 'gold', 'silver', 'kosdaq', 'kospi', 'sp500', 'usdkrw', 'wti', 'avgper', 'yieldgap', 'usdidx' - 총 13개\n
        doc - date, value\n
    """
    COL_TITLE = ('aud', 'chf', 'gbond3y', 'gold', 'silver', 'kosdaq', 'kospi',
                 'sp500', 'usdkrw', 'wti', 'avgper', 'yieldgap', 'usdidx')

    def __init__(self, index: str):
        super().__init__(db='mi', table=index)

    @property
    def index(self) -> str:
        return self.table

    @index.setter
    def index(self, index: str):
        assert index in self.COL_TITLE, f'Invalid value : {index}({self.COL_TITLE})'
        self.table = index

    # ========================End Properties=======================

    def get_recent(self) -> Tuple[str, float]:
        """저장된 가장 최근의 값을 반환하는 함수
        """
        try:
            d = dict(self._col.find({'date': {'$exists': True}}, {"_id": 0}).sort('date', DESCENDING).next())
            # del doc['_id'] - 위의 {"_id": 0} 으로 해결됨.
            return d['date'], d['value']
        except StopIteration:
            logger.warning(f"There is no data on {self.index}")
            return '', float('nan')

    def get_trend(self) -> dict:
        """
        해당하는 인덱스의 전체 트렌드를 딕셔너리로 반환한다.
        리턴값 - index
        {'2023.04.05': '63900',
         '2023.04.06': '62300',
         '2023.04.07': '65000',
         '2023.04.10': '65700',
         '2023.04.11': '65900',
         '2023.04.12': '66000',
         '2023.04.13': '66100',
         '2023.04.14': '65100',
         '2023.04.17': '65300'}
        """
        items = dict()
        for doc in self._col.find({'date': {'$exists': True}}, {"_id": 0, "date": 1, "value": 1}).sort('date', ASCENDING):
            items[doc['date']] = doc['value']
        return items

    @classmethod
    def save(cls, index: str, mi_data: dict) -> bool:
        """MI 데이터 저장

        Args:
            index (str): 'aud', 'chf', 'gbond3y', 'gold', 'silver', 'kosdaq', 'kospi', 'sp500', 'usdkrw', 'wti', 'avgper', 'yieldgap', 'usdidx'
            mi_data (dict): ex - {'date': '2021.07.21', 'value': '1154.50'}
        """
        assert index in cls.COL_TITLE, f'Invalid value : {index}({cls.COL_TITLE})'
        Base.mongo_client['mi'][index].create_index([('date', ASCENDING)], unique=True)
        # scraper에서 해당일 전후로 3일치 데이터를 받아오기때문에 c101과는 다르게 업데이트 한다.
        result = Base.mongo_client['mi'][index].update_one(
            {'date': mi_data['date']}, {"$set": {'value': mi_data['value']}}, upsert=True)
        return result.acknowledged











class DateBase(Base):
    """
    날짜를 컬렉션으로 가지는 데이터베이스를 위한 기반클래스
    """
    def __init__(self, client: MongoClient, db_name: str, date: str):
        if utils.isYmd(date):
            super().__init__(client=client, db_name=db_name, col_name=date)
        else:
            raise Exception(f"Invalid date : {date}(%Y%m%d)")

    @property
    def date(self):
        return self.col_name

    @date.setter
    def date(self, date: str):
        if utils.isYmd(date):
            self.col_name = date
        else:
            raise Exception(f"Invalid date : {date}(%Y%m%d)")

    # ========================End Properties=======================

    def save_df(self, df: pd.DataFrame) -> bool:
        if df.empty:
            print('Dataframe is empty..So we will skip saving db..')
            return False

        self.clear_docs_in_col()
        print(f"Save new data to '{self.db_name}' / '{self.col_name}'")
        result = self.my_col.insert_many(df.to_dict('records'))
        return result.acknowledged

    def load_df(self) -> pd.DataFrame:
        try:
            df = pd.DataFrame(list(self.my_col.find({}))).drop(columns=['_id'])
        except KeyError:
            df = pd.DataFrame()
        return df


class EvalByDate(Base):
    """
    각 날짜별로 만들어진 eval-report 데이터프레임을 관리하는 클래스
    DB_NAME : eval
    COL_NAME : Ymd형식 날짜
    """
    EVAL_DB = 'eval'

    def __init__(self, client: MongoClient, date: str):
        super().__init__(client, self.EVAL_DB, date)
        # 인덱스 설정
        #self.my_col.create_index('code', unique=True)

    @staticmethod
    def get_dates(client: MongoClient) -> List[str]:
        # 데이터베이스에 저장된 날짜 목록을 리스트로 반환한다.
        dates_list = client.eval.list_collection_names()
        dates_list.sort()
        return dates_list

    @classmethod
    def get_recent(cls, client: MongoClient, type: str):
        """
        eval 데이터베이스의 가장 최근의 유요한 자료를 반환한다.
        type의 종류에 따라 반환값이 달라진다.[date, dataframe, dict]
        """
        dates = cls.get_dates(client)

        while len(dates) > 0:
            recent_date = dates.pop()
            recent_df = cls(client, recent_date).load_df()
            if len(recent_df) != 0:
                if type == 'date':
                    return recent_date
                elif type == 'dataframe':
                    return recent_df
                elif type == 'dict':
                    return recent_df.to_dict('records')
                else:
                    raise Exception(f"Invalid type : {type}")

        return None

