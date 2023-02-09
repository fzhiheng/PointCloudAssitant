# -- coding: utf-8 --
import os
import numpy as np
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from .generate_ply import npy2ply


# @Time : 2023/2/9 21:03
# @Author : Zhiheng Feng
# @File : FormatTrans.py
# @Software : PyCharm

class FormatTrans(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('拖入文件')
        self.setAcceptDrops(True)
        self.textBrowser = QTextBrowser()
        self.setCentralWidget(self.textBrowser)


        # self.textBrowser.setLineWrapMode()
        # 设置字体
        font = QFont()
        font.setFamily("黑体")
        font.setPointSize(11)
        self.textBrowser.setFont(font)


    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        for input_path in e.mimeData().urls():
            input_path = os.path.abspath((input_path.toLocalFile()))
            print(input_path)
            if os.path.isfile(input_path):
                self.textBrowser.clear()
                self.textBrowser.setText(f'trans... {os.path.basename(input_path)}')
                self.format_trans(input_path)
            elif os.path.isdir(input_path):
                for path in input_path:
                    if path.endwiths('.npy'):
                        self.textBrowser.clear()
                        self.textBrowser.setText(f'trans... {os.path.basename(input_path)}')
                        npy2ply(path)


    def format_trans(self, input_path, out_path=None):
        if not out_path:
            dirname = os.path.dirname(input_path)
            name = os.path.splitext(input_path)[0]
            out_path = os.path.join(dirname, f"{name}.ply")
            print(out_path)
        color = np.random.randint(0, 255, (3))
        npy2ply(input_path, out_path, color)







