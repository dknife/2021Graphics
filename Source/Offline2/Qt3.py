
from PyQt5.QtWidgets import *
import sys

class MyOpenGLWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()

def main():
    app = QApplication(sys.argv)

    win = MyOpenGLWidget()
    win.show()

    app.exec()

###################################
if __name__ == '__main__':
    main()
    

