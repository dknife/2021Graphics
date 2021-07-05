from OpenGL.GL import *
from OpenGL.GLU import *

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QOpenGLWidget


class Example1(QOpenGLWidget):

    def __init__(self, parent=None):
        super(Example1, self).__init__(parent)

    def initializeGL(self):
         glClearColor(0.5, 0.0, 0.0, 1.0)

    def resizeGL(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()


    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glColor(0, 0, 255)
        glBegin(GL_TRIANGLES)
        glVertex3fv([-1.0, 0.0, 0.0])
        glVertex3fv([ 1.0, 0.0, 0.0])
        glVertex3fv([ 0.0, 1.0, 0.0])
        glEnd()
        glFlush()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Example1()
    window.setWindowTitle('Example1')
    window.setFixedSize(600, 600)
    window.show()
    sys.exit(app.exec_())
