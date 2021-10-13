# opengl 라이브러리 임포트
from OpenGL.GL import *
from OpenGL.GLU import *

# pyQt 임포트
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter, QPen

import sys
import numpy as np

PRIMITIVES = ['GL_POINTS', 'GL_LINES', 'GL_LINE_STRIP',
              'GL_LINE_LOOP', 'GL_TRIANGLES', 'GL_TRIANGLE_STRIP',
              'GL_TRIANGLE_FAN', 'GL_QUADS', 'GL_QUAD_STRIP', 'GL_POLYGON']

PRIMITIVE_VALUES = [GL_POINTS, GL_LINES, GL_LINE_STRIP,
              GL_LINE_LOOP, GL_TRIANGLES, GL_TRIANGLE_STRIP,
              GL_TRIANGLE_FAN, GL_QUADS, GL_QUAD_STRIP, GL_POLYGON]

seleced = 0

class MyWindow(QMainWindow):
    def __init__(self, title=''):
        super().__init__()

        central_widget = QWidget()
        layout = QHBoxLayout()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(layout)

        # 1. OpenGL Widget
        self.opengl = MyGLWidget()
        # 2. Control Widget
        self.control = QGroupBox('Control')
        # 3. Painter Widget
        self.input = Drawer()

class MyGLWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()

class Drawer(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)


def main():
    app = QApplication(sys.argv)
    win = MyWindow('My Primitive Test App')
    win.setFixedSize(800, 400)
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


