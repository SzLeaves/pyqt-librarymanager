#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -- 数据库对象映射模块 -- #

from Model.database import select, execute


class Model:
    def __init__(self, table=None):
        # 指定数据表名
        self.table = table

    """
    -- find_info 数据查询方法 --
    top: 限制返回行数量 int
    column: 查询列名 str
    where: 筛选条件 str
    order_by: 按指定列排序（默认升序） str
    sort_down: 指定降序排列 boolean
    """

    def findInfo(self, top=None, column='*', where=None, order_by=None, sort_down=False):
        if top:
            top = 'top %d' % top
        if where:
            where = 'where %s' % where

        if sort_down:
            order_by = 'order by ' + order_by + ' desc'

        table_name = 'from %s' % self.table

        sql_list = list(filter(lambda x: x is not None, [top, column, table_name, where, order_by]))

        # 补充必要参数
        sql_list.insert(0, 'select')

        # 拼接参数
        sql = ' '.join(sql_list)
        return select(sql)

    """
    -- save_info 数据保存方法 --
    column_list: 数据表定义的列名 list
    save_fields: 保存的数据 dict
    """

    def saveInfo(self, *column_list, **save_fields):
        # 检查列名是否与插入的数据类型一致
        for k, v in zip(column_list, list(save_fields.keys())):
            if k != v:
                raise TypeError('different type columns')

        args = '%s(%s)' % (self.table, ','.join(column_list))

        fields = list()
        for index in save_fields.values():
            index = "'%s'" % index
            fields.append(index)

        values = 'values(%s)' % ','.join(fields)

        sql_list = ['insert into', args, values]
        sql = ' '.join(sql_list)
        return execute(sql)

    """
    -- update_info 数据更新方法 --
    args: 指定更新列名参数 str
    where: 筛选条件 str
    """

    def updateInfo(self, args, where=None):
        args = '%s set %s' % (self.table, ''.join(args))

        if where:
            where = 'where %s' % where
            sql_list = ['update', args, where]
        else:
            sql_list = ['update', args]

        sql = ' '.join(sql_list)
        return execute(sql)

    """
    -- delete_info 数据删除方法 --
    where: 筛选条件 str
    """

    def deleteInfo(self, where=None):
        if where:
            where = 'where %s' % where
            sql_list = ['delete from', self.table, where]
        else:
            sql_list = ['delete from', self.table]

        sql = ' '.join(sql_list)
        return execute(sql)
