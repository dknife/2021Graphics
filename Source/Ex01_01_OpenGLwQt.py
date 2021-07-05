from OpenGL.GL import *
from OpenGL.GLU import *

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QOpenGLWidget


class Example1(QOpenGLWidget):

    def __init__(self, parent=None):
        super(Example1, self).__init__(parent)

    def initializeGL(self):
        glPolygonMode(GL_FRONT, GL_FILL)
        glPolygonMode(GL_BACK, GL_FILL)

        glShadeModel(GL_SMOOTH)
        glEnable(GL_NORMALIZE)

        glClearColor(0.5, 0.0, 0.0, 1.0)

        glClearDepth(1.0)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)

    def resizeGL(self, width, height):
        glGetError()

        aspect = width if (height == 0) else width / height

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, aspect, 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glColor(0, 0, 255)

        glPushMatrix()
        glTranslatef(0.0, 0.0, -5.0)
        self.Draw(1.0, 1.0, 1.0)
        glPopMatrix()
        glFlush()

    def Draw(self, x, y, z):
        point1 = [x / 2.0, y / 2.0, z / -2.0]
        point2 = [x / 2.0, y / 2.0, z / 2.0]
        point3 = [x / 2.0, y / -2.0, z / 2.0]
        point4 = [x / 2.0, y / -2.0, z / -2.0]
        point5 = [x / -2.0, y / -2.0, z / 2.0]
        point6 = [x / -2.0, y / 2.0, z / 2.0]
        point7 = [x / -2.0, y / 2.0, z / -2.0]
        point8 = [x / -2.0, y / -2.0, z / -2.0]

        glBegin(GL_QUADS)

        glVertex3fv(point1)
        glVertex3fv(point2)
        glVertex3fv(point6)
        glVertex3fv(point7)

        glVertex3fv(point3)
        glVertex3fv(point4)
        glVertex3fv(point8)
        glVertex3fv(point5)

        glVertex3fv(point2)
        glVertex3fv(point3)
        glVertex3fv(point5)
        glVertex3fv(point6)

        glVertex3fv(point7)
        glVertex3fv(point8)
        glVertex3fv(point4)
        glVertex3fv(point1)

        glVertex3fv(point6)
        glVertex3fv(point5)
        glVertex3fv(point8)
        glVertex3fv(point7)

        glVertex3fv(point1)
        glVertex3fv(point4)
        glVertex3fv(point3)
        glVertex3fv(point2)

        glEnd()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Example1()
    window.setWindowTitle('Example1')
    window.setFixedSize(600, 600)
    window.show()
    sys.exit(app.exec_())
