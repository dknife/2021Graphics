from OpenGL.GL import *
from OpenGL.GLU import *

import sys

from PyQt5.QtWidgets import QOpenGLWidget, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtWidgets import QGroupBox, QComboBox, QPushButton
from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter, QPen

import numpy as np

PRIMITIVES = ['GL_POINTS', 'GL_LINES', 'GL_LINE_STRIP', 'GL_LINE_LOOP',
              'GL_TRIANGLES', 'GL_TRIANGLE_STRIP', 'GL_TRIANGLE_FAN',
              'GL_QUADS', 'GL_QUAD_STRIP', 'GL_POLYGON']

PRIMITIVE_VALUES = [GL_POINTS, GL_LINES, GL_LINE_STRIP, GL_LINE_LOOP,
                    GL_TRIANGLES, GL_TRIANGLE_STRIP, GL_TRIANGLE_FAN,
                    GL_QUADS, GL_QUAD_STRIP, GL_POLYGON]
selected = 0

POINTS = [[0, 0], [10, 10], [100, 50]]

class MyGLWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super(MyGLWidget, self).__init__(parent)
        self.colors = []
        self.colors.append(np.array([0.0, 0.0, 0.0]))
        self.colors.append(np.array([0.0, 0.0, 0.0]))
        self.colors.append(np.array([0.0, 0.0, 0.0]))

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
        glOrtho(0, 240, 380, 0, -1, 1)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # ^{\it \color{gray} 색과 프리미티브를 이용한 객체 그리기}^
        glColor3f(1, 0, 0)
        glBegin(GL_POINTS)
        for i in range(len(POINTS)):
            glVertex2fv(POINTS[i])
        glEnd()

        glBegin(PRIMITIVE_VALUES[selected])
        nPoints = len(POINTS)
        for i in range(nPoints):
            glColor3f((1-i/nPoints), 0, i/nPoints)
            glVertex2fv(POINTS[i])
        glEnd()

        glColor4f(0, 1, 0, 0.1)
        glBegin(GL_LINE_STRIP)
        for i in range(len(POINTS)):
            glVertex2fv(POINTS[i])
        glEnd()

        # ^{\it \color{gray} 그려진 프레임버퍼를 화면으로 송출}^
        glFlush()


class MyWindow(QMainWindow):

    def __init__(self, title=''):
        QMainWindow.__init__(self)  # ^{\it \color{gray} call the init for the parent class}^
        self.setWindowTitle(title)

        ### ^{\it \color{gray} GUI 설정}^

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        gui_layout = QHBoxLayout()  # ^{\it \color{gray} CentralWidget에 사용될 수직 나열 레이아웃}^
        # ^{\it \color{gray}    배치될 것들 - GL Window + Control}^
        central_widget.setLayout(gui_layout)

        self.glWidget = MyGLWidget()  # ^{\it \color{gray} OpenGL Widget}^
        gui_layout.addWidget(self.glWidget)

        self.controlGroup = QGroupBox('Vertex and Primitives')
        gui_layout.addWidget(self.controlGroup)

        control_layout = QVBoxLayout()
        self.controlGroup.setLayout(control_layout)
        primitive_selection = QComboBox()
        for i in range(len(PRIMITIVES)):
            primitive_selection.addItem(PRIMITIVES[i])

        # ^{\it \color{gray} ComboBox에 기능 연결}^
        primitive_selection.currentIndexChanged.connect(self.selectPrimitive)

        reset_button = QPushButton('reset vertices', self)
        reset_button.clicked.connect(self.resetPoints)

        control_layout.addWidget(primitive_selection)
        control_layout.addWidget(reset_button)

        self.canvas = Drawer(parent=self)
        gui_layout.addWidget(self.canvas)

    def selectPrimitive(self, text):
        global selected
        selected = int(text)
        self.glWidget.update()

    def resetPoints(self, btn):
        global POINTS
        POINTS = []
        self.glWidget.update()
        self.canvas.update()



class Drawer(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.painter = QPainter()

    def paintEvent(self, event):
        global POINTS

        self.painter.begin(self)
        self.painter.setPen(QPen(Qt.red, 6))

        for i in range(len(POINTS)):
            self.painter.drawPoint(POINTS[i][0], POINTS[i][1])

        self.painter.setPen(QPen(Qt.blue, 2))
        for i in range(len(POINTS) - 1):
            self.painter.drawLine(POINTS[i][0], POINTS[i][1], POINTS[i + 1][0], POINTS[i + 1][1])
        self.painter.end()

    def mousePressEvent(self, event):
        POINTS.append([event.x(), event.y()])
        print(event.x(), event.y())
        self.parent.glWidget.update()
        self.update()




def main(argv=[]):
    app = QApplication(argv)
    window = MyWindow('Primitives')
    window.setFixedSize(800, 400)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv)
