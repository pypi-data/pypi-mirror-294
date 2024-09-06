import random
import logging
import threading
from django.db.transaction import get_connection

from djtokit.ctx.context import RequestContext

# from uhashring import HashRing


logger = logging.getLogger('debug')

# 读库：可以支持多个
# Aurora: 最多15个副本处理只读查询流量。
db_read = ['readonly', ]
# Aurora: 写
db_default = 'default'
db_write = [db_default]
db_all = db_write.extend(db_read)
# db_read_hash_ring = HashRing(db_read)


def check_in_atomic_block(using=None):
    """
    验证 conn 线程安全
    @param using:
    @return:
    """
    conn = get_connection(using)
    conn.validate_thread_sharing()
    # logger.debug(f"check_in_atomic_block tid({threading.get_ident()})  conn ({id(conn)}) "
    #              f"in_atomic_block ({conn.in_atomic_block})")
    return conn.in_atomic_block


class PrimaryReplicaRouter:
    """
    settings.py
    DATABASE_ROUTERS = ['...', 'luffy.common.custom_db.router.rw.PrimaryReplicaRouter']

    读写分离:  写主读从
    """
    def show(self):
        return f"tid({threading.get_ident()})  conn ({id(get_connection())})"

    def db_for_read(self, model, **hints):
        """
        Reads go to a randomly-chosen replica.
        """
        db = random.choice(db_read)
        # logger.debug(f"PrimaryReplicaRouter read {self.show()} db ({db})")
        return db

    def db_for_write(self, model, **hints):
        """
        Writes always go to primary.
        """
        # logger.debug(f"PrimaryReplicaRouter write {self.show()} db ({db_default})")
        return db_default

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the primary/replica pool.
        """
        if obj1._state.db in db_all and obj2._state.db in db_all:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        All non-auth models end up in this pool.
        """
        return True


class PrimaryReplicaRouterCtx(PrimaryReplicaRouter):
    def db_for_write(self, model, **hints):
        """
        1.获取来自请求开始前的 ctx. user_id
        """
        ctx = RequestContext.get_context()
        ctx.using = True
        ctx.extra[str(model)] = True
        # logger.debug(f"PrimaryReplicaRouterCtx ctx: {ctx}")
        return db_default


class TransactionPrimaryReplicaRouter(PrimaryReplicaRouter):
    """
    事物上下文：
        using 主库
    """

    def db_for_read(self, model, **hints):
        """
        读操作使用 主库
        如果用户使用了 using() Queryset._db 优先级最高，会拦截此处的db路由器
        """
        in_atomic_block = check_in_atomic_block()
        logger.debug(f"TransactionPrimaryReplicaRouter db_for_read in_atomic_block: {in_atomic_block}")
        if in_atomic_block:
            return db_default
        return super().db_for_read(model, **hints)

#
# class HashTransactionPrimaryReplicaRouter(TransactionPrimaryReplicaRouter):
#     """
#     使用一致性哈希来分配读请求到不同的读库。
#     单调读
#     """
#
#     def db_for_write(self, model, **hints):
#         """
#         Writes always go to primary.
#         """
#         ctx = RequestContext.get_context()
#         if not ctx.user_id:
#             return super().db_for_write(model, **hints)
#         RequestContext.update_context(extra={str(model): True}, orm_write=True)
#         logger.info(f"HashTransactionPrimaryReplicaRouter db_for_read ctx: {ctx} db: {db_default}")
#         return db_default
#
#     def db_for_read(self, model, **hints):
#         """
#         1.TransactionPrimaryReplicaRouter
#         2.同一个user_id, 一致性同一个从库
#         """
#         # todo 测试
#         ctx = RequestContext.get_context()
#         if not ctx.user_id:
#             db = super().db_for_read(model, **hints)
#             return db
#         db = db_read_hash_ring.get_node(ctx.user_id)
#         logger.info(f"HashTransactionPrimaryReplicaRouter db_for_read ctx: {ctx} db: {db}")
#         return db


