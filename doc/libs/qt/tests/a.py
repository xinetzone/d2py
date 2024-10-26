import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Slot, Signal, QObject

class Communicate(QObject):
    # create two new signals on the fly: one will handle
    # int type, the other will handle strings
    speak = Signal((int,), (str,))

    def __init__(self, parent=None):
        super().__init__(parent)

        self.speak[int].connect(self.say_something)
        self.speak[str].connect(self.say_something)

    # define a new slot that receives a C 'int' or a 'str'
    # and has 'say_something' as its name
    @Slot(int)
    @Slot(str)
    def say_something(self, arg):
        if isinstance(arg, int):
            print("This is a number:", arg)
        elif isinstance(arg, str):
            print("This is a string:", arg)

# class MyWidget(QtWidgets.QWidget):
class MyWidget(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(800, 600)
        self.scene = QtWidgets.QGraphicsScene()
        self.rect = self.scene.addRect(QtCore.QRectF(0, 0, 100, 100))
        self.item = self.scene.itemAt(50, 50, QtGui.QTransform())

        # self.pix = QtGui.QPixmap()
        # # 载入图片，如果成功加载了像素图，则返回`True`；否则会使像素图无效并返回 `False`
        # self.pix.load('/media/pc/data/board/arria10/lxw/tasks/images/bus.jpg') 
        # self.setPixmap(self.pix)

        picture = QtGui.QPicture()
        painter = QtGui.QPainter()
        painter.begin(picture)            # paint in picture
        painter.drawEllipse(10,20, 80,70) # draw an ellipse
        painter.end()                     # painting done
        picture.save("drawing.pic")       # save picture

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)
        self.button.clicked.connect(self.onButtonClick)
        self.button.clicked.connect(output)
        self.someone = Communicate()                                                                                                        
        
    def onButtonClick(self):
        # sender 是发送信号的对象
        sender = self.sender()
        print(sender.text() + ' 被按下了')

    @Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))
        self.someone.speak.emit(334)
        self.someone.speak[int].emit(33)
        self.someone.speak[str].emit("DDDDDD")
        

@Slot()
def output():
    """在控制台输出内容"""
    print("Button clicked")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec())
