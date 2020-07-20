# -*- coding: utf-8 -*-
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

import cv2
import numpy as np
import glob
import sys

class Calib:
    def __init__(self):
        self.Nx_cor = 19  # 横向
        self.Ny_cor = 15  # 竖向
 
        # 标定，获取内参，同一相机内参矩阵固定
        try:
            npzfile = np.load('/home/gxg/Desktop/Training/CamCalib/Calibresult/calibrate.npz')
            self.mtx = npzfile['mtx']
            self.dist = npzfile['dist']
        except IOError:
            print("重新标定相机...")
            self.calibrate()

        # 二次标定,获取相机-标定板外参
        try:
            npzfile1 = np.load('/home/gxg/Desktop/Training/CamCalib/Calibresult/Transfer.npz')
            self.rmtx = npzfile1['rmtx']
            self.tmtx = npzfile1['tmtx']
        except IOError:
            print("重新标定外参...")
            self.Transfer()

    def calibrate(self):
        # 设置寻找亚像素角点的参数，采用的停止准则是最大迭代次数30和最大误差容限0.001
        criteria = (cv2.TERM_CRITERIA_MAX_ITER | cv2.TERM_CRITERIA_EPS, 30, 0.001)
        # 获取标定板角点的位置
        objp = np.zeros((self.Nx_cor * self.Ny_cor, 3), np.float32)
        objp[:, :2] = np.mgrid[0:self.Nx_cor * 5:5, 0:self.Ny_cor * 5:5].T.reshape(-1, 2)  # 将世界坐标系建在标定板上，所有点的Z坐标全部为0，所以只需要赋值x和y

        obj_points = []  # 存储3D点
        img_points = []  # 存储2D点
        images = glob.glob("/home/gxg/Desktop/Training/CamCalib/Calibsource/calib*.jpg")
        for fname in images:
            # print(fname)
            img = cv2.imread(fname)
            cv2.imshow('img', img)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, (self.Nx_cor, self.Ny_cor), None)
            print(ret)
            if ret:
                corners = cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), criteria)  # 在原角点的基础上寻找亚像素角点
                obj_points.append(objp)
                img_points.append(corners)

                cv2.drawChessboardCorners(img, (self.Nx_cor, self.Ny_cor), corners, ret)  # OpenCV的绘制函数一般无返回值
                cv2.imshow('img', img)
                cv2.waitKey(800)
        print('共计', len(img_points), '张图片')

        # global mtx, dist
        # 标定
        ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

        # 衡量误差
        tot_error = 0
        for i in range(len(obj_points)):
            img_points2, _ = cv2.projectPoints(obj_points[i], self.rvecs[i], self.tvecs[i], self.mtx, self.dist)
            error = cv2.norm(img_points[i], img_points2, cv2.NORM_L2) / len(img_points2)
            tot_error += error
        print("重投影误差:", tot_error / len(obj_points))
        # print("-----------------------------------------------------")
        np.savez('/home/gxg/Desktop/Training/CamCalib/Calibresult/calibrate.npz', mtx=self.mtx, dist=self.dist[0:4])

    # 得到相机的外参矩阵
    def Transfer(self):
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        objp = np.zeros((self.Nx_cor * self.Ny_cor, 3), np.float32)
        objp[:, :2] = np.mgrid[0:self.Nx_cor * 30:30, 0:self.Ny_cor * 30:30].T.reshape(-1, 2)

        print("外参标定时采用的内参矩阵为:\n", mtx)
        # 载入固定标定图
        images = glob.glob('/home/gxg/Desktop/Training/CamCalib/Calibsource/calib1.jpg')  # 选择需要标定的图片
        if len(images) == 0:
            print('No Test Picture can be loading!')
            exit()
        img = cv2.imread(images[0])
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # 灰度处理
        ret, corners = cv2.findChessboardCorners(gray, (self.Nx_cor, self.Ny_cor), None)  # 寻找角点
        print(ret)
        # global rmtx, tmtx
        if ret:
            imgp = cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), criteria)
            ret, self.rmtx, self.tmtx, inliers = cv2.solvePnPRansac(objp, imgp, mtx, dist)
            # print('像素原点:', imgp[0][0])
            # print('用户原点:', cameraToWorld(mtx, rmtx, tmtx, imgp[0][0])[0][0])
        # print("-----------------------------------------------------")
        # print(rmtx)
        # return rmtx,tmtx
        np.savez('/home/gxg/Desktop/Training/CamCalib/Calibresult/Transfer.npz', rmtx = self.rmtx, tmtx = self.tmtx)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initTimer()


    def initTimer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_pic)

    def show_pic(self):
        ret, img = self.vc.read()
        if not ret:
            print('read error!\n')
            return
        cv2.flip(img, 1, img)
        cur_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        heigt, width = cur_frame.shape[:2]
        # print(heigt,width)
        pixmap = QImage(cur_frame, width, heigt, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(pixmap)
        self.lbl.setPixmap(pixmap)

    def openCamera(self):
        self.lbl.setEnabled(True)
        self.vc = cv2.VideoCapture(0)
        self.openCameraBtn.setEnabled(False)
        self.closeCameraBtn.setEnabled(True)
        self.timer.start(100)

    def closeCamera(self):
        self.vc.release()
        self.openCameraBtn.setEnabled(True)
        self.closeCameraBtn.setEnabled(False)
        self.QLable_close()
        self.timer.stop()

    def initUI(self):
        # 控件实例化与对应的信号
        ## 视频展示
        self.lbl = QLabel(self)
        self.lbl.setFixedWidth(960)
        self.lbl.setFixedHeight(960)

        ## 按钮
        self.openCameraBtn = QPushButton('打开相机')
        self.openCameraBtn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.openCameraBtn.clicked.connect(self.openCamera)
        self.CalibBtn = QPushButton('相机标定')
        self.CalibBtn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.CalibBtn.clicked.connect(self.OpenCalib)
        self.transBtn = QPushButton('外参标定')
        self.transBtn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # self.transBtn.clicked.connect(self.)
        self.catchBtn = QPushButton('目标抓取')
        self.catchBtn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # self.catchBtn.clicked.connect(self.catch)
        self.closeCameraBtn = QPushButton('关闭相机')
        self.closeCameraBtn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.closeCameraBtn.clicked.connect(self.closeCamera)
        self.openCameraBtn.setEnabled(True)
        self.closeCameraBtn.setEnabled(False)

        # 设置按钮大小
        self.openCameraBtn.setFixedSize(100, 60)
        self.CalibBtn.setFixedSize(100, 60)
        self.transBtn.setFixedSize(100, 60)
        self.catchBtn.setFixedSize(100, 60)
        self.closeCameraBtn.setFixedSize(100, 60)


        ## 相机相关参数
        self.mtx_label = QLabel('内参')
        self.rt_label = QLabel('外参')
        self.mtx_text = QTextBrowser()
        self.rt_text = QTextBrowser()

        ## 工件相关参数
        self.coor_label = QLabel('工件坐标')
        self.coor_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.angel_label = QLabel('工件角度')
        self.angel_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.coor_box = QLineEdit()
        self.angel_box = QLineEdit()
        self.coor_box.setReadOnly(True)
        self.angel_box.setReadOnly(True)

        ## 界面布局
        self.hbox = QHBoxLayout(self)   # 添加一个水平布局
        self.hbox.addWidget(self.lbl)

        self.fbox = QFormLayout(self)   # 添加一个表单布局
        self.fbox.addRow(self.mtx_label, self.mtx_text)
        self.fbox.addRow(self.rt_label, self.rt_text)
        self.fbox.addRow(self.coor_label,self.coor_box) #只有表单布局存在addrow
        self.fbox.addRow(self.angel_label,self.angel_box)
        self.fbox.setRowWrapPolicy(QFormLayout.WrapAllRows)  # 字段总是位与标签的下方
        self.fbox.addRow(self.openCameraBtn)
        self.fbox.addRow(self.CalibBtn)
        self.fbox.addRow(self.transBtn)
        self.fbox.addRow(self.catchBtn)
        self.fbox.addRow(self.closeCameraBtn)
        self.fbox.setRowWrapPolicy(QFormLayout.WrapAllRows)  # 字段总是位与标签的下方
        self.hbox.addLayout(self.fbox)

        self.setLayout(self.hbox)   # 设置widget控件布局为水平布局

        self.QLable_close()
        self.move(40, 40)   # 有什么用？
        self.setWindowTitle('OPEN CV_Video')
        self.setGeometry(300, 40, 1230, 1000)
        self.show()

    def openCamera(self):
        self.lbl.setEnabled(True)
        self.vc = cv2.VideoCapture(0)
        self.openCameraBtn.setEnabled(False)
        self.closeCameraBtn.setEnabled(True)
        self.timer.start(100)

    def QLable_close(self):
        self.lbl.setStyleSheet("background:black;")
        self.lbl.setPixmap(QPixmap())   # 设置label的背景

    def OpenCalib(self):
        # 实例化函数
        self.calib = Calib()
        self.mtx_text.setText(self.calib.mtx)
        self.rt_text.setText(self.calib.rmtx,self.calib.tmtx)


    def start(self):
        self.timer.start(100)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())