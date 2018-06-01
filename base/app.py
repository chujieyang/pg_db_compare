# _*_ coding: utf-8 _*_
# @Time    : 2018/6/1 下午2:00
# @Author  : 杨楚杰
# @File    : app.py
# @license : Copyright(C), 安锋游戏
from base import pg_client


def db_table_list(db):
    query_sql = """
        SELECT tablename FROM pg_tables WHERE tablename LIKE 'ty_%' ORDER BY tablename;
    """
    table_list = db.query(query_sql)
    result = []
    for table in table_list:
        result.append(table['tablename'])
    return result


def compare_table_struct(origin_db, dest_db, table_name):
    struct_query_sql = """
        SELECT a.attname AS field, t.typname AS type, a.attlen AS length, a.atttypmod AS lengthvar,
        a.attnotnull AS notnull FROM pg_class c,pg_attribute a,pg_type t
        WHERE c.relname = '{table_name}' and a.attnum > 0 and a.attrelid = c.oid and a.atttypid = t.oid
        ORDER BY a.attname;
    """.format(table_name=table_name)
    origin_table_column_list = []
    dest_table_column_list = []
    origin_table_struct = origin_db.query(struct_query_sql)
    dest_table_struct = dest_db.query(struct_query_sql)
    for column in origin_table_struct:
        origin_table_column_list.append(column['field'])
    for column in dest_table_struct:
        dest_table_column_list.append(column['field'])
    in_origin_not_in_dest = list(set(origin_table_column_list).difference(set(dest_table_column_list)))
    in_dest_not_in_origin = list(set(dest_table_column_list).difference(set(origin_table_column_list)))
    if len(in_origin_not_in_dest) > 0:
        print("表名：%s 源表中存在，但目标表中不存在的列有：%s" % (table_name, in_origin_not_in_dest))
    if len(in_dest_not_in_origin) > 0:
        print("表名：%s 目标表中存在，但源表中不存在的列有：%s" % (table_name, in_dest_not_in_origin))


def compare(origin_db, dest_db):
    origin_db_client = pg_client(origin_db['host'], origin_db['port'], origin_db['database'],
                                 origin_db['username'], origin_db['password'])
    dest_db_client = pg_client(dest_db['host'], dest_db['port'], dest_db['database'],
                               dest_db['username'], dest_db['password'])

    origin_db_table_list = db_table_list(origin_db_client)
    dest_db_table_list = db_table_list(dest_db_client)
    in_origin_not_in_dest = list(set(origin_db_table_list).difference(set(dest_db_table_list)))
    in_dest_not_in_origin = list(set(dest_db_table_list).difference(set(origin_db_table_list)))
    if len(in_origin_not_in_dest) > 0:
        print("源库存在，但目标库中不存在的表有：%s" % in_origin_not_in_dest)
    if len(in_dest_not_in_origin) > 0:
        print("目标库中存在，但源库中不存在的表有：%s" % in_dest_not_in_origin)
    intersection_table_list = list(set(origin_db_table_list).intersection(set(dest_db_table_list)))
    for table_name in intersection_table_list:
        compare_table_struct(origin_db_client, dest_db_client, table_name)
