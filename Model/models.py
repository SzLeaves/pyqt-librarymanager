#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -- 数据模型定义模块 -- #

from Model.orm import Model

"""
-- 定义基本数据模型 --
self.table: 定义数据库表名
self.fields: 定义数据库列名
"""

# 读者信息表
class Readers(Model):
    def __init__(self, table):
        super().__init__(table)
        self.fields = ['id', 'name', 'gender', 'department', 'telephone', 'status']


# 图书信息表
class Books(Model):
    def __init__(self, table):
        super().__init__(table)
        self.fields = ['id', 'name', 'author', 'press', 'price']


# 借阅信息表
class Borrow(Model):
    def __init__(self, table):
        super().__init__(table)
        self.fields = ['reader_id', 'book_id', 'borrow_date', 'return_date']


# 登录用户信息表
class User(Model):
    def __init__(self, table):
        super().__init__(table)
        self.fields = ['id', 'name', 'password']
