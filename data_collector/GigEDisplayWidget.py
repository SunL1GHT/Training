from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from camera.CameraInterface import *
import time
import os
from pathlib import Path


SAVING_PATH = "data/"



BUTTON_STYLE = "\
QPushButton {\
    background-color: lightgray;\
    border-style: outset;\
    border-width: 2px;\
    border-radius: 10px;\
    border-color: beige;\
    font: 24px;\
    padding: 8px;\
}\
QPushButton:pressed {\
    background-color: gray;\
    border-style: inset;\
}\
"

GROUPBOX_STYLE_TOTAL = "\
QGroupBox {\
    background-color: lightgray;\
    border-style: outset;\
    border-width: 2px;\
    border-radius: 10px;\
    border-color: beige;\
}\
"

GROUPBOX_STYLE_GOOD = "\
QGroupBox {\
    background-color: green;\
    border-style: outset;\
    border-width: 2px;\
    border-radius: 10px;\
    border-color: beige;\
}\
"

GROUPBOX_STYLE_NG = "\
QGroupBox {\
    background-color: red;\
    border-style: outset;\
    border-width: 2px;\
    border-radius: 10px;\
    border-color: beige;\
}\
"

class NormalButton(QPushButton):
    def __init__(self, str):
        QPushButton.__init__(self, str)
        self.setStyleSheet(BUTTON_STYLE);





class CustomizedImageLabel(QLabel):
    def __init__(self,t):
        QLabel.__init__(self,t)
        self.setAlignment(Qt.AlignCenter)
        self.pic_width = 640
        self.pic_height = 480
        self.resize(self.pic_width,self.pic_height)
        self.resize_signal = CustomizedSignal()
        
# 控制面板
class ControlPannel(QGroupBox):
    def __init__(self):
        #字体大小
        self.font = QFont()
        self.font.setPixelSize(18)
        QGroupBox.__init__(self,"控制面板")

        #button group
        self.cam_select_combo = QComboBox()
        # self.cam_select_combo.addItem("选择相机")
        # self.cam_select_combo.addItem("LBAS")
        # self.cam_select_combo.addItem("USB")
        # self.cam_select_combo.addItem("MindVision")
        self.cam_select_combo.setFont(self.font)
        
        

        self.cam_btn = NormalButton("打开相机")
        self.auto_save_btn = NormalButton("开始自动采集")
        self.auto_save_time_interval_label = QLabel("自动采集时间间隔:")
        self.auto_save_time_interval_label.setFont(self.font)
        # self.auto_save_time_interval_label.setStyleSheet("font:20")
        self.auto_save_time_spinbox = QSpinBox()
        self.auto_save_time_spinbox.setRange(0,1000)
        self.auto_save_time_spinbox.setValue(50)
        self.auto_save_time_spinbox.setFont(self.font)

        self.layout = QVBoxLayout()
        # self.layout.addWidget(self.cam_select_combo)
        self.layout.addWidget(self.cam_btn)
        self.layout.addWidget(self.auto_save_btn)
        self.layout.addWidget(self.auto_save_time_interval_label)
        self.layout.addWidget(self.auto_save_time_spinbox)
        self.layout.addStretch()
        self.setLayout(self.layout)

class ImagePannel(QGroupBox):
    def __init__(self,title,learn):
        QGroupBox.__init__(self,title)



class WarningBox(QMessageBox):
    def __init__(self,text):
        QMessageBox.__init__(self)
        self.setText(text)

        self.timer = QTimer()
        self.timer.setInterval(3000)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timeoutSlot)
        self.timer.start()

        ret = self.exec_()
        if ret == QMessageBox.Ok:
            self.ok_clicked()

    
    def ok_clicked(self):
        print("ok clicked...")
    
    @Slot()
    def timeoutSlot(self):
        #print("get in time out")
        self.close()


# IMAGE_WIDTH = 640
# IMAGE_HEIGHT = 480

IMAGE_WIDTH = 1200
IMAGE_HEIGHT = 960



class GigEDisplayWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)


        #图像显示部分
        self.image = CustomizedImageLabel("image")
        #相机实例化
        self.camera = None
        self.camera = CameraInterface("LBAS",0)
        # self.camera = CameraInterface("usb",0)


        #控制面板
        self.control = ControlPannel()
        # self.control.cam_select_combo.setCurrentIndex(0)



        #layout
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.image,stretch=5)
        self.layout.addWidget(self.control,stretch=1)
        self.layout.addStretch()
        self.setLayout(self.layout)


        # 添加保存快捷键
        shortcut_save_ok = QShortcut(QKeySequence(self.tr("Ctrl+O", "File|Open")),self)
        shortcut_save_ok.setKey('s')    #"ok"
        shortcut_save_ok.activated.connect(self.auto_save)

        #signal and slot
        #--------control pannel---------
        # self.control.cam_select_combo.currentIndexChanged.connect(self.cam_select)
        # self.control.cam_select_combo.activated.connect(self.cam_select)
        self.control.cam_btn.clicked.connect(self.cam_control)
        self.control.auto_save_btn.clicked.connect(self.auto_save_control)


        


        #相机图像更新定时器
        self.update_timer = QTimer(self,interval = 5)
        self.update_timer.timeout.connect(self.update_frame)

        #自动采集定时器
        self.auto_save_timer = QTimer(self)
        self.auto_save_timer.timeout.connect(self.auto_save)


        #variables
        self.cam_state = False  #用来显示相机的当前状态   True:打开   False:关闭，主要用于相机控制按钮的状态
        self.auto_save_state = False



    def cam_select(self):
        # print(self.control.cam_select_combo.currentIndex())
        # print(self.control.cam_select_combo.currentText())

        # self.camera = CameraInterface("LBAS",0)
        self.camera = CameraInterface(self.control.cam_select_combo.currentText(),0)


    def auto_save(self):
        image = self.camera.pop_frame()
        fname =  '{}img{}.jpg'.format(SAVING_PATH,int(round(time.time() * 1000)))
        self.camera.save(fname,image)






    def auto_save_control(self):
        if not self.cam_state:
            return

        self.auto_save_state = not self.auto_save_state
        if self.auto_save_state:
            self.auto_save_timer.setInterval(self.control.auto_save_time_spinbox.value())
            self.auto_save_timer.start()
            self.control.auto_save_btn.setText("关闭自动采集")
        else:
            self.auto_save_timer.stop()
            self.control.auto_save_btn.setText("开启自动采集")



    def cam_control(self):
        self.cam_state = not self.cam_state

        if self.cam_state:
            if self.on_open_camera():
                self.control.cam_btn.setText("关闭相机")
            else:
                self.cam_state = not self.cam_state
        else:
            self.on_close_camera()
            self.control.cam_btn.setText("打开相机")





    def on_open_camera(self):
        cams_status = True
        status = self.camera.open()
        if status:
            self.update_timer.start()
            
        cams_status = cams_status and status

        if not cams_status:
            self.warning = WarningBox("相机打开失败，请检查连线是否正确。")
        return cams_status

    def on_close_camera(self):
        self.update_timer.stop()
        self.camera.close()
        self.image.clear()




    def update_frame(self):
        if self.camera == None:
            return

        image = self.camera.pop_frame()
       
        self.displayImage(image,True)


    def displayImage(self, img, window=True):
        qformat = QImage.Format_Indexed8
        # print("img.shap in displayImage .....   ",img.shape)
        if len(img.shape)==3 :
            if img.shape[2]==4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888


        # print(img.shape)

        outImage = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        # outImage = outImage.rgbSwapped()
        # outImage = outImage.scaled(1920,1280)
        # print(outImage.width())

        if window:
            resizedImage = QPixmap.fromImage(outImage)
            # resizedImage = resizedImage.scaled(IMAGE_WIDTH,IMAGE_HEIGHT,Qt.KeepAspectRatio) 
            self.image.setPixmap(resizedImage)