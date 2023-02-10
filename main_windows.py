# -- coding: utf-8 --
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from format_transformation.FormatTrans import FormatTrans
from utils.Img2Video import Img2Video

# @Time : 2023/2/10 22:10
# @Author : Zhiheng Feng
# @File : main_windows.py
# @Software : PyCharm



class MyMainWindows(QMainWindow):
    def __init__(self, MAX_WORKERS=50):
        super().__init__()

        # 设置整体布局
        layout = QHBoxLayout()
        self.tab_windows = QTabWidget(self)
        self.tab_windows.setLayout(layout)
        self.setCentralWidget(self.tab_windows)


        # 格式转换工具
        self.format_widget = FormatTrans(self)
        self.tab_windows.addTab(self.format_widget, "格式转换")


        # 图片转视频工具
        self.img2video = Img2Video(self)
        self.tab_windows.addTab(self.img2video, "图片转视频")



