#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -- 系统登录界面控制器 -- #


from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

from Controller.main import MainWindow
from Model.models import User

# 加载系统主题配置路径 (on linux)
# QtCore.QCoreApplication.addLibraryPath("/usr/lib/qt/plugins")

# 设置布局文件
UiFile, _tmp = loadUiType('../View/login.ui')
del _tmp


class LoginWindow(QMainWindow, UiFile):
    def __init__(self):
        QMainWindow.__init__(self)
        self.users_table = User('users_info')
        self.initLayout()

    # 初始化主登录界面
    def initLayout(self):
        self.setupUi(self)
        self.loginStatusBar.setText('')  # 清空状态栏

        # 绑定按钮事件
        self.loginExec.clicked.connect(self.queryInfo)
        self.exitExec.clicked.connect(self.exitSystem)

        # 第一行文本框获取焦点
        self.userIdText.setFocus()

    # 登录按钮-槽函数
    def queryInfo(self):
        user_id = self.userIdText.text()
        user_passwd = self.userPasswordText.text()

        if user_id and user_passwd:
            data = self.users_table.findInfo(column='id, password')
            for index in data:
                if user_id == index[0] and user_passwd == index[1]:
                    self.mainWindow = MainWindow(user_id, self)
                    self.close()  # 关闭当前窗口

                    # 设置主界面居中显示
                    size = self.mainWindow.frameGeometry()
                    size.moveCenter(QDesktopWidget().availableGeometry().center())
                    self.mainWindow.move(size.topLeft())

                    self.mainWindow.show()
                    return None

            self.loginStatusBar.setText('用户名或密码不正确')
            return None

        else:
            self.loginStatusBar.setText('请输入用户名和密码')

    # 退出系统-槽函数
    def exitSystem(self):
        self.close()
