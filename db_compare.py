# _*_ coding: utf-8 _*_
# @Time    : 2018/6/1 下午1:54
# @Author  : 杨楚杰
# @File    : db_compare.py
# @license : Copyright(C), 安锋游戏
from base import compare

"""
    PostgreSQL 数据库表结构对比工具
"""

origin_db = {
    'host': '192.168.1.241',
    'port': 4453,
    'username': 'postgres',
    'password': '',
    'database': 'tianyan'
}

destination_db = {
    'host': '192.168.1.241',
    'port': 4453,
    'username': 'postgres',
    'password': '',
    'database': 'tianyan_5'
}


if __name__ == '__main__':
    print("PostgreSQL 数据库表结构对比开始 ...")
    compare(origin_db, destination_db)
    print("对比结束")
