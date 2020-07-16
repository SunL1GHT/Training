import cv2
import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
# from UIFactory import *
# from pages.InspSettingWidget import *
# from pages.CameraSettingWidget import *
from GigEDisplayWidget import *
# from ctypes import *




# def wrap_function(lib, funcname, restype, argtypes):
#     """Simplify wrapping ctypes functions"""
#     func = lib.__getattr__(funcname)
#     func.restype = restype
#     func.argtypes = argtypes
#     return func


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("数据采集软件")
        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("")
        
        # Exit QAction
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)
        self.file_menu.addAction(exit_action)

  
        self.main_page = GigEDisplayWidget()    # 使用GigECamera
        
        # 设置默认居中widget
        self.setCentralWidget(self.main_page)

        # signals and slots
        # self.main_page.cam_setting.clicked.connect(self.on_open_cam_setting_page)
        # self.main_page.insp_setting.clicked.connect(self.on_open_insp_setting_page)


    
    @Slot()
    def exit_app(self, checked):
        QApplication.quit()

    # @Slot()
    # def on_open_main_page(self):
    #     #self.main_page = DisplayWidget()    # 使用usb camera
    #     self.main_page = GigEDisplayWidget()    # 使用GigECamera
    #     self.main_page.cam_setting.clicked.connect(self.on_open_cam_setting_page)
    #     self.main_page.insp_setting.clicked.connect(self.on_open_insp_setting_page)
    #     self.setCentralWidget(self.main_page)

    # @Slot()
    # def on_open_cam_setting_page(self):
    #     self.cam_setting_page = CameraSettingWidget()
    #     self.cam_setting_page.back.clicked.connect(self.on_open_main_page)
    #     self.setCentralWidget(self.cam_setting_page)

    # @Slot()
    # def on_open_insp_setting_page(self):
    #     self.insp_setting_page = InspSettingWidget()
    #     self.insp_setting_page.back.clicked.connect(self.on_open_main_page)
    #     self.setCentralWidget(self.insp_setting_page)


