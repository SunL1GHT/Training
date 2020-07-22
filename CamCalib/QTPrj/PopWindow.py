from PySide2.QtWidgets import QWidget, QPushButton, QApplication, QMessageBox, QGridLayout
from PySide2.QtGui import QIcon
from PySide2.QtCore import Signal, Slot

class MyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.btn_dialog01 = QPushButton('弹出自定义关于消息框')
        self.btn_dialog01.clicked.connect(self.openMessageBox01)
        self.btn_dialog02 = QPushButton('弹出关于Qt信息')
        self.btn_dialog02.clicked.connect(self.openMessageBox02)
        self.btn_dialog03 = QPushButton('弹出危急消息框')
        self.btn_dialog03.clicked.connect(self.openMessageBox03)
        self.btn_dialog04 = QPushButton('弹出信息消息框')
        self.btn_dialog04.clicked.connect(self.openMessageBox04)
        self.btn_dialog05 = QPushButton('弹出询问消息框')
        self.btn_dialog05.clicked.connect(self.openMessageBox05)
        self.btn_dialog06 = QPushButton('弹出警告消息框')
        self.btn_dialog06.clicked.connect(self.openMessageBox06)

        self.layout = QGridLayout()
        self.layout.addWidget(self.btn_dialog01, 1, 1)
        self.layout.addWidget(self.btn_dialog02, 1, 2)
        self.layout.addWidget(self.btn_dialog03, 1, 3)
        self.layout.addWidget(self.btn_dialog04, 2, 1)
        self.layout.addWidget(self.btn_dialog05, 2, 2)
        self.layout.addWidget(self.btn_dialog06, 2, 3)
        self.setLayout(self.layout)

    @Slot()
    def openMessageBox01(self):
        QMessageBox.about(self, '我是标题', '我是内容')

    @Slot()
    def openMessageBox02(self):
        QMessageBox.aboutQt(self)

    @Slot()
    def openMessageBox03(self):
        QMessageBox.critical(self, '我是标题', '我是内容')

    @Slot()
    def openMessageBox04(self):
        QMessageBox.information(self, '我是标题', '我是内容')

    @Slot()
    def openMessageBox05(self):
        print(QMessageBox.question(self, '我是标题', '我是内容'))

    @Slot()
    def openMessageBox06(self):
        QMessageBox().warning(self, '我是标题', '我是内容')


app = QApplication()
widget = MyWidget()
widget.show()
app.exec_()