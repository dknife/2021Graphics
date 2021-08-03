from OpenGL.GL import *
from OpenGL.GLU import *

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QOpenGLWidget
from PyQt5.QtCore import QBasicTimer
import math

def drawAxes():
    glBegin(GL_LINES)
    glColor3f(1, 0, 0)
    glVertex3f(0, 0, 0); glVertex3f(1, 0, 0)
    glColor3f(0, 1, 0)
    glVertex3f(0, 0, 0); glVertex3f(0, 1, 0)
    glColor3f(0, 0, 1)
    glVertex3f(0, 0, 0); glVertex3f(0, 0, 1)
    glEnd()

class MyGLWindow(QOpenGLWidget):

    def __init__(self, parent=None):
        super(MyGLWindow, self).__init__(parent)
        self._timer = QBasicTimer()              # ^{\it \color{gray}타이머 생성}^
        self._timer.start(int(1000 / 60), self)  # ^{\it \color{gray}초당 60 프레임}^
        self.angle = 0.0

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
        gluLookAt(2.0 * math.cos(self.angle), 1.0, 2.0 * math.sin(self.angle),
                  0,0,0, 0,1,0)

        glBegin(GL_TRIANGLES)
        glVertex3f(-0.5, 0, 0)
        glVertex3f( 0.5, 0, 0)
        glVertex3f( 0, 0.5, 0)
        glEnd()
        drawAxes()

        # ^{\it \color{gray} 그려진 프레임버퍼를 화면으로 송출}^
        glFlush()

    def timerEvent(self, QTimerEvent):
        self.angle += 0.01
        self.update()

def main(argv = []):
    app = QApplication(argv)
    window = MyGLWindow()
    window.setWindowTitle('My First GL Window with Qt')
    window.setFixedSize(600, 600)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv)
