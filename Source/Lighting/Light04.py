from OpenGL.GL import *
from OpenGL.GLU import *

import sys

from PyQt5.QtWidgets import QOpenGLWidget, QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider
from PyQt5.QtCore import *

import numpy as np
import math

def LightSet():
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glMaterialfv(GL_FRONT, GL_AMBIENT, [1.0, 1.0, 0.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 127)

    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 0.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])

def LightPosition() :
    glLightfv(GL_LIGHT0, GL_POSITION, [1, 1, 1, 1])

class MyGLWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super(MyGLWidget, self).__init__(parent)
        self.center = np.array([0,0,0], dtype=float)
        self.verts = np.array([[-1,1,-1], [1, -1, -1], [1,1,1], [-1,-1,1]], dtype=float)
        self.angle = 0.0

    def initializeGL(self):
        # ^{\it \color{gray}  OpenGL 그리기를 수행하기 전에 각종 상태값을 초기화}^
        glClearColor(0.8, 0.8, 0.6, 1.0)
        glPointSize(10)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        LightSet()
        
    def resizeGL(self, width, height):
        # ^{\it \color{gray}  카메라의 투영 특성을 여기서 설정}^
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, width/height, 0.1, 1000)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x = 5.2*math.sin(self.angle)
        z = 5.2*math.cos(self.angle)
        gluLookAt(x, 2.0, z, 0,0,0, 0,1,0)
        LightPosition()

        # ^{\it \color{gray}  색과 프리미티브를 이용한 객체 그리기}^
        # ^{\it \color{gray}  광원의 색}^
        glBegin(GL_POINTS)
        glColor3f(0,0,0)
        glVertex3fv(self.center)
        for i in range(len(self.verts)):
            glColor3f(1,0,0)
            glVertex3fv(self.verts[i])
        glEnd()

     
        glColor3f(0, 0, 1)
        glLineWidth(3)
        nSub = 3
        draw_triangle(self.verts[0], self.verts[2], self.verts[1], subdivide=nSub)
        draw_triangle(self.verts[0], self.verts[3], self.verts[2], subdivide=nSub)
        draw_triangle(self.verts[2], self.verts[3], self.verts[1], subdivide=nSub)
        draw_triangle(self.verts[0], self.verts[1], self.verts[3], subdivide=nSub)
        glLineWidth(1)



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
    window.setFixedSize(600, 400)
    window.show()
    sys.exit(app.exec_())

def draw_triangle(v0, v1, v2, subdivide = 0):

    if subdivide <= 0:
        glColor3f(1, 1, 0)
        glBegin(GL_TRIANGLES)
        N = computeNormal(v0, v1, v2)
        glNormal3fv(N)
        glVertex3fv(v0)
        glVertex3fv(v1)
        glVertex3fv(v2)
        glEnd()
    else :
        v01 = v0 + v1
        v12 = v1 + v2
        v20 = v2 + v0
        l01 = np.linalg.norm(v01)  # v01이 원점에서 얼마나 떨어져 있는가
        l12 = np.linalg.norm(v12)  # v12이 원점에서 얼마나 떨어져 있는가
        l20 = np.linalg.norm(v20)  # v20이 원점에서 얼마나 떨어져 있는가
        
        root3 = math.sqrt(3.0)
        v01 = v01 * root3 / l01
        v12 = v12 * root3 / l12
        v20 = v20 * root3 / l20

        draw_triangle(v0, v01, v20, subdivide - 1)
        draw_triangle(v01, v1, v12, subdivide - 1)
        draw_triangle(v20, v12, v2, subdivide - 1)
        draw_triangle(v20, v01, v12, subdivide - 1)

def normalize(v):
    return v / np.linalg.norm(v)
    
def computeNormal(v0, v1, v2) :
    v01 = v1 - v0
    v02 = v2 - v0
    N = np.cross(v01, v02)
    l = np.linalg.norm(N)
    return N / l

if __name__ == '__main__':
    main(sys.argv)