# -*- coding: utf-8 -*-

"""
PyQt5 tutorial 

This example shows how to use
a QComboBox widget.

author: py40.com
last edited: 2017年3月
"""
import json
import sys
import os
import time

import pandas as pd
from glom import glom

from PyQt5.QtWidgets import (QMessageBox, QLineEdit, QWidget, QLabel, QDesktopWidget,
                             QPushButton, QApplication)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

ROOT_PATH = 'D:\\桌面\\数据集\\handpose_datasets_v1-2021-01-31\\dataPackage\\0'


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self._filenames = []  # 所有文件名，不包括后缀
        self._idx = 0  # 文件索引 从-1开始
        self._info_data = None  # json所有数据
        self._pic = None  # 图片名
        self._pixmap = None  # pixmap
        self._lbl = None  # 放置图片
        self._status = None  # 状态栏
        self._qle = None  # 输入框

        self.getFilenames()  # 获得文件夹所有文件名
        self.readJson()  # 第一张单独处理
        self._pic = os.path.join(ROOT_PATH, str(self._filenames[self._idx]) + '.jpg')  # 第一张单独处理

        self.initUI()  # 绘图

    def getFilenames(self):
        image_list = os.listdir(ROOT_PATH)
        for idx, file in enumerate(image_list):
            # print(file)
            if idx % 2 == 0:
                self._filenames.append(file.split('.')[0])
        print(self._filenames)

    def getNext(self):
        if self._idx+1 >= len(os.listdir(ROOT_PATH)) / 2:
            QMessageBox.information(self, "Information", "您已完成此工作包！！！")
            QApplication.instance().quit()
        else:
            self._idx += 1
            self.readJson()
            self._pic = os.path.join(ROOT_PATH, str(self._filenames[self._idx]) + '.jpg')
            self._status.setText(os.path.split(self._pic)[-1])
            self._pixmap = QPixmap(self._pic)
            self._pixmap = self._pixmap.scaledToWidth(400)
            self._lbl.setPixmap(self._pixmap)
            self._qle.setText(self.array2text(self._info_data['info'][0]['fingers']))

    def readJson(self):
        # print(os.path.join(ROOT_PATH,str(self._filenames[self._idx])+'.json'))
        # JSON到字典转化
        f = open(os.path.join(ROOT_PATH, str(self._filenames[self._idx]) + '.json'), 'r')
        print(self._filenames[self._idx])
        self._info_data = json.load(f)
        # print(info_data)
        if 'fingers' not in self._info_data['info'][0]:
            self._info_data['info'][0]['fingers'] = [0, 0, 0, 0, 0]

    def initUI(self):
        # 设置label提示
        # tip = QLabel(self)
        # tip.setText('提示：0，1，2，3，4，5，6，7，8，9，+')
        # 设置字体
        font = QFont()
        font.setFamily("Arial")  # 括号里能够设置成本身想要的其它字体
        font.setPointSize(18)  # 括号里的数字能够设置成本身想要的字体大小
        # 设置输入框
        self._qle = QLineEdit(self)
        self._qle.resize(220, 40)
        self._qle.move(530, 250)
        self._qle.setFont(font)
        self._qle.setText(self.array2text(self._info_data['info'][0]['fingers']))
        self._qle.textChanged[str].connect(self.textChanged)
        # 设置确认按钮
        # btn = QPushButton('确认', self)
        # btn.resize(80, 40)
        # btn.setCheckable(True)
        # btn.move(600, 350)
        # btn.clicked[bool].connect(self.writeData)
        # 设置图片
        self._pixmap = QPixmap(self._pic)
        self._pixmap = self._pixmap.scaledToWidth(400)
        self._lbl = QLabel(self)
        self._lbl.setPixmap(self._pixmap)
        self._lbl.move(100, 30)
        # 状态栏
        self._status = QLabel(self)
        self._status.setText(os.path.split(self._pic)[-1])
        self._status.move(200, 5)
        # 提示
        self._tip = QLabel(self)
        self._tip.setText('ctrl 确认   alt 清空')
        self._tip.setFont(font)
        self._tip.move(530,500)
        self._tip2 = QLabel(self)
        self._tip2.setText('填写内容为0-18代表0-180')
        font.setPointSize(10)  # 括号里的数字能够设置成本身想要的字体大小
        self._tip2.setFont(font)
        self._tip2.move(530, 600)
        # 父控件
        self.setGeometry(300, 300, 800, 650)
        self.setWindowTitle('数据标注')
        self.center()
        self.show()

    # 控制窗口显示在屏幕中心的方法
    def center(self):
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 写回数据
    def writeData(self):
        if len(self._info_data['info'][0]['fingers']) != 5:
            QMessageBox.information(self, "Information", "输入有误")
            return False
        else:
            self._info_data = self.format()
            file = os.path.join(ROOT_PATH, str(self._filenames[self._idx]) + '.json')
            with open(file, 'w', encoding='utf-8') as f:
                json.dump(self._info_data, f)
            # print("加载入文件完成...")
            print('Finished:' + str(self._idx+1))
            print('')
            return True

    # 输入和数据转换
    def text2array(self, input):
        temp = [10*int(i) for i in input.split()]
        # temp = [0,0,0,0,0]
        return temp

    # 输入和数据转换
    def array2text(self, input):
        temp = ''
        for i in input:
            temp += str(int(i/10))
            temp += ' '
        temp = temp.strip()
        return temp

    # 输入框数据绑定
    def textChanged(self, text):
        self._info_data['info'][0]['fingers'] = self.text2array(text)
    # 格式化
    def format(self):
        tmp= dict()
        tmp['maker']=self._info_data['maker']
        tmp['modifier'] = 'wangyu'
        tmp['date'] = self._info_data['date']
        tmp['modified_time'] = time.strftime("%Y-%m-%d", time.localtime())
        tmp['info']=self._info_data['info']
        # print(tmp)
        return tmp

    # 重写键盘响应
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key() == Qt.Key_Control:
            # pass
            if (self.writeData()):
                self.getNext()
        elif e.key() == Qt.Key_Alt:
            self._qle.setText('')
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
