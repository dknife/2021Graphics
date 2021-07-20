from OpenGL.GL import *
from OpenGL.GLU import *

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QOpenGLWidget


class MyGLWindow(QOpenGLWidget):

    def __init__(self, parent=None):
        super(MyGLWindow, self).__init__(parent)

    def initializeGL(self):
        # OpenGL 그리기를 수행하기 전에 각종 상태값을 초기화
        glClearColor(0.8, 0.8, 0.6, 1.0)

    def resizeGL(self, width, height):
        # 카메라의 투영 특성을 여기서 설정
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # 색과 프리미티브를 이용한 객체 그리기
        glColor3f(0.5, 0.5, 0.8)
        glBegin(GL_TRIANGLES)
        glVertex3fv([-1.0, 0.0, 0.0])
        glVertex3fv([ 1.0, 0.0, 0.0])
        glVertex3fv([ 0.0, 1.0, 0.0])
        glEnd()

        # 그려진 프레임버퍼를 화면으로 송출
        glFlush()

def main(argv = []):
    app = QApplication(argv)
    window = MyGLWindow()
    window.setWindowTitle('Example1')
    window.setFixedSize(600, 600)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv)
