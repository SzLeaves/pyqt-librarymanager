#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -- 系统启动入口 -- #


import sys

from PyQt5.QtWidgets import QApplication

from Controller.login import LoginWindow


def app_run():
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    # 启动窗口进程
    sys.exit(app.exec_())


if __name__ == '__main__':
    app_run()
