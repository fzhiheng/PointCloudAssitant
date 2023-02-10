# -- coding: utf-8 --
import os
import glob
import numpy as np
import cv2
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from typing import List

from concurrent import futures


# @Time : 2023/2/10 22:07
# @Author : Zhiheng Feng
# @File : Img2Video.py
# @Software : PyCharm

class WorkThread(QThread):
    signals = pyqtSignal(str)  # 定义信号对象,传递值为str类型，使用int，可以为int类型
    process = pyqtSignal(str)

    def __init__(self, parent, img_dir: str, save_path, fps):  # 向线程中传递参数，以便在run方法中使用
        super().__init__(parent)
        self.img_dir = img_dir
        self.save_apth = save_path
        self.fps = fps

    def run(self):  # 重写run方法
        img_list = os.listdir(self.img_dir)
        img_list = sorted(img_list)
        img = cv2.imread(os.path.join(self.img_dir, img_list[0]))
        H, W, C = img.shape

        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        videoWriter = cv2.VideoWriter(self.save_apth, fourcc, self.fps, (W, H))
        for i, img_name in enumerate(img_list):
            frame = cv2.imread(os.path.join(self.img_dir, img_name))
            videoWriter.write(frame)
            self.process.emit(str(i))

        videoWriter.release()
        self.signals.emit('finish!')


class Img2Video(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

        self.fps = 0
        self.img_dir = ""
        self.times_path = ""

        # 用于选图片文件夹的按钮
        self.choose_img_button = QPushButton("选择文件夹", self)
        self.choose_img_button.clicked.connect(self.choose_img_dir)

        # 用于选时间戳的按钮
        self.choose_times_button = QPushButton("设置时间戳", self)
        self.choose_times_button.clicked.connect(self.choose_times_path)

        # 确认按钮
        self.confirm_button = QPushButton("转换开始", self)
        self.confirm_button.clicked.connect(self.begin_task)

        # 取消按钮
        self.cancal_button = QPushButton("取消转换", self)
        self.cancal_button.clicked.connect(self.reset)

        # 显示选中的图片文件夹与时间戳文件夹
        self.show_imgs = QLabel(self)
        self.show_times = QLabel(self)
        self.show_imgs.setFrameShape(QFrame.Box)
        self.show_imgs.setStyleSheet('border-width: 1px;border-style: solid;border-color: rgb(255, 170, 0);')

        self.show_times.setFrameShape(QFrame.Box)
        self.show_times.setStyleSheet('border-width: 1px;border-style: solid;border-color: rgb(255, 170, 0);')

        # 进度条设置
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(50, 50, 210, 25)
        self.pbar.setValue(0)

        # 设置布局
        layout = QGridLayout(self)
        layout.addWidget(self.choose_img_button, 0, 0, 1, 1)
        layout.addWidget(self.show_imgs, 0, 1, 1, 2)
        layout.addWidget(self.choose_times_button, 1, 0, 1, 1)
        layout.addWidget(self.show_times, 1, 1, 1, 2)
        layout.addWidget(self.confirm_button, 2, 0, 1, 1)
        layout.addWidget(self.cancal_button, 2, 2, 1, 1)
        layout.addWidget(self.pbar, 3, 0, 1, 3)

    def choose_img_dir(self):
        dialog = QFileDialog(self)
        self.img_dir = dialog.getExistingDirectory()
        self.show_info()

    def choose_times_path(self):
        question = QMessageBox()
        question.setIcon(QMessageBox.Information)
        question.setWindowTitle('提示')
        question.setText("选择时间戳文件或输入fps")
        question.addButton("选择文件", QMessageBox.YesRole)
        question.addButton("输入fps", QMessageBox.NoRole)

        api = question.exec_()
        if api == QMessageBox.YesRole:
            dialog = QFileDialog(self)
            self.times_path = dialog.getOpenFileUrl()[0].toLocalFile()
            self.show_info()
            if os.path.exists(self.times_path):
                with open(self.times_path) as fp:
                    lines = fp.readlines()
                    final = lines[-1].strip()
                    fps = float(final) / len(lines)
                    fps = int(fps)
                    self.fps = fps
                    print(self.fps)
        elif api == QMessageBox.NoRole:
            i, okPressed = QInputDialog.getInt(self, "输入fps", "fps:", 10, 0, 1000, 1)
            if okPressed:
                self.fps = i
                self.show_info()
        else:
            return

    def begin_task(self):
        if not os.path.exists(self.img_dir):
            QMessageBox.warning(self,"警告", ""f"文件夹{self.img_dir}不存在")
            return
        if self.fps <= 0:
            QMessageBox.warning(self, "警告", f"fps: {self.fps} 不能小于0")
            return

        self.show_info()
        save_path = self.img_dir + '.avi'
        t = WorkThread(self, self.img_dir, save_path, self.fps)
        t.process.connect(self.call_backlog)
        try:
            t.start()
        except Exception as e:
            print(e)
        finally:
            self.reset()

    def call_backlog(self, msg):
        self.pbar.setValue(int(msg))  # 将线程的参数传入进度条

    # 清空当前的所有设置
    def reset(self):
        self.fps = 0
        self.img_dir = ""
        self.times_path = ""
        self.show_info()

    def show_info(self):
        self.show_imgs.setText(self.img_dir)
        if self.times_path:
            self.show_times.setText(f'{self.times_path}')
        else:
            if self.fps != 0:
                self.show_times.setText(str(self.fps))
