# coding=utf-8

"""
@fileName       :   task_config.py
@data           :   2024/8/27
@author         :   jiangmenggui@hosonsoft.com
"""
import queue
import random
from csv import reader as csv_reader
from threading import Lock
from typing import Any

from lljz_tools.client.db_client import MySQLConnectionPool
from lljz_tools.excel import ExcelReader
from lljz_tools.simple_pref_test.utils import FilePath, DataBase


class _TaskConfig[T]:

    def __init__(self, data: list[T]):
        self._data = data
        self.lock = Lock()

    def get(self) -> T:
        pass


class _TaskRandomConfig[T](_TaskConfig[T]):

    def get(self) -> T:
        with self.lock:
            return random.choice(self._data)


class _TaskLoopConfig[T](_TaskConfig[T]):

    def __init__(self, data: list[T]):
        super().__init__(data)
        self._data = queue.Queue()
        for item in data:
            self._data.put(item)

    def get(self) -> T:
        if self._data.empty():
            raise StopIteration("数据读取完毕")
        item = self._data.get()
        self._data.put(item)
        return item


class _TaskOnceConfig[T](_TaskConfig[T]):

    def __init__(self, data: list[T]):
        super().__init__(data)
        self._data = queue.Queue()
        for item in data:
            self._data.put(item)

    def get(self) -> T:
        if self._data.empty():
            raise StopIteration("数据读取完毕")
        item = self._data.get()
        return item


class TaskConfig[T:Any]:
    """
    任务配置

    model：数据读取模式
        - loop: 循环读取，当数据读取完毕后，从头开始读取
        - once: 一次性读取，当数据读取完毕后，不再读取
        - random: 每次随机取一个值
    """

    def __init__(self, *, data: list[T] = None, database: DataBase = None, csv: FilePath = None,
                 excel: FilePath = None, model='loop'):
        assert len([i for i in [data, database, csv, excel] if i is not None]) == 1, \
            "data、database、csv、excel参数必须有且仅有一个不为空"
        if data is not None:
            _data = data
        elif database is not None:
            _data = self._read_database(database)
        elif csv is not None:
            _data = self._read_csv(csv)
        elif excel is not None:
            _data = self._read_excel(excel)
        else:
            _data = []
        if model == 'random':
            self._config = _TaskRandomConfig(_data)
        elif model == 'once':
            self._config = _TaskOnceConfig(_data)
        else:
            self._config = _TaskLoopConfig(_data)

    @staticmethod
    def _read_database(database: DataBase):
        with MySQLConnectionPool(database.uri, database.ssh_url, show_sql=database.show_sql) as pool:
            with pool.connect() as mysql:
                return mysql.select_all(database.sql)

    @staticmethod
    def _read_csv(csv: FilePath):
        data = []
        with open(csv, mode='r', encoding='utf-8') as file:
            reader = csv_reader(file)
            title = next(reader)
            for row in reader:
                # row是一个列表，包含了当前行的所有值
                data.append(dict(zip(title, row)))
        return data

    @staticmethod
    def _read_excel(excel: FilePath):
        excel = ExcelReader(excel)
        return excel.read()

    def get(self) -> T:
        return self._config.get()


class TaskConfigGroup[T: Any]:
    def __init__(self, data: dict[int | str, list[T]]):
        self.data = {k: TaskConfig[T](data=v) for k, v in data.items()}

    def get(self, key: int | str) -> T:
        return self.data[key].get()


if __name__ == '__main__':
    pass
