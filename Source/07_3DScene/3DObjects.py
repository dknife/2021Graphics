
from PyQt5.QtWidgets import *


from OpenGL.GL import *
from OpenGL.GLU import *
import math
import sys

class MyOpenGLWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()

    def initializeGL(self):
        glClearColor(0.5, 0.5, 0.5, 1.0)        

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)

    def resizeGL(self, w, h):
        pass


def main():
    app = QApplication(sys.argv)

    win = MyOpenGLWidget()
    win.show()

    app.exec()

###################################
if __name__ == '__main__':
    main()
