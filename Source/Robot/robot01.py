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
        glEnable(GL_DEPTH_TEST)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 5, 25, 0, 0, 0, 0, 1, 0)
        draw_axes()
        
        glColor3f(0.5, 0.5, 1.0)
        draw_plane(30, 30, 1.0)
        glColor3f(1.0, 1.0, 1.0)
        glTranslatef(0, 1, 0)
        draw_cube()


        glFlush()

    def resizeGL(self, w, h):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 1.0, 0.1, 100)
        
    def timerEvent(self, QTimerEvent):
        self.angle += 5.0
        self.update()
        


def main():
    app = QApplication(sys.argv)

    win = MyOpenGLWidget()
    win.show()

    app.exec()

def draw():
    glPushMatrix()
    glScalef(0.2, 0.2, 0.2)
    
    glBegin(GL_LINE_LOOP)
    glVertex3f(-1,-1, -1)
    glVertex3f( 2,-1, -1)
    glVertex3f( 2,-1,  1)
    glVertex3f(-1,-1,  1)
    glEnd()
    draw_cube()
    glPopMatrix()

def draw_plane(width, depth, interval):
    x, X = -width/2, width/2
    z, Z = -depth/2, depth/2
    cur = x
    glBegin(GL_LINES)
    while cur <= X: 
        glVertex3f(cur, 0, z)
        glVertex3f(cur, 0, Z)
        cur += interval
    cur = z
    while cur <= Z: 
        glVertex3f(x, 0, cur)
        glVertex3f(X, 0, cur)
        cur += interval
    glEnd()



def draw_square():
    glBegin(GL_LINE_LOOP)
    glVertex3f(-1,-1, 0)
    glVertex3f( 1,-1, 0)
    glVertex3f( 1, 1, 0)
    glVertex3f(-1, 1, 0)
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

def draw_cube():

    glPushMatrix()
    glTranslatef(0, 0, 1)
    draw_square()

    glTranslatef(0, 0, -2)
    draw_square()

    glTranslatef(0, 0, 1)
    glRotatef(90, 0, 1, 0)
    glTranslatef(0, 0, 1)
    draw_square()

    glTranslatef(0, 0, -2)
    draw_square()

    glTranslatef(0, 0, 1)
    glRotatef(90, 1,0,0)
    glTranslatef(0, 0, 1)
    draw_square()
    
    glTranslatef(0, 0, -2)
    draw_square()

    glPopMatrix()

###################################
if __name__ == '__main__':
    main()
