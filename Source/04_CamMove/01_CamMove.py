from OpenGL.GL import *
from OpenGL.GLU import *

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QOpenGLWidget


class MyGLWindow(QOpenGLWidget):

    def __init__(self, parent=None):
        super(MyGLWindow, self).__init__(parent)

    def initializeGL(self):
        # ^{\it \color{gray} OpenGL 그리기를 수행하기 전에 각종 상태값을 초기화}^
        glClearColor(0.8, 0.8, 0.6, 1.0)
        glLineWidth(3)

    def resizeGL(self, width, height):
        # ^{\it \color{gray} 카메라의 투영 특성을 여기서 설정}^
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        asp = width/height
        gluPerspective(60, asp, 0.01, 100)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(2,2,2, 0,0,0, 0,1,0)

        # ^{\it \color{gray} 그려진 프레임버퍼를 화면으로 송출}^
        glBegin(GL_LINES)
        glColor3f(1, 0, 0)
        glVertex3f(0, 0, 0); glVertex3f(1, 0, 0)
        glColor3f(0, 1, 0)
        glVertex3f(0, 0, 0); glVertex3f(0, 1, 0)
        glColor3f(0, 0, 1)
        glVertex3f(0, 0, 0); glVertex3f(0, 0, 1)
        glEnd()

        glBegin(GL_TRIANGLES)
        glVertex3f(-0.5, 0, 0)
        glVertex3f( 0.5, 0, 0)
        glVertex3f( 0, 0.5, 0)
        glEnd()
        glFlush()

def main(argv = []):
    app = QApplication(argv)
    window = MyGLWindow()
    window.setWindowTitle('My First GL Window with Qt')
    window.setFixedSize(600, 600)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv)
