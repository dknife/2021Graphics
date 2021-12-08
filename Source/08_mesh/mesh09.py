from OpenGL.GL import *
from OpenGL.GLU import *

import sys

from PyQt5.QtWidgets import QOpenGLWidget, QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider
from PyQt5.QtCore import *

import numpy as np
import math

    

class MeshLoader():
    def __init__(self):
        self.nV, self.nF = 0, 0

    def load(self, filename):
        with open(filename, 'rt') as openFile:
            self.nV = int(next(openFile))
            print('number of verts = ', self.nV)
            
            self.verts = np.zeros( shape = (self.nV * 3, ) , dtype = 'f' )
            self.norms = np.zeros( shape = (self.nV * 3, ) , dtype = 'f' )
            for i in range(self.nV):
                start = i * 3
                self.verts[start : start+3] = next(openFile).split()

            self.nF = int(next(openFile))
            print('number of faces = ', self.nF)
            self.faces = np.zeros( shape = (self.nF * 3, ), dtype = 'i')
            for i in range(self.nF) :
                start = i * 3
                self.faces[start: start+3] = next(openFile).split()[1:4]
            
            self.setNormals()

    def setNormals(self):
        for i in range(self.nF) :
            i0, i1, i2 = self.faces[i*3 : i*3 + 3]
            v0 = self.verts[i0*3: i0*3 + 3]
            v1 = self.verts[i1*3: i1*3 + 3]
            v2 = self.verts[i2*3: i2*3 + 3] 
            N = computeNormal(v0, v1, v2)
            self.norms[i0 * 3: i0*3 + 3] += N
            self.norms[i1 * 3: i1*3 + 3] += N
            self.norms[i2 * 3: i2*3 + 3] += N

        for i in range(self.nV):
            length = np.linalg.norm(self.norms[i * 3: i*3 + 3])
            self.norms[i * 3: i*3 + 3] /= length

    def draw(self):


        glBegin(GL_TRIANGLES)
        for i in range(self.nF):
            idx = i * 3
            i0, i1, i2 = self.faces[idx: idx+3]
            v0 = self.verts[i0*3: i0*3 + 3]
            v1 = self.verts[i1*3: i1*3 + 3]
            v2 = self.verts[i2*3: i2*3 + 3] 
            n0 = self.norms[i0*3: i0*3 + 3]
            n1 = self.norms[i1*3: i1*3 + 3]
            n2 = self.norms[i2*3: i2*3 + 3] 

            glNormal3fv(n0)
            glVertex3fv(v0)
            glNormal3fv(n1)
            glVertex3fv(v1)
            glNormal3fv(n2)
            glVertex3fv(v2)
        glEnd()

    def draw_fast(self):
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.verts)
        glNormalPointer(GL_FLOAT, 0, self.norms)

        glDrawElements(GL_TRIANGLES, self.nF * 3, GL_UNSIGNED_INT, self.faces)

        
class MyGLWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super(MyGLWidget, self).__init__(parent)
        self.mesh = MeshLoader()
        self.mesh.load('./Mesh/mesh.txt') 

        self.camloc = np.array([0.0, 2.0, 10.0])
        self.viewAngle = 3*2*3.141592 / 4




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
        
        x, y, z = self.camloc
        cosine = math.cos(self.viewAngle)
        sine = math.sin(self.viewAngle)
        dir = np.array([cosine, 0, sine])

        gluLookAt(x, y, z, x+dir[0], y, z+dir[2], 0,1,0)

        self.LightPosition()


        self.mesh.draw_fast()

        # ^{\it \color{gray}  그려진 프레임버퍼를 화면으로 송출}^
        glFlush()


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
        glLightfv(GL_LIGHT0, GL_POSITION, [1, 1, 1, 0])
        glLightfv(GL_LIGHT1, GL_POSITION, [-1, 1, -1, 0])

    def keyPressEvent(self, e):
        k = e.key()
        if k == Qt.Key_W :
            self.camloc[2] -= 0.1
        if k == Qt.Key_S :
            self.camloc[2] += 0.1

        self.update()


def main():
    app = QApplication(sys.argv)

    win = MyGLWidget()
    win.show()

    app.exec()


def normalize(v) :
    return v / np.linalg.norm(v)


def computeNormal(v0, v1, v2):
    a = v1 - v0
    b = v2 - v0
    N = np.cross(a, b)
    return N / np.linalg.norm(N)


if __name__ == '__main__':
    main()
