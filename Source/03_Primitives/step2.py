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