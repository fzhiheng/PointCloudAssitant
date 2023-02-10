# -- coding: utf-8 --
import os
import glob
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from typing import List

from concurrent import futures
from .generate_ply import npy2ply


# @Time : 2023/2/9 21:03
# @Author : Zhiheng Feng
# @File : FormatTrans.py
# @Software : PyCharm

# 使用线程处理
class WorkThread(QThread):
    signals = pyqtSignal(str)  # 定义信号对象,传递值为str类型，使用int，可以为int类型
    process = pyqtSignal(str)

    def __init__(self, parent, paths: List[str], save_dir=None, MAX_WORKERS=50):  # 向线程中传递参数，以便在run方法中使用
        super().__init__(parent)
        self.paths = paths
        self.save_dir = save_dir
        self.MAX_WORKERS = MAX_WORKERS

    # def __del__(self):
    #     self.wait()

    def run(self):  # 重写run方法
        self.process_many(self.paths)

    # 多线程处理文件夹
    def process_many(self, input_paths: List[str]):
        for i, path in enumerate(input_paths):
            self.process_one(path, self.save_dir)
            self.process.emit(str(i))
        self.signals.emit(f'finish!')  # 发射信号，str类型数据，内容为需要传递的数据
        # workers = min(len(input_paths), self.MAX_WORKERS)
        # with futures.ThreadPoolExecutor(workers) as exector:
        #     exector.map(self.process_one, input_paths)

    # 默认在源文件中生成转换文件
    def process_one(self, input_path, out_root=None):
        filepath, fullflname = os.path.split(input_path)
        name = os.path.splitext(fullflname)[0]
        if not out_root:
            out_path = os.path.join(filepath, f"{name}.ply")
        else:
            out_path = os.path.join(out_root, f"{name}.ply")
        color = np.random.randint(0, 255, (3))
        npy2ply(input_path, out_path, color)


class FormatTrans(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('拖入文件')
        self.setAcceptDrops(True)

        # 用于显示当前正在处理的文件或者文件夹
        self.textBrowser = QTextBrowser()
        font = QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.textBrowser.setFont(font)

        # 用于选择转换的窗口
        self.choose_button = QPushButton("保存路径", self)
        self.choose_button.clicked.connect(self.choose_save_path)
        # 确认转换
        self.confirm_button = QPushButton("开始")

        layout = QHBoxLayout()
        # self.layout.addWidget(self.textBrowser,0,0,1,2)
        layout.addWidget(self.choose_button)
        layout.addWidget(self.confirm_button)

        # 进度条设置
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(50, 50, 210, 25)
        self.pbar.setValue(0)

        layout2 = QVBoxLayout(self)
        layout2.addWidget(self.textBrowser, 5)
        layout2.addWidget(self.pbar, 1)
        layout2.addLayout(layout, 1)

        self.widget = QWidget(self)
        self.widget.setLayout(layout2)
        self.setCentralWidget(self.widget)

        self.need_process_path = None
        self.save_dir = None

    def choose_save_path(self):
        dialog = QFileDialog(self)
        self.save_dir = dialog.getExistingDirectory()


    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()


    def dropEvent(self, event):
        for input_path in event.mimeData().urls():
            input_path = os.path.abspath((input_path.toLocalFile()))
            self.textBrowser.setText(f'processing... {input_path}')
            need_process_paths = []
            file_root = ""
            if os.path.isfile(input_path) and input_path.endswith('.npy'):
                need_process_paths = [input_path]
                file_root,_ = os.path.split(input_path)
            elif os.path.isdir(input_path):
                need_process_paths = glob.glob(os.path.join(input_path, '*.npy'))
                file_root = input_path

            if not self.save_dir:
                self.save_dir = file_root + '_trans_ply'
                os.makedirs(self.save_dir,exist_ok=True)

            t = WorkThread(self, need_process_paths, self.save_dir)
            t.signals.connect(self.textBrowser.setText)
            t.process.connect(self.call_backlog)
            try:
                t.start()
            except Exception as e:
                print(e)
            finally:
                self.save_dir = None
                self.call_backlog(0)


    def call_backlog(self, msg):
        self.pbar.setValue(int(msg))  # 将线程的参数传入进度条

    def process_many(self, input_paths: List[str]):
        workers = min(len(input_paths), self.MAX_WORKERS)
        with futures.ThreadPoolExecutor(workers) as exector:
            exector.map(self.process_one, input_paths)

    # 默认在源文件中生成转换文件
    def process_one(self, input_path, out_path=None):
        if not out_path:
            dirname = os.path.dirname(input_path)
            name = os.path.splitext(input_path)[0]
            out_path = os.path.join(dirname, f"{name}.ply")
        color = np.random.randint(25, 255, (3))
        npy2ply(input_path, out_path, color)
