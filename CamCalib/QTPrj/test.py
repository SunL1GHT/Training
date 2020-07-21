import sys
import PyQt5.QtWidgets as PQW
import PyQt5.QtGui as PQG

#########################################
# 1、QPushButton按钮控件
class PushButton(PQW.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建QColor对象，初始化颜色为黑色。RGB格式
        self.color = PQG.QColor(0, 0, 0)

        # 创建表示红色的QPushButton按钮
        redButton = PQW.QPushButton('红色',self)
        # 必须用setCheckable(True)才能让按钮可以设置两种状态。
        redButton.setCheckable(True)
        redButton.move(10,10)
        # 将setColor方法与按钮的单击事件关联，bool是一个类，表示setColor参数类型是一个布尔类型
        # 这个布尔类型的参数值表示按钮按下和抬起两种状态。
        redButton.clicked[bool].connect(self.setColor)

        # 创建表示绿色的QPushButton按钮
        greenButton = PQW.QPushButton('绿色',self)
        greenButton.setCheckable(True)
        greenButton.move(10,60)
        greenButton.clicked[bool].connect(self.setColor)

        # 创建表示蓝色的QPushButton按钮
        blueButton = PQW.QPushButton('蓝色',self)
        blueButton.setCheckable(True)
        blueButton.move(10,110)
        blueButton.clicked[bool].connect(self.setColor)

        # 创建用于显示当前颜色的QFrame对象。
        self.square = PQW.QFrame(self)
        self.square.setGeometry(150,20,100,100)
        # 设置QFrame的背景色。
        self.square.setStyleSheet("QWidget { background-color: %s }" % self.color.name())

        self.setGeometry(300,200,280,170)
        self.setWindowTitle('按钮控件')
        self.show()

    # 按钮的单击事件方法，3个按钮共享着一个方法。
    def setColor(self,pressed):
        # 获取单击的哪一个按钮
        source = self.sender()
        # pressed就是前面clicked[bool]中指定的布尔类型参数值。
        if pressed:
            val = 255
        else:
            val = 0
        # 遍历是哪个按钮操作
        if source.text()=='红色':
            self.color.setRed(val)
        elif source.text()=='绿色':
            self.color.setGreen(val)
        else:
            self.color.setBlue(val)

        self.square.setStyleSheet("QFrame {background-color: %s}" %self.color.name())

if __name__ == '__main__':
    app = PQW.QApplication(sys.argv)
    ex = PushButton()
    sys.exit(app.exec_())