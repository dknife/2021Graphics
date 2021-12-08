from OpenGL.GL import *
from OpenGL.GLU import *

import sys

from PyQt5.QtWidgets import QOpenGLWidget, QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider
from PyQt5.QtCore import *

import numpy as np
import math

    

class MyGLWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super(MyGLWidget, self).__init__(parent)
        self.angle = 0.0
        self.lightx = 0.0

    def initializeGL(self):
        # ^{\it \color{gray}  OpenGL 그리기를 수행하기 전에 각종 상태값을 초기화}^
        glClearColor(0.8, 0.8, 0.6, 1.0)
        glPointSize(1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        self.LightSet()

    def resizeGL(self, width, height):
        # ^{\it \color{gray}  카메라의 투영 특성을 여기서 설정}^
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, width/height, 0.1, 1000)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x = 15*math.sin(self.angle)
        z = 15*math.cos(self.angle)
        gluLookAt(x, 2.0, z, 0,0,0, 0,1,0)

        self.LightPosition()

        glBegin(GL_POINTS)
        glVertex3f(self.lightx, self.lightx, 5)
        glEnd()

        # ^{\it \color{gray}  그려진 프레임버퍼를 화면으로 송출}^
        glFlush()


    def set_angle(self, val):
        self.angle = 6.28*val/100
        self.update()
    
    def set_light(self, val):
        self.lightx = 6*(val-50)/50
        self.update()

    def LightSet(self):
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])
        glMaterialf(GL_FRONT, GL_SHININESS, 120)

        glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 0.0, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])

        glLightfv(GL_LIGHT1, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.0, 1.0, 1.0, 1.0])
        glLightfv(GL_LIGHT1, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])


    def LightPosition(self) :
        glLightfv(GL_LIGHT0, GL_POSITION, [self.lightx, self.lightx, 5, 1])
        glLightfv(GL_LIGHT1, GL_POSITION, [-self.lightx, -self.lightx, 5, 1])



class MyWindow(QMainWindow):

    def __init__(self, title = ''):
        QMainWindow.__init__(self)    # ^{\it \color{gray}  call the init for the parent class}^
        self.setWindowTitle(title)

        # ^{\it \color{gray}  GUI 설정}^

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        gui_layout = QVBoxLayout()   # ^{\it \color{gray}  CentralWidget에 사용될 수직 나열 레이아웃}^
                                     # ^{\it \color{gray}     배치될 것들 - GL Window + Control}^
        central_widget.setLayout(gui_layout)

        self.glWidget = MyGLWidget()  # ^{\it \color{gray}  OpenGL Widget}^
        gui_layout.addWidget(self.glWidget)

        angle_slider = QSlider(Qt.Horizontal)
        gui_layout.addWidget(angle_slider)
        angle_slider.valueChanged.connect(lambda val: self.glWidget.set_angle(val))

        light_slider = QSlider(Qt.Horizontal)
        gui_layout.addWidget(light_slider)
        light_slider.valueChanged.connect(lambda val: self.glWidget.set_light(val))


def main(argv = []):
    app = QApplication(argv)
    window = MyWindow('Tetrahedron Vertices')
    window.setFixedSize(1200, 800)
    window.show()
    sys.exit(app.exec_())

def normalize(v) :
    return v / np.linalg.norm(v)


def computeNormal(v0, v1, v2):
    a = v1 - v0
    b = v2 - v0
    N = np.cross(a, b)
    return N / np.linalg.norm(N)



if __name__ == '__main__':
    main(sys.argv)
