import logging
from django.conf import settings
from django.db.models.manager import Manager, BaseManager
from django.db import models


logger = logging.getLogger('debug')

"""
方案一：全局配置所有ORM操作走主库
这个方案通过在Django的settings.py文件中设置一个配置项（例如PrimaryQuerySetForWrite），
然后在自定义的QuerySet类中根据这个配置来决定是否默认使用主库。
这种方式适合于大部分操作需要确保数据一致性的应用场景，可以简单地通过改变配置来切换行为。


方案二：使用装饰器指定方法走主库
通过定义一个装饰器use_default_db，可以在特定的QuerySet方法上使用这个装饰器，使得这些方法在执行时强制使用主库。
这种方式提供了更细粒度的控制，允许在不影响整体读写分离策略的前提下，针对特定操作确保数据一致性。

使用建议：
如果您的应用中数据一致性是首要考虑，而读写分离带来的性能优化不是主要关注点，推荐使用方案一。
如果您的应用大多数时间能够从读写分离中获益，只有在少数关键操作中需要确保数据一致性，推荐使用方案二。


PrimaryQuerySetUsingEnable=True orm 全局主库
PrimaryQuerySetMethodUsingEnable=True orm method 被装饰器的使用主库
"""


def use_default_db(func):
    """
    方案二: 指定的方法走主库. PrimaryQuerySetMethodUsingEnable
    eg: 被装饰的方法，将使用主库
    class QuerySet(models.QuerySet):
        @use_default_db
        def first(self):
            return supper().first()

    @param func:
    @return:
    """
    def wrapper(*args, **kwargs):
        self = args[0]
        _for_method_using = getattr(settings, 'PrimaryQuerySetMethodUsingEnable', False)
        logger.info(f"PrimaryQuerySetMethodUsingEnable: {_for_method_using} -->set using default")
        if _for_method_using:
            self = self.using('default')
        # func是QuerySet 实列的方法. 调用原始的方法
        return func(self, *args[1:], **kwargs)
    return wrapper


class PrimaryQuerySet(models.QuerySet):

    def _set_default_db(self, using=None):
        """
        方案一: 通过配置settings.PrimaryQuerySetUsingEnable = True 开启所有orm queryset都走主库.

        1.用户指定using
           否: 保持默认
           是: 使用用户的指定的数据库
        2.查看是否配置了 PrimaryQuerySetUsingEnable
            否: 保持默认
            是：使用当前queryset的操作当作是写操作，使用主库
        @return:
        """
        # 用户指定using
        if using:
            return
        # 查看是否配置了 PrimaryQuerySetUsing
        _for_using = getattr(settings, 'PrimaryQuerySetUsingEnable', '')
        if _for_using:
            self._db = 'default'
        return

    def __init__(self, model=None, query=None, using=None, hints=None):
        super().__init__(model=model, query=query, using=using, hints=hints)
        self._set_default_db(using=using)

    @use_default_db
    def first(self):
        """获取第一个对象，强制使用默认数据库"""
        return super().first()

    @use_default_db
    def last(self):
        return super().last()

    @use_default_db
    def exists(self):
        return super().exists()

    @use_default_db
    def count(self):
        return super().count()


# class Manager(BaseManager.from_queryset(QuerySet)):
#     pass
class PrimaryManager(BaseManager.from_queryset(PrimaryQuerySet)):
    pass

#
# class PrimaryManager(models.Manager):
#     """使用PrimaryQuerySet作为默认查询集"""
#     def get_queryset(self):
#         return PrimaryQuerySet(self.model, using=self._db)

