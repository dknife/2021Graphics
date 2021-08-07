from OpenGL.GL import *
from OpenGL.GLU import *

import sys

from PyQt5.QtWidgets import QOpenGLWidget, QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider
from PyQt5.QtCore import *

import numpy as np
import math

def drawTriangle(v0, v1, v2, subdivision=0):
    if subdivision==0:
        glBegin(GL_LINE_LOOP)
        glVertex3fv(v0)
        glVertex3fv(v1)
        glVertex3fv(v2)
        glEnd()
    elif subdivision > 0:
        v01, v12, v20 = (v0 + v1), (v1+v2), (v2+v0)
        l01 = np.linalg.norm(v01)
        l12 = np.linalg.norm(v12)
        l20 = np.linalg.norm(v20)
        v01 /= l01
        v12 /= l12
        v20 /= l20
        drawTriangle(v0, v01, v20, subdivision = subdivision-1)
        drawTriangle(v01, v1, v12, subdivision = subdivision-1)
        drawTriangle(v20, v12, v2, subdivision = subdivision-1)
        drawTriangle(v01, v12, v20, subdivision = subdivision-1)
        

class MyGLWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super(MyGLWidget, self).__init__(parent)
        self.center = np.array([0,0,0], dtype=float)
        c = 1/math.sqrt(3)
        self.verts = np.array([[-c,c,-c], [c, -c, -c], [c,c,c], [-c,-c,c]], dtype=float)
        self.angle = 0.0

    def initializeGL(self):
        # ^{\it \color{gray}  OpenGL 그리기를 수행하기 전에 각종 상태값을 초기화}^
        glClearColor(0.8, 0.8, 0.6, 1.0)
        glPointSize(10)

    def resizeGL(self, width, height):
        # ^{\it \color{gray}  카메라의 투영 특성을 여기서 설정}^
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, width/height, 0.1, 10)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x = 2.2*math.sin(self.angle)
        z = 2.2*math.cos(self.angle)
        gluLookAt(x, 2.0, z, 0,0,0, 0,1,0)

        # ^{\it \color{gray}  색과 프리미티브를 이용한 객체 그리기}^
        # ^{\it \color{gray}  광원의 색}^
        glBegin(GL_POINTS)
        glColor3f(0,0,0)
        glVertex3fv(self.center)
        for i in range(len(self.verts)):
            glColor3f(1,0,0)
            glVertex3fv(self.verts[i])
        glEnd()

        glLineWidth(3)
        glColor3f(0,0,1)
        nSub =3
        drawTriangle(self.verts[0], self.verts[2], self.verts[1], subdivision = nSub)
        drawTriangle(self.verts[1], self.verts[2], self.verts[3], subdivision = nSub)
        drawTriangle(self.verts[3], self.verts[2], self.verts[0], subdivision = nSub)
        drawTriangle(self.verts[0], self.verts[1], self.verts[3], subdivision = nSub)
        
        
        # ^{\it \color{gray}  그려진 프레임버퍼를 화면으로 송출}^
        glFlush()

    def set_angle(self, val):
        self.angle = 6.28*val/100
        self.update()


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

def main(argv = []):
    app = QApplication(argv)
    window = MyWindow('Tetrahedron Vertices')
    window.setFixedSize(1200, 800)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv)
