from OpenGL.GL import *
from OpenGL.GLU import *

import sys

from PyQt5.QtWidgets import QOpenGLWidget, QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider
from PyQt5.QtCore import *

import numpy as np
import math

class MeshLoader():
    def __init__(self):
        self.nV = 0
        self.nF = 0

    def load(self, filename):
        with open(filename, "rt") as meshdata:
            self.nV = int(next(meshdata))
            print('total number of vertices = ', self.nV)
            self.verts = np.zeros(shape = (self.nV * 3, ), dtype = 'f')

            for i in range(self.nV) :
                start = i*3
                self.verts[start: start+3] = next(meshdata).split()

            self.nF = int(next(meshdata))
            print('total number of faces = ', self.nF)
            self.faces = np.zeros(shape = (self.nF * 3, ), dtype = 'i')

            for i in range(self.nF) :
                start = i*3
                self.faces[start: start+3] = next(meshdata).split()[1:4]


    def draw(self):
        glBegin(GL_POINTS)
        for i in range(self.nV):
            idx = i*3
            glVertex3fv(self.verts[idx: idx+3])
        glEnd()

        
        for i in range(self.nF):
            idx = i*3
            i0, i1, i2 = self.faces[idx: idx+3]
            glBegin(GL_LINE_LOOP)
            glVertex3fv(self.verts[i0*3:i0*3+3])
            glVertex3fv(self.verts[i1*3:i1*3+3])
            glVertex3fv(self.verts[i2*3:i2*3+3])
            glEnd()
    

class MyGLWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super(MyGLWidget, self).__init__(parent)
        self.mesh = MeshLoader()
        self.mesh.load('./Lighting/mesh.txt')
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

        self.mesh.draw()

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

def draw_triangle(v0, v1, v2, subdivide = 0):

    if subdivide <= 0:
        glColor3f(1, 1, 0)
        glBegin(GL_TRIANGLES)        
        glNormal3fv(computeNormal(v0, v1, v2))
        #glNormal3fv(normalize(v0))
        glVertex3fv(v0)
        #glNormal3fv(normalize(v1))
        glVertex3fv(v1)
        #glNormal3fv(normalize(v2))
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



if __name__ == '__main__':
    main(sys.argv)