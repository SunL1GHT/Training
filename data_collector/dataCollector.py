# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import *
from PySide2.QtQuick import *
from PySide2.QtCore import *
from MainWindow import *


if __name__ == "__main__":
    app = QApplication([])
#    app.setStyleSheet(custom_style)
    window = MainWindow()
    # window.resize(1024, 600)
    # window.resize(1200,1000)
    # 2560*1440  desktop resolution
    # window.resize(860,520)
    window.resize(1920,1080)
    window.show()
    sys.exit(app.exec_())

