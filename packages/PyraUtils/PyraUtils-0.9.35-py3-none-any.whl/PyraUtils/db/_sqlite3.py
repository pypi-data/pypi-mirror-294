"""
created by：2018-2-23 14:15:57
modify by: 2023-05-13 15:05:05

功能：sqlite3的方法函数的封装。
"""

import sqlite3
from ..log.logger._loguru import LoguruHandler

logger = LoguruHandler()


def handle_db_operations(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except sqlite3.DatabaseError as e:
            logger.error(f"Database error during {func.__name__}: {e}")
            raise
    return wrapper



class SQLite3Util:
    """
    使用时可以像这样：
    with SQLite3Util('my.db') as db:
        result = db.query('SELECT * FROM users WHERE age > ?', (18,))
        for row in result:
            print(row['username'], row['age'])
    """

    def __init__(self, dbfile=None):
        """
        如果dbfile为None或空字符串，就使用内存数据库，
        否则就使用dbfile指定的数据库文件存
        """
        self.db = sqlite3.connect(dbfile or ':memory:')
        self.db.row_factory = sqlite3.Row
        self.c = self.db.cursor()

    @handle_db_operations
    def query(self, sql, params=None):
        """
        执行查询操作，返回所有结果。
        """
        with self.db:
            self.c.execute(sql, params or ())
            return self.c.fetchall()

    @handle_db_operations
    def insert(self, table, data):
        """
        执行插入操作，返回自动生成的 ID 号。
        """
        fields = ','.join(data.keys())
        values = tuple(data.values())
        placeholders = ','.join(['?'] * len(data))
        sql = f'INSERT INTO {table} ({fields}) VALUES ({placeholders})'

        with self.db:
            self.c.execute(sql, values)
            return self.c.lastrowid

    @handle_db_operations
    def select(self, table, fields='*', condition='', params=None):
        """
        执行查询操作，并使用 Row 创建可迭代的行对象。
        """
        sql = f'SELECT {fields} FROM {table}'
        if condition:
            sql += f' WHERE {condition}'

        with self.db:
            self.c.execute(sql, params or ())
            return self.c.fetchall()

    @handle_db_operations
    def execute(self, sql, params=None, many=False):
        """
        执行任意 SQL 语句，返回是否修改了数据。
        可以通过判断 total_changes 是否大于 0 来确定是否有更新。
        """
        with self.db:
            if many:
                self.c.executemany(sql, params or [])
            else:
                self.c.execute(sql, params or ())
            return self.db.total_changes > 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.db.rollback()
            logger.error(f"Exception has been handled and the transaction is rollbacked.")
        else:
            self.db.commit()
        self.c.close()
        self.db.close()
