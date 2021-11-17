from PyQt5.QtWidgets import *
from PyQt5.QtCore import QBasicTimer, Qt


from OpenGL.GL import *
from OpenGL.GLU import *
import math
import sys

class MyOpenGLWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self._timer = QBasicTimer()              # ^{\it \color{gray}타이머 생성}^
        self._timer.start(int(1000 / 60), self)  # ^{\it \color{gray}초당 60 프레임}^
        self.angle = 45.0
        self.handangle = 45
        self.bending = 45.0
        self.locz = 0.0

    def initializeGL(self):
        glClearColor(0.5, 0.5, 0.5, 1.0)      
        glEnable(GL_DEPTH_TEST)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 8, 35, 0, 0, 0, 0, 1, 0)

        draw_axes()

        glColor3f(1, 1, 0)
        draw_sphere()

        glTranslatef(6, 0, 0)
        glColor3f(0, 1, 0)
        draw_sphere()

        glFlush()

    def resizeGL(self, w, h):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 1.0, 0.1, 100)
        

def main():
    app = QApplication(sys.argv)

    win = MyOpenGLWidget()
    win.show()

    app.exec()

def draw_sphere():
    glPushMatrix()
    slice = 8
    angle = 180 / slice
    
    for _ in range(slice):
        glRotatef(angle, 0, 1, 0)
        draw_circle()

    for _ in range(slice):
        glRotatef(angle, 1, 0, 0)
        draw_circle()
    glPopMatrix()

def draw_circle():
    angle = 0
    glBegin(GL_LINE_LOOP)
    while angle < 3.14159*2:
        glVertex3f(math.cos(angle), math.sin(angle), 0)
        angle += 0.1
    glEnd()

def draw_axes():
    #### 축 그리기
    glBegin(GL_LINES)
    glColor3f(1,0,0)
    glVertex3f(0,0,0)
    glVertex3f(1,0,0)
    glColor3f(0,1,0)
    glVertex3f(0,0,0)
    glVertex3f(0,1,0)
    glColor3f(0,0,1)
    glVertex3f(0,0,0)
    glVertex3f(0,0,1)
    glEnd()

###################################
if __name__ == '__main__':
    main()
