"""
Package Title: 

settings.py 中替换引擎
DATABASES.xx
    'ENGINE': 'custom_db.mysql',
目标: 拦截mysql 2013错误，回放sql
todo:
    1.哪些可以回放?   读操作/..
    2.哪些不可以回放?
    3.是否可以完成连接copy, 1:1 复制出错前的连接状态
"""

import logging
import time

from django.utils.asyncio import async_unsafe
from django.db.backends.mysql.base import Database, CursorWrapper
from django.db.backends.mysql.base import DatabaseWrapper as MysqlDatabaseWrapper
from django.db.utils import (
    DataError,
    DatabaseErrorWrapper,
    IntegrityError,
    OperationalError,
    ProgrammingError,
    InternalError,
)

logger = logging.getLogger("django.db.backends")


class CustomCursorWrapper(CursorWrapper):
    """
    定制: mysql 2013
    """
    codes_for_retry_error = (
        2013,  # CHECK constraint failed
    )

    def retry(self, query, args=None):
        logger.info(f"{self.cursor} will retry query:{query} args:{args}")
        time.sleep(10)
        # 获取连接
        # self.cursor.connection.close()
        return

    def execute(self, query, args=None):
        try:
            # args is None means no string interpolation
            logger.info(f"CustomCursorWrapper execute: {query}:{args}")
            return self.cursor.execute(query, args)
        except Database.OperationalError as e:
            # Map some error codes to IntegrityError, since they seem to be
            # misclassified and Django would prefer the more logical place.
            logger.error(f"CustomCursorWrapper error: {e}")
            # e.args[0] == 2013. Lost connection to MySQL server during query
            # todo: 1.copy connection 重建 2.是否回放sql
            if e.args[0] in self.codes_for_retry_error:
                return self.retry(query, args)
            if e.args[0] in self.codes_for_integrityerror:
                raise IntegrityError(*tuple(e.args))
            raise

    def executemany(self, query, args):
        try:
            return self.cursor.executemany(query, args)
        except Database.OperationalError as e:
            # Map some error codes to IntegrityError, since they seem to be
            # misclassified and Django would prefer the more logical place.
            if e.args[0] in self.codes_for_integrityerror:
                raise IntegrityError(*tuple(e.args))
            raise


class DatabaseWrapper(MysqlDatabaseWrapper):

    @async_unsafe
    def create_cursor(self, name=None):
        """
        拦截游标wrapper
        @param name:
        @return:
        """
        cursor = self.connection.cursor()
        logger.info(f"create_cursor: {cursor}")
        return CustomCursorWrapper(cursor)

    def _cursor(self, name=None):
        self.ensure_connection()
        with self.wrap_database_errors:
            return self._prepare_cursor(self.create_cursor(name))
