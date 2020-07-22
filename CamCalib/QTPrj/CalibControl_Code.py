# -*- coding: utf-8 -*-
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from CalibControl_UI import CalibControlUI

import cv2
import numpy as np
import glob
import sys

class Calib:
    def __init__(self):
        self.mtx = None
        self.dist = None
        self.rmtx = None
        self.tmtx = None
        self.circle_objp = None
        self.angle = None

        # 标定，获取内参，同一相机内参矩阵固定
        try:
            npzfile = np.load('../Calibresult/calibrate.npz')
            self.mtx = npzfile['mtx']
            self.dist = npzfile['dist']
        except IOError:
            print("重新标定相机...")
            self.Calibrate()

        # 获取外参
        try:
            npzfile1 = np.load('../Calibresult/Transfer.npz')
            self.rmtx = npzfile1['rmtx']
            self.tmtx = npzfile1['tmtx']
        except IOError:
            print("重新标定外参...")
            self.Transfer()

        self.DetectCircle(self.mtx, self.rmtx, self.tmtx)

    def get_rmtx(self):
        return self.rmtx

    def get_tmtx(self):
        return self.tmtx

    def Calibrate(self):
        criteria = (cv2.TERM_CRITERIA_MAX_ITER | cv2.TERM_CRITERIA_EPS, 30, 0.0001)
        objp = np.zeros((Nx_cor*Ny_cor, 3), np.float32)
        objp[:, :2] = np.mgrid[0:Nx_cor*gap:gap, 0:Ny_cor*gap:gap].T.reshape(-1, 2)
        obj_points = []
        img_points = []
        images = sorted(glob.glob("../Calibsource/calib*.jpg"))

        for fname in images:
            img = cv2.imread(fname)
            cv2.imshow('img', img)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, (Nx_cor, Ny_cor), None)
            print(ret)
            if ret:
                corners = cv2.cornerSubPix(gray, corners, (5, 5), (1, 1), criteria)
                obj_points.append(objp)
                img_points.append(corners)
                cv2.drawChessboardCorners(img, (Nx_cor, Ny_cor), corners, ret)
                cv2.imshow('img', img)
                cv2.waitKey(500)

        print('共计', len(img_points), '张图片')
        # global mtx, dist
        ret, self.mtx, self.dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)
        np.savez('../Calibresult/calibrate.npz', mtx=self.mtx, dist=self.dist[0:4])

    def draw_axis(self, img, corners, imgpts):
        corners = corners.astype(np.int32)
        imgpts = imgpts.astype(np.int32)
        corner = tuple(corners[0].ravel())
        img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255, 0, 0), 5)
        cv2.putText(img, "x", tuple(imgpts[0].ravel()), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0, 255, 0), 5)
        cv2.putText(img, "y", tuple(imgpts[1].ravel()), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0, 0, 255), 5)
        cv2.putText(img, "z", tuple(imgpts[2].ravel()), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return img

    def Transfer(self):
        # 绘制坐标系
        axis_axis = np.float32([[20, 0, 0], [0, 20, 0], [0, 0, -20]]).reshape(-1, 3)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.0001)
        objp = np.zeros((Nx_cor*Ny_cor, 3), np.float32)
        objp[:, :2] = np.mgrid[0:Nx_cor*gap:gap, 0:Ny_cor*gap:gap].T.reshape(-1, 2)
        images = glob.glob('../Calibsource/Transfer.jpg')
        if len(images) == 0:
            print('No Test Picture can be loading!')
            exit()
        img = cv2.imread(images[0])

        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        ret, corners = cv2.findChessboardCorners(binary, (Nx_cor, Ny_cor), None)

        # global rmtx, tmtx
        if ret:
            imgp_temp = cv2.cornerSubPix(gray, corners, (5, 5), (1, 1), criteria)  # 亚像素点
            if imgp_temp[0][0][0] < imgp_temp[1][0][0]:  # 判断是否按照由左到右的顺序
                imgp = imgp_temp
            else:
                imgp = np.flipud(imgp_temp)

            ret, self.rmtx, self.tmtx, inliers = cv2.solvePnPRansac(objp, imgp, self.mtx, self.dist)
            # project 3D points to image plane
            imgpts, jac = cv2.projectPoints(axis_axis, self.rmtx, self.tmtx, self.mtx, self.dist)
            img = self.draw_axis(img, imgp, imgpts)

            # cv2.imshow('img', img)
            # cv2.waitKey(2000)
            cv2.imwrite('../Calibresult/gesture.png', img)

            print('imgp:', imgp[0])
            print('world:', self.cameraToWorld(self.mtx, self.rmtx, self.tmtx, imgp[0][0]))
            print("-----------------------------------------------------")
            np.savez('../Calibresult/Transfer.npz', rmtx=self.rmtx, tmtx=self.tmtx)
            return img # 返回带坐标系图片

    def DetectCircle(self, matrix, Rmatrix, tmatrix):
        image = glob.glob('../Calibsource/circle.jpg')
        if len(image) == 0:
            print('No Detect Picture can be loading!')
            exit()
        img = cv2.imread(image[0])
        imgroi = img[0:960, 320:1280]  # roi [y,x]

        imgGray = cv2.cvtColor(imgroi, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(imgGray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        find = False  # 是否检测到圆的标志,False--->未检测到圆，True--->检测到圆
        for cnt in contours:
            area = cv2.contourArea(cnt)
            # 工件大圆检测
            if 2000 < area < 500000:
                cv2.drawContours(imgroi, cnt, -1, (255, 30, 255), 2)  # 绘制外轮廓
                (Cx, Cy), radius = cv2.minEnclosingCircle(cnt)
                Xcenter = (int(Cx), int(Cy))
                Sx = Cx + 320
                Sy = Cy
                circle_point = np.array([Sx, Sy], dtype=np.float32)
                radius = int(radius)
                cv2.circle(imgroi, Xcenter, radius, (255, 0, 0), 2)
                print("大圆中心坐标为：", Xcenter)
                find = True

            # 工件小圆检测
            if 200 < area < 2000:
                cv2.drawContours(imgroi, cnt, -1, (255, 0, 255), 2)  # 绘制外轮廓
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                x, y, w, h = cv2.boundingRect(approx)
                cv2.rectangle(imgroi, (x, y), (x + w, y + h), (0, 255, 0), 3)
                Rx = x + w / 2
                Ry = y + h / 2
                Ycenter = (int(Rx), int(Ry))
                print("小圆中心坐标为:", Ycenter)
                cv2.line(imgroi, (int(Cx), int(Cy)), (int(Rx), int(Ry)), (0, 255, 0), 2)
                a = np.array([int(Rx - Cx), int(Ry - Cy)])
                b = np.array([int(Cx), 0])
                cosangle = a.dot(b) / (np.linalg.norm(a) * np.linalg.norm(b))
                self.angle = np.arccos(cosangle) * 57.3
                if Cy < Ry:
                    self.angle = 360 - self.angle
                cv2.putText(imgroi, '{}'.format(self.angle), Ycenter, cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)

        if find:
            print('圆心检测成功!')
            cv2.imwrite('../Calibresult/detectedCircle.jpg', imgroi)
            print('圆心坐标为:', circle_point)
            self.circle_objp = self.cameraToWorld(matrix, Rmatrix, tmatrix, circle_point)[0][0]
            print('圆心对应世界坐标为:', self.circle_objp)
            print("-----------------------------------------------------")
        else:
            print('圆心检测失败!')
            print("-----------------------------------------------------")

    def cameraToWorld(self, cameraMatrix, r, t, imgPoints):
        invK = np.asmatrix(cameraMatrix).I
        rMat = np.zeros((3, 3), dtype=np.float64)
        cv2.Rodrigues(r, rMat)
        # print('rMat=', rMat)
        # 计算 invR * T
        invR = np.asmatrix(rMat).I  # 3*3
        # print('invR=', invR)
        transPlaneToCam = np.dot(invR, np.asmatrix(t))  # 3*3 dot 3*1 = 3*1
        # print('transPlaneToCam=', transPlaneToCam)
        worldpt = []
        coords = np.zeros((3, 1), dtype=np.float64)

        coords[0][0] = imgPoints[0]
        coords[1][0] = imgPoints[1]
        coords[2][0] = 1.0

        worldPtCam = np.dot(invK, coords)  # 3*3 dot 3*1 = 3*1
        # print('worldPtCam=', worldPtCam)
        # [x,y,1] * invR
        worldPtPlane = np.dot(invR, worldPtCam)  # 3*3 dot 3*1 = 3*1
        # print('worldPtPlane=', worldPtPlane)
        # zc
        scale = transPlaneToCam[2][0] / worldPtPlane[2][0]
        # print("scale: ", scale)
        # zc * [x,y,1] * invR
        scale_worldPtPlane = np.multiply(scale, worldPtPlane)
        # print("scale_worldPtPlane: ", scale_worldPtPlane)
        # [X,Y,Z]=zc*[x,y,1]*invR - invR*T
        worldPtPlaneReproject = np.asmatrix(scale_worldPtPlane) - np.asmatrix(transPlaneToCam)  # 3*1 dot 1*3 = 3*3
        # print("worldPtPlaneReproject: ", worldPtPlaneReproject)
        pt = np.zeros((3, 1), dtype=np.float64)
        # 转为SCARA适合的笛卡尔右手坐标系
        pt[0][0] = worldPtPlaneReproject[0][0]
        pt[1][0] = worldPtPlaneReproject[1][0]
        pt[2][0] = 0  # 世界坐标系的Z轴坐标，一般设定为0
        worldpt.append(pt.T)
        # print('worldpt:',worldpt)
        return worldpt


class MainWindow(QWidget,CalibControl_UI):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initTimer()
        self.calib = None

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
        # self.openCameraBtn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.openCameraBtn.setEnabled(True)
        self.openCameraBtn.clicked.connect(self.openCamera)
        self.CalibBtn = QPushButton('相机标定')
        # self.CalibBtn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.CalibBtn.clicked.connect(self.OpenCalib)
        self.transBtn = QPushButton('外参标定')
        # self.transBtn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.transBtn.setEnabled(False)
        self.transBtn.clicked.connect(self.calib_slot)

        self.catchBtn = QPushButton('目标抓取')
        # self.catchBtn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.catchBtn.setEnabled(False)
        # self.catchBtn.clicked.connect(self.catch)
        self.closeCameraBtn = QPushButton('关闭相机')
        # self.closeCameraBtn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.closeCameraBtn.clicked.connect(self.closeCamera)
        self.closeCameraBtn.setEnabled(False)

        self.yolov3Btn = QPushButton('Yolo识别')

        ## 坐标跟踪
        self.setcoorLabel_X = QLabel('x')
        self.setcoorLabel_Y = QLabel('y')
        self.setcoorBox_X = QLineEdit()
        self.setcoorBox_Y = QLineEdit()
        self.setcoorBtn = QPushButton('确认')

        ## 相机相关参数
        self.mtx_label = QLabel('内参')
        self.rt_label = QLabel('外参')
        self.mtx_text = QTextEdit()
        self.rt_text = QTextEdit()


        ## 工件相关参数
        self.coor_label = QLabel('工件坐标')
        self.angel_label = QLabel('工件角度')
        self.coor_box = QLineEdit()
        self.angel_box = QLineEdit()

        ## 设置只读属性的文本框
        self.mtx_text.setReadOnly(True)
        self.rt_text.setReadOnly(True)
        self.coor_box.setReadOnly(True)
        self.angel_box.setReadOnly(True)

        ## 帮助信息
        self.help_box = QTextEdit('使用帮助:'+'\r\n')

        ## 界面布局
        self.hbox = QHBoxLayout(self)   # 添加一个水平布局
        self.hbox.addWidget(self.lbl)

        self.gbox = QGridLayout(self)
        self.gbox.addWidget(self.mtx_label, 1,1,1,1)
        self.gbox.addWidget(self.mtx_text, 2,1,1,1)
        self.gbox.addWidget(self.rt_label, 1,5,1,1)
        self.gbox.addWidget(self.rt_text, 2,5,1,1)
        self.gbox.addWidget(self.coor_label, 7,1,1,1)
        self.gbox.addWidget(self.coor_box, 8,1,1,5)
        self.gbox.addWidget(self.angel_label, 10,1,1,1)
        self.gbox.addWidget(self.angel_box, 11,1,1,5)

        ### 坐标追踪
        self.gbox.addWidget(self.setcoorLabel_X, 12,1,1,1)
        self.gbox.addWidget(self.setcoorBox_X, 12,2,1,1)
        self.gbox.addWidget(self.setcoorLabel_Y, 12,3,1,1)
        self.gbox.addWidget(self.setcoorBox_Y, 12,4,1,1)
        self.gbox.addWidget(self.setcoorBtn, 12,5,1,1)


        self.gbox.addWidget(self.openCameraBtn,13,1,1,2)
        self.gbox.addWidget(self.CalibBtn, 13,4,1,2)
        self.gbox.addWidget(self.transBtn, 15,1,1,2)
        self.gbox.addWidget(self.yolov3Btn,15,4,1,2)
        self.gbox.addWidget(self.catchBtn, 17,1,1,2)
        self.gbox.addWidget(self.closeCameraBtn, 17,4,1,2)
        self.gbox.addWidget(self.help_box,19,1,1,5)

        self.hbox.addLayout(self.gbox)

        self.QLable_close()
        self.move(40, 40)
        self.setWindowTitle('OPEN CV_Video')

        self.setGeometry(300, 40, 1500, 1000)
        self.show()

    def calib_slot(self):
        img_axis = self.calib.Transfer()
        img_axis = img_axis[:, 320:] # must before convert
        img_axis = cv2.cvtColor(img_axis, cv2.COLOR_BGR2RGB)

        heigt, width = img_axis.shape[:2]
        pixmap = QImage(img_axis, width, heigt, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(pixmap)
        self.lbl.setPixmap(pixmap)

        self.rt_text.setText('旋转向量:\r\n' + np.array2string(self.calib.get_rmtx()) + '\r\n\r\n' + '平移向量:\r\n' +np.array2string(self.calib.get_tmtx()))


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
        self.mtx_text.setText(np.array2string(self.calib.mtx,))
        self.rt_text.setText('旋转向量：\r\n' + np.array2string(self.calib.rmtx,) +'\r\n\r\n'+ '平移向量:\r\n' + np.array2string(self.calib.tmtx,))
        self.coor_box.setText(np.array2string(self.calib.circle_objp))
        self.angel_box.setText(np.array2string(self.calib.angle))
        self.CalibBtn.setEnabled(False)
        self.transBtn.setEnabled(True)

    def HelpText(self):
        QMessageBox.information(self, '使用帮助', '相机标定：标定相机的内外参数'+'\r\n'
                                                '外参标定：重新标定相机的外参'+'\r\n'
                                                '目标抓取：抓取工件')

    def start(self):
        self.timer.start(100)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gap = 5
    Nx_cor = 19
    Ny_cor = 15
    ex = MainWindow()
    sys.exit(app.exec_())