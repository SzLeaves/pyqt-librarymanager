#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -- 系统主界面控制器 -- #


from datetime import datetime, timedelta

from PyQt5 import QtCore, Qt
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

from Model.database import version
from Model.models import *

# 加载系统主题配置路径 (on linux)
# QtCore.QCoreApplication.addLibraryPath("/usr/lib/qt/plugins")

# 设置布局文件
UiFile, _tmp = loadUiType('../View/main.ui')
del _tmp


class MainWindow(QMainWindow, UiFile):
    def __init__(self, user_id, loginWindow):
        QMainWindow.__init__(self)

        # 初始化数据模型
        self.user_id = user_id
        self.readers_table = Readers('reader_info')
        self.books_table = Books('book_info')
        self.borrow_table = Borrow('borrow_info')
        self.users_table = User('users_info')

        # 设置基本布局
        self.initLayout()
        self.loginWindow = loginWindow

        # 初始化信号处理连接器
        self.handleButtons()

    # -- 初始化基础布局 -- #
    def initLayout(self):
        self.setupUi(self)
        self.menuTab.tabBar().setVisible(False)
        self.currentUserId.setText(self.user_id)
        self.openReaderInfoTab()  # 切换至第一页

    # -- 信号处理连接器 -- #
    def handleButtons(self):
        # 页面切换
        self.readerInfoButton.clicked.connect(self.openReaderInfoTab)
        self.bookInfoButton.clicked.connect(self.openBookInfoTab)
        self.borrowInfoButton.clicked.connect(self.openBorrowInfoTab)
        self.systemInfoButton.clicked.connect(self.openSystemInfoTab)

        # 读者信息模块功能
        self.readerQueryExec.clicked.connect(self.queryReader)
        self.readerUpdateExec.clicked.connect(self.updateReader)
        self.readerInsertExec.clicked.connect(self.insertReader)
        self.readerDeleteQuery.clicked.connect(self.deleteReader)
        self.readerDeleteExec.clicked.connect(self.deleteReaderExec)

        # 图书信息模块功能
        self.bookQueryExec.clicked.connect(self.queryBook)
        self.bookUpdateExec.clicked.connect(self.updateBook)
        self.bookInsertExec.clicked.connect(self.insertBook)
        self.bookDeleteQuery.clicked.connect(self.deleteBook)
        self.bookDeleteExec.clicked.connect(self.deleteBookExec)

        # 借阅模块功能
        self.borrowQueryExec.clicked.connect(self.queryBorrow)
        self.borrowBookQuery.clicked.connect(self.borrowBook)
        self.bookBorrowExec.clicked.connect(self.borrowBookExec)
        self.reutrnBookQuery.clicked.connect(self.returnBook)
        self.reutrnBorrowExec.clicked.connect(self.returnBookExec)

        # 系统设置模块功能
        self.updateUserNameExec.clicked.connect(self.updateUserName)
        self.updateUserPasswordExec.clicked.connect(self.updateUserPasswd)
        self.exitLoginExec.clicked.connect(self.exitLogin)

    # -- 槽函数 -- #

    """
    -- 切换页面 --
    """

    def openReaderInfoTab(self):
        # 跳转至指定目录页
        self.menuTab.setCurrentIndex(0)
        # 切换至第一页
        self.readerInfoTab.setCurrentIndex(0)

        self.statusBar.showMessage('')
        self.readerDeleteConfirm.setVisible(False)
        self.queryTableAll(self.readers_table)

    def openBookInfoTab(self):
        # 跳转至指定目录页
        self.menuTab.setCurrentIndex(1)
        # 切换至第一页
        self.bookInfoTab.setCurrentIndex(0)

        self.statusBar.showMessage('')
        self.bookDeleteConfirm.setVisible(False)
        self.queryTableAll(self.books_table)

    def openBorrowInfoTab(self):
        # 跳转至指定目录页
        self.menuTab.setCurrentIndex(2)
        # 切换至第一页
        self.borrowInfoTab.setCurrentIndex(0)

        self.statusBar.showMessage('')
        self.borrowBookConfirm.setVisible(False)
        self.returnBookConfirm.setVisible(False)
        self.queryTableAll(self.borrow_table)

    def openSystemInfoTab(self):
        # 跳转至指定目录页
        self.menuTab.setCurrentIndex(3)
        self.statusBar.showMessage('')
        self.showSystemInfo()

    # 退出登录
    def exitLogin(self):
        self.close()

        # 设置登录窗口属性
        self.loginWindow.loginStatusBar.setText('')  # 清空状态栏
        self.loginWindow.userIdText.setText('')
        self.loginWindow.userPasswordText.setText('')
        # 第一行文本框获取焦点
        self.loginWindow.userIdText.setFocus()
        # 显示登录窗口
        self.loginWindow.show()

    """
    -- 信息查询 --
    """

    # 将信息输出在指定表格上
    def showTableInfo(self, data, table_widget):
        # 获取数据表大小
        row_num = len(data)

        # 设置显示表格格式
        table_widget.setRowCount(row_num)

        # 设置单元格禁止编辑
        table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        if data:
            for row, index in enumerate(data):
                for col, item in enumerate(index):
                    table_widget.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
        else:
            self.statusBar.showMessage('未查询到对应信息')

    def queryTableAll(self, table):
        data = table.findInfo()

        if table == self.readers_table:
            self.showTableInfo(data, self.readerQueryTable)
        if table == self.books_table:
            self.showTableInfo(data, self.bookQueryTable)
        if table == self.borrow_table:
            self.showTableInfo(data, self.borrowQueryTable)

    # 显示系统版本信息和用户信息
    def showSystemInfo(self):
        self.databaseVersionText.setText(version())
        self.graphicVersionText.setText(Qt.QT_VERSION_STR)

        self.userIdLabel.setText(self.user_id)
        self.userNameLabel.setText(self.users_table.findInfo(column='name', where="id='%s'" % self.user_id)[0][0])
        self.updateInfoShow.setText('')

    # 查询指定用户信息
    def queryReader(self):
        query_args = list()
        is_sort = False
        options_id = self.readerQueryOptions.currentIndex()
        if options_id:
            if '借阅证号' == self.readerQueryOptions.itemText(options_id):
                query_args.append(self.readers_table.fields[0])
            if '姓名' == self.readerQueryOptions.itemText(options_id):
                query_args.append(self.readers_table.fields[1])
            if '部门' == self.readerQueryOptions.itemText(options_id):
                query_args.append(self.readers_table.fields[3])
            if '联系方式' == self.readerQueryOptions.itemText(options_id):
                query_args.append(self.readers_table.fields[4])

            query_args.append("like '%%%s%%'" % self.readerQueryText.toPlainText())

            if self.readerQuerySort.isChecked():
                sort_column = query_args[0]
                is_sort = True
            else:
                sort_column = None

            data = self.readers_table.findInfo(where=' '.join(query_args), order_by=sort_column, sort_down=is_sort)

        else:
            data = self.readers_table.findInfo()

        self.statusBar.showMessage('信息查询成功')
        self.showTableInfo(data, self.readerQueryTable)

    # 查询指定图书信息
    def queryBook(self):
        query_args = list()
        is_sort = False
        options_id = self.bookQueryOptions.currentIndex()
        if options_id:
            if '图书编号' == self.bookQueryOptions.itemText(options_id):
                query_args.append(self.books_table.fields[0])
            if '书名' == self.bookQueryOptions.itemText(options_id):
                query_args.append(self.books_table.fields[1])
            if '作者' == self.bookQueryOptions.itemText(options_id):
                query_args.append(self.books_table.fields[2])
            if '出版社' == self.bookQueryOptions.itemText(options_id):
                query_args.append(self.books_table.fields[3])
            if '价格' == self.bookQueryOptions.itemText(options_id):
                query_args.append(self.books_table.fields[4])

            query_args.append("like '%%%s%%'" % self.bookQueryText.toPlainText())

            if self.bookQuerySort.isChecked():
                sort_column = query_args[0]
                is_sort = True
            else:
                sort_column = None

            data = self.books_table.findInfo(where=' '.join(query_args), order_by=sort_column, sort_down=is_sort)

        else:
            data = self.books_table.findInfo()

        self.statusBar.showMessage('信息查询成功')
        self.showTableInfo(data, self.bookQueryTable)

    # 查询指定借阅信息
    def queryBorrow(self):
        query_args = list()
        is_sort = False
        options_id = self.borrowQueryOptions.currentIndex()
        if options_id:
            if '借阅证号' == self.borrowQueryOptions.itemText(options_id):
                query_args.append(self.borrow_table.fields[0])
            if '图书编号' == self.borrowQueryOptions.itemText(options_id):
                query_args.append(self.borrow_table.fields[1])
            if '借阅日期' == self.borrowQueryOptions.itemText(options_id):
                query_args.append(self.borrow_table.fields[2])
            if '归还日期' == self.borrowQueryOptions.itemText(options_id):
                query_args.append(self.borrow_table.fields[3])

            query_args.append("like '%%%s%%'" % self.borrowQueryText.toPlainText())

            if self.borrowQuerySort.isChecked():
                sort_column = query_args[0]
                is_sort = True
            else:
                sort_column = None

            data = self.borrow_table.findInfo(where=' '.join(query_args), order_by=sort_column, sort_down=is_sort)

        else:
            data = self.borrow_table.findInfo()

        self.statusBar.showMessage('信息查询成功')
        self.showTableInfo(data, self.borrowQueryTable)

    """
    -- 信息修改 --
    """

    # 更新读者信息
    def updateReader(self):
        update_args = list()

        # 查询需要修改的读者信息
        update_id = "%s" % self.readerUpdateId.toPlainText()
        if not self.readers_table.findInfo(where="id='%s'" % update_id):
            self.statusBar.showMessage('未找到指定的用户')
            return None

        options_id = self.readerUpdateOptions.currentIndex()
        if options_id:
            if '姓名' == self.readerUpdateOptions.itemText(options_id):
                update_args.append(self.readers_table.fields[1])
            if '性别' == self.readerUpdateOptions.itemText(options_id):
                update_args.append(self.readers_table.fields[2])
            if '部门' == self.readerUpdateOptions.itemText(options_id):
                update_args.append(self.readers_table.fields[3])
            if '联系方式' == self.readerUpdateOptions.itemText(options_id):
                update_args.append(self.readers_table.fields[4])

            update_info = "= '%s'" % self.readerUpdateText.toPlainText()
            if update_info == '':
                self.statusBar.showMessage('更改的信息不能为空')
                return None
            update_args.append(update_info)

            # 执行修改，返回影响的行数
            affected = self.readers_table.updateInfo(' '.join(update_args), where="id='%s'" % update_id)

            # 进行修改后数据的显示
            data = self.readers_table.findInfo(where="id='%s'" % update_id)
            self.showTableInfo(data, self.readerUpdateTable)
            self.statusBar.showMessage('修改成功，影响%s行' % affected)
            self.queryTableAll(self.readers_table)

        else:
            self.statusBar.showMessage('请选择需要更改的字段')

    # 添加读者信息
    def insertReader(self):
        insert_args = dict()
        insert_args['id'] = self.readerInsertId.toPlainText()
        insert_args['name'] = self.readerInsertName.toPlainText()
        insert_args['gender'] = self.readerInsertGender.currentText()
        insert_args['department'] = self.readerInsertPart.toPlainText()
        insert_args['telephone'] = self.readerInsertTel.toPlainText()
        insert_args['status'] = str(self.readerInsertStatus.currentIndex())

        for index in insert_args.values():
            if index == '':
                self.statusBar.showMessage('信息不能为空')
                return None

        id_list = self.readers_table.findInfo(column='id')
        for index in id_list:
            if insert_args['id'] == index[0]:
                self.statusBar.showMessage('新增的借阅证号已存在')
                return None

        # 执行修改，返回影响的行数
        affected = self.readers_table.saveInfo(*self.readers_table.fields, **insert_args)
        # 进行修改后数据的显示
        data = self.readers_table.findInfo(where="id='%s'" % insert_args['id'])
        self.showTableInfo(data, self.readerInsertTable)
        self.statusBar.showMessage('修改成功，影响%s行' % affected)
        self.queryTableAll(self.readers_table)

    # 更新图书信息
    def updateBook(self):
        update_args = list()

        # 查询需要修改的图书信息
        update_id = "%s" % self.bookUpdateId.toPlainText()
        if not self.books_table.findInfo(where="id='%s'" % update_id):
            self.statusBar.showMessage('未找到指定的图书')
            return None

        options_id = self.bookUpdateOptions.currentIndex()
        if options_id:
            if '书名' == self.bookUpdateOptions.itemText(options_id):
                update_args.append(self.books_table.fields[1])
            if '作者' == self.bookUpdateOptions.itemText(options_id):
                update_args.append(self.books_table.fields[2])
            if '出版社' == self.bookUpdateOptions.itemText(options_id):
                update_args.append(self.books_table.fields[3])
            if '价格' == self.bookUpdateOptions.itemText(options_id):
                update_args.append(self.books_table.fields[4])

            update_info = "= '%s'" % self.bookUpdateText.toPlainText()
            if update_info == '':
                self.statusBar.showMessage('更改的信息不能为空')
                return None
            update_args.append(update_info)

            # 执行修改，返回影响的行数
            affected = self.books_table.updateInfo(' '.join(update_args), where="id='%s'" % update_id)

            # 进行修改后数据的显示
            data = self.books_table.findInfo(where="id='%s'" % update_id)
            self.showTableInfo(data, self.bookUpdateTable)
            self.statusBar.showMessage('修改成功，影响%s行' % affected)
            self.queryTableAll(self.books_table)

        else:
            self.statusBar.showMessage('请选择需要更改的字段')

    # 添加图书信息
    def insertBook(self):
        insert_args = dict()
        insert_args['id'] = self.bookInsertId.toPlainText()
        insert_args['name'] = self.bookInsertName.toPlainText()
        insert_args['author'] = self.bookInsertAuthor.toPlainText()
        insert_args['press'] = self.bookInsertPress.toPlainText()
        insert_args['price'] = self.bookInsertPrice.toPlainText()

        for index in insert_args.values():
            if index == '':
                self.statusBar.showMessage('信息不能为空')
                return None

        id_list = self.books_table.findInfo(column='id')
        for index in id_list:
            if insert_args['id'] == index[0]:
                self.statusBar.showMessage('新增的图书编号已存在')
                return None

        # 执行修改，返回影响的行数
        affected = self.books_table.saveInfo(*self.books_table.fields, **insert_args)
        # 进行修改后数据的显示
        data = self.books_table.findInfo(where="id='%s'" % insert_args['id'])
        self.showTableInfo(data, self.bookInsertTable)
        self.statusBar.showMessage('修改成功，影响%s行' % affected)
        self.queryTableAll(self.books_table)

    # 删除读者信息
    def deleteReader(self):
        delete_id = self.readerDeleteId.toPlainText()
        id_list = self.readers_table.findInfo(column='id')
        for index in id_list:
            if delete_id == index[0]:
                # 显示确认删除框
                self.readerDeleteConfirm.setVisible(True)
                data = self.readers_table.findInfo(where="id='%s'" % index[0])
                self.showTableInfo(data, self.readerDeleteTable)
                return None

        self.statusBar.showMessage('未找到指定的读者')
        self.readerDeleteConfirm.setVisible(False)

    def deleteReaderExec(self):
        delete_id = self.readerDeleteId.toPlainText()
        if delete_id != '' and self.readerDeleteOptions.currentIndex():
            # 进行删除操作
            affected = self.readers_table.deleteInfo(where="id='%s'" % delete_id)

            # 进行数据展示
            data = self.readers_table.findInfo(where="id='%s'" % delete_id)
            self.showTableInfo(data, self.readerDeleteTable)
            self.statusBar.showMessage('删除成功，影响%s行' % affected)
            self.queryTableAll(self.readers_table)

        else:
            self.statusBar.showMessage('操作已取消')
            self.readerDeleteConfirm.setVisible(False)

    # 删除图书信息
    def deleteBook(self):
        delete_id = self.bookDeleteId.toPlainText()
        id_list = self.books_table.findInfo(column='id')
        for index in id_list:
            if delete_id == index[0]:
                # 显示确认删除框
                self.bookDeleteConfirm.setVisible(True)
                data = self.books_table.findInfo(where="id='%s'" % index[0])
                self.showTableInfo(data, self.bookDeleteTable)
                return None

        self.statusBar.showMessage('未找到指定的图书')
        self.bookDeleteConfirm.setVisible(False)

    def deleteBookExec(self):
        delete_id = self.bookDeleteId.toPlainText()
        if delete_id != '' and self.bookDeleteOptions.currentIndex():
            # 进行删除操作
            affected = self.books_table.deleteInfo(where="id='%s'" % delete_id)

            # 进行数据展示
            data = self.books_table.findInfo(where="id='%s'" % delete_id)
            self.showTableInfo(data, self.bookDeleteTable)
            self.statusBar.showMessage('删除成功，影响%s行' % affected)
            self.queryTableAll(self.books_table)

        else:
            self.statusBar.showMessage('操作已取消')
            self.bookDeleteConfirm.setVisible(False)

    # 借阅操作
    def borrowBook(self):
        reader_id = self.borrowReaderText.toPlainText()
        book_id = self.borrowBookText.toPlainText()

        reader_id_list = self.readers_table.findInfo(column='id')
        book_id_list = self.books_table.findInfo(column='id')

        for reader_index in reader_id_list:
            if reader_id == reader_index[0]:
                for book_index in book_id_list:
                    if book_id == book_index[0]:
                        # 进行数据展示
                        self.borrowBookConfirm.setVisible(True)

                        data = self.books_table.findInfo(where="id='%s'" % book_id)
                        self.showTableInfo(data, self.borrowBookTable)
                        return None

                self.statusBar.showMessage('未找到对应的图书信息')
                self.borrowBookConfirm.setVisible(False)
                return None

        self.statusBar.showMessage('未找到对应的读者')
        self.borrowBookConfirm.setVisible(False)
        return None

    def borrowBookExec(self):
        reader_id = self.borrowReaderText.toPlainText()
        book_id = self.borrowBookText.toPlainText()

        if reader_id and book_id and self.bookBorrowOptions.currentIndex():
            insert_args = dict()
            insert_args['reader_id'] = reader_id
            insert_args['book_id'] = book_id
            # 计算借阅日期与待归还日期，默认时效30天
            insert_args['borrow_date'] = datetime.now().strftime('%Y-%m-%d')
            insert_args['return_date'] = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')

            # 检查重复借阅
            reader_id_list = self.borrow_table.findInfo(column='reader_id')
            book_id_list = self.borrow_table.findInfo(column='book_id')
            for reader_index, book_index in zip(reader_id_list, book_id_list):
                if insert_args['reader_id'] == reader_index[0] and insert_args['book_id'] == book_index[0]:
                    self.statusBar.showMessage('本书已被该读者借阅过，不能重复借阅')
                    return None

            self.borrow_table.saveInfo(*self.borrow_table.fields, **insert_args)
            data = self.borrow_table.findInfo(
                where="reader_id='%s' and book_id='%s'" % (insert_args['reader_id'], insert_args['book_id']))

            # 设置显示表格新格式
            self.borrowBookTable.setColumnCount(4)
            self.borrowBookTable.setHorizontalHeaderLabels(['借阅证号', '图书编号', '借阅日期', '待归还日期'])

            self.showTableInfo(data, self.borrowBookTable)
            self.statusBar.showMessage('借阅成功')
            # 刷新借阅表显示
            self.queryTableAll(self.borrow_table)

        else:
            self.statusBar.showMessage('操作已取消')
            self.borrowBookConfirm.setVisible(False)

    # 归还操作
    def returnBook(self):
        reader_id = self.returnReaderText.toPlainText()
        book_id = self.returnBookText.toPlainText()

        reader_id_list = self.borrow_table.findInfo(column='reader_id')
        book_id_list = self.borrow_table.findInfo(column='book_id')

        for reader_index in reader_id_list:
            if reader_id == reader_index[0]:
                for book_index in book_id_list:
                    if book_id == book_index[0]:
                        # 进行数据展示
                        self.returnBookConfirm.setVisible(True)

                        data = self.borrow_table.findInfo(
                            where="reader_id='%s' and book_id='%s'" % (reader_id, book_id))
                        self.showTableInfo(data, self.returnBookTable)
                        return None

                self.statusBar.showMessage('未找到对应的图书信息')
                self.returnBookConfirm.setVisible(False)
                return None

        self.statusBar.showMessage('未找到对应的读者')
        self.returnBookConfirm.setVisible(False)
        return None

    def returnBookExec(self):
        reader_id = self.returnReaderText.toPlainText()
        book_id = self.returnBookText.toPlainText()
        is_return = True  # 图书是否已归还标记

        # 检查归还记录
        reader_id_list = self.borrow_table.findInfo(column='reader_id')
        book_id_list = self.borrow_table.findInfo(column='book_id')
        for reader_index, book_index in zip(reader_id_list, book_id_list):
            if reader_id == reader_index[0] and book_id == book_index[0]:
                is_return = False
                break

        if not is_return and reader_id and book_id and self.returnBorrowOptions.currentIndex():
            affected = self.borrow_table.deleteInfo(where="reader_id='%s' and book_id='%s'" % (reader_id, book_id))

            data = self.borrow_table.findInfo(
                where="reader_id='%s' and book_id='%s'" % (reader_id, book_id))
            self.showTableInfo(data, self.returnBookTable)
            self.statusBar.showMessage('归还成功，影响%s行' % affected)
            # 刷新借阅表显示
            self.queryTableAll(self.borrow_table)

        else:
            self.statusBar.showMessage('操作已取消')
            self.returnBookConfirm.setVisible(False)

    # 帐号设置操作
    def updateUserName(self):
        user_name = self.updateUserNameText.text()

        if user_name:
            self.users_table.updateInfo(args="name='%s'" % user_name, where="id='%s'" % self.user_id)
            self.userNameLabel.setText(user_name)
            self.updateInfoShow.setText("修改成功！\n\n当前用户ID：%s\n当前用户名：%s\n当前用户密码：%s" %
                                        (self.user_id, user_name,
                                         self.users_table.findInfo(
                                             column='password', where="id='%s'" % self.user_id)[0][0]))
        else:
            self.statusBar.showMessage('请输入需要修改的用户名信息')

    def updateUserPasswd(self):
        user_passwd = self.updateUserPasswdText.text()

        if user_passwd:
            self.users_table.updateInfo(args="password='%s'" % user_passwd, where="id='%s'" % self.user_id)
            self.updateInfoShow.setText("修改成功！\n\n当前用户ID：%s\n当前用户名：%s\n当前用户密码：%s" %
                                        (self.user_id, self.userNameLabel.text(),
                                         self.users_table.findInfo(
                                             column='password', where="id='%s'" % self.user_id)[0][0]))
        else:
            self.statusBar.showMessage('请输入需要修改的用户密码信息')
