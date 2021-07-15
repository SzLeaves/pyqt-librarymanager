#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -- 数据库操作模块 -- #

import pyodbc

"""
-- connect() 数据库连接函数 --
server: 数据库地址 str
database: 准备连接的目标数据库 str
username: 数据库登录用户名 str
password: 数据库登录密码 str
"""


def connect():
    server = '172.17.0.2'
    database = 'BookDB'
    username = 'SA'
    password = 'mssqlASDF@'

    try:
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=' + server +
            ';DATABASE=' + database +
            ';UID=' + username +
            ';PWD=' + password
        )
    except ConnectionError as e:
        raise e

    # 返回查询游标
    return cnxn.cursor()


"""
-- dml 操作映射函数 --
sql: 预拼接的sql语句 str

select(): 执行select查询指令，返回结果集 list
execute(): 执行insert, update, delete操作指令，返回受影响的行数 int
version(): 返回数据库版本信息 str
"""


def select(sql):
    cur = connect()

    try:
        cur.execute(sql)
        # 取回结果集
        res = cur.fetchall()
    except RuntimeError as e:
        raise e
    finally:
        cur.close()

    # 返回查询结果集
    return res


def execute(sql):
    cur = connect()

    try:
        cur.execute(sql)
        affected = cur.rowcount
        # 提交事务并关闭数据库连接
        cur.commit()
    except RuntimeError as e:
        raise e
    finally:
        cur.close()

    # 返回影响的行数
    return affected


def version():
    return select('select @@version')[0][0]
