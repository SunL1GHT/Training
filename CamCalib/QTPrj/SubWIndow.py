from PySide2 import QtWidgets
import sys

class Window2(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('子窗口')

        window2_widget = QtWidgets.QWidget() # 实例化一个widget控件
        window2_layout = QtWidgets.QVBoxLayout() # 实例化一个垂直布局层
        window2_widget.setLayout(window2_layout) # 设置widget控件布局为水平布局
        # 实例化3个按钮
        button_1 = QtWidgets.QPushButton('返回')
        button_2 = QtWidgets.QPushButton('退出')
        # button_3 = QtWidgets.QPushButton('按钮三')
        # 将按钮添加到水平布局中
        window2_layout.addWidget(button_1)
        window2_layout.addWidget(button_2)
        # window2_layout.addWidget(button_3)


        button_1.clicked.connect(self.open_old_window)
        button_2.clicked.connect(self.checkout)

        self.setCentralWidget(window2_widget) # 设置窗口的中央部件
    

    def open_old_window(self):
        # 实例化另外一个窗口
        self.mainwindow = MainWindow()
        # 显示新窗口
        self.mainwindow.show()
        # 关闭自己
        self.close()
    
    def checkout(self):
        self.close()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('窗口1')

        centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(centralWidget)

        button = QtWidgets.QPushButton('打开新窗口')
        button.clicked.connect(self.open_new_window)

        grid = QtWidgets.QGridLayout(centralWidget)
        grid.addWidget(button)

    def open_new_window(self):
        # 实例化另外一个窗口
        self.window2 = Window2()
        # 显示新窗口
        self.window2.show()
        # 关闭自己
        self.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())