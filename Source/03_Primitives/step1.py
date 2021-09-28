from OpenGL.GL import *
from OpenGL.GLU import *

import sys

from PyQt5.QtWidgets import QOpenGLWidget, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtWidgets import QGroupBox, QComboBox, QPushButton
from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter, QPen

import numpy as np



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

        self.canvas = Drawer(parent=self)
        gui_layout.addWidget(self.canvas)



class Drawer(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.painter = QPainter()




def main(argv=[]):
    app = QApplication(argv)
    window = MyWindow('Primitives')
    window.setFixedSize(800, 400)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv)
