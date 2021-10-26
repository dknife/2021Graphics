from OpenGL.GL import *
from OpenGL.GLU import *

import sys

from PyQt5.QtWidgets import QOpenGLWidget, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtWidgets import QGroupBox, QComboBox, QPushButton
from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter, QPen

import numpy as np

DEGREES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']

selected = 0


class MyGLWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super(MyGLWidget, self).__init__(parent)

    def initializeGL(self):
        # ^{\it \color{gray} OpenGL 그리기를 수행하기 전에 각종 상태값을 초기화}^
        glClearColor(0.8, 0.8, 0.6, 1.0)
        glPointSize(4)
        glLineWidth(2)
        glEnable(GL_BLEND)

    def resizeGL(self, width, height):
        # ^{\it \color{gray} 카메라의 투영 특성을 여기서 설정}^
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glBegin(GL_LINES)
        glVertex2f(-1.0, 0.0)
        glVertex2f( 1.0, 0.0)
        glVertex2f(0.0, -1.0)
        glVertex2f(0.0,  1.0)
        glEnd()

        self.draw_curve(-1, 1, selected)

        glFlush()

    def draw_curve(self, x, X, degree):
        nPoints = 100
        dx = (X-x)/nPoints
        glBegin(GL_LINE_STRIP)
        for i in range(nPoints):
            v = dx*i+x
            glVertex2f(v, v**degree)
            glVertex2f(v+dx, (v+dx)**degree)
        glEnd()
            


class MyWindow(QMainWindow):

    def __init__(self, title=''):
        QMainWindow.__init__(self)  # ^{\it \color{gray} call the init for the parent class}^
        self.setWindowTitle(title)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        gui_layout = QVBoxLayout()  

        central_widget.setLayout(gui_layout)

        self.glWidget = MyGLWidget() 
        degree_selection = QComboBox()
        for i in range(len(DEGREES)):
            degree_selection.addItem(DEGREES[i])

        gui_layout.addWidget(self.glWidget)
        gui_layout.addWidget(degree_selection)


        degree_selection.currentIndexChanged.connect(self.selectDegree)


    def selectDegree(self, value):
        global selected
        selected = value
        self.glWidget.update()


def main(argv=[]):
    app = QApplication(argv)
    window = MyWindow('Primitives')
    window.setFixedSize(400, 420)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv)
