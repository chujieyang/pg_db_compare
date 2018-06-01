# _*_ coding: utf-8 _*_
# @Time    : 2018/6/1 下午1:57
# @Author  : 杨楚杰
# @File    : untils.py
# @license : Copyright(C), 安锋游戏
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import SingletonThreadPool


class pg_client:
    def __init__(self, host, port, database, username, password):
        uri = "postgresql://{username}:{password}@{host}:{port}/{database}"\
            .format(host=host, port=port, database=database, username=username, password=password)
        self.engine = create_engine(uri, echo=False, pool_recycle=5, pool_size=1, poolclass=SingletonThreadPool)
        self.db_session = sessionmaker(autocommit=True, bind=self.engine)

    def query(self, sql):
        result = self.db_session().execute(sql).fetchall()
        return result
