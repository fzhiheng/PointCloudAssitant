# -- coding: utf-8 --
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.QtWidgets import QHBoxLayout, QLineEdit

from format_transformation.FormatTrans import FormatTrans

# @Time : 2023/2/9 20:17
# @Author : Zhiheng Feng
# @File : main.py
# @Software : PyCharm
import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class Example(QMainWindow):

    def __init__(self):
        super(Example, self).__init__()
        # 窗口标题
        self.setWindowTitle('文件拖入')
        # 定义窗口大小
        self.resize(500, 400)
        self.textBrowser = QTextBrowser()
        self.setCentralWidget(self.textBrowser)
        # 不换行设置
        self.textBrowser.setLineWrapMode(0)
        # 调用Drops方法
        self.setAcceptDrops(True)
        # 设置字体
        font = QFont()
        font.setFamily("黑体")
        font.setPointSize(13)
        self.textBrowser.setFont(font)

    # 鼠标拖入事件
    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.textBrowser.setText('文件路径:\n' + os.path.dirname((e.mimeData().urls())[0].toLocalFile()))
        # 获取文件地址
        for path in e.mimeData().urls():
            print(os.path.abspath((path.toLocalFile())))





if __name__ == "__main__":
    app = QApplication(sys.argv)
    example = FormatTrans()
    example.show()
    sys.exit(app.exec_())


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     main_window = QMainWindow()
#     # layout = QHBoxLayout(main_window)
#     format_helper = FormatTrans(main_window)
#
#     # layout.addWidget(format_helper)
#     main_window.setCentralWidget(format_helper)
#     main_window.show()
#     sys.exit(app.exec())
