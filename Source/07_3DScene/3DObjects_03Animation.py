
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QBasicTimer


from OpenGL.GL import *
from OpenGL.GLU import *
import math
import sys

class MyOpenGLWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self._timer = QBasicTimer()              # ^{\it \color{gray}타이머 생성}^
        self._timer.start(int(1000 / 60), self)  # ^{\it \color{gray}초당 60 프레임}^
        self.angle = 0.0

    def initializeGL(self):
        glClearColor(0.5, 0.5, 0.5, 1.0)        

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslate(0.5, 0, 0)
        glRotatef(self.angle, 0, 1, 0)
        draw_axes()
        
        glColor3f(1, 1, 0)
        glBegin(GL_LINE_LOOP)
        glVertex3f(-0.5, -0.5, 1)
        glVertex3f( 0.5, -0.5, 1)
        glVertex3f( 0.5,  0.5, 1)
        glVertex3f(-0.5,  0.5, 1)
        glEnd()

        glColor3f(0, 1, 1)
        glBegin(GL_LINE_LOOP)
        glVertex3f(-0.5, -0.5, 0)
        glVertex3f( 0.5, -0.5, 0)
        glVertex3f( 0.5,  0.5, 0)
        glVertex3f(-0.5,  0.5, 0)
        glEnd()
        
        glFlush()

    def resizeGL(self, w, h):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-2, 2, -2, 2, -2, 2)
        
    def timerEvent(self, QTimerEvent):
        self.angle += 1.0
        self.update()
        


def main():
    app = QApplication(sys.argv)

    win = MyOpenGLWidget()
    win.show()

    app.exec()

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