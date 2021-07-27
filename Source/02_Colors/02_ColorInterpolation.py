from OpenGL.GL import *
from OpenGL.GLU import *

import sys

#from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QOpenGLWidget
from PyQt5.QtWidgets import QOpenGLWidget, QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QGroupBox, QGridLayout, QSlider
from PyQt5.QtCore import *

import numpy as np

class MyGLWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super(MyGLWidget, self).__init__(parent)
        self.colors = []
        self.colors.append(np.array([0.0, 0.0, 0.0]))
        self.colors.append(np.array([0.0, 0.0, 0.0]))
        self.colors.append(np.array([0.0, 0.0, 0.0]))

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
        glBegin(GL_TRIANGLES)
        glColor3fv(self.colors[0])
        glVertex3fv([ 0.0, 1.0, 0.0])
        glColor3fv(self.colors[1])
        glVertex3fv([-1.0, 0.0, 0.0])
        glColor3fv(self.colors[2])
        glVertex3fv([ 1.0, 0.0, 0.0])
        glEnd()

        # 그려진 프레임버퍼를 화면으로 송출
        glFlush()

    def setColor(self, point, channel, val):
        self.colors[point][channel] = val/99
        self.update()

class MyWindow(QMainWindow):

    def __init__(self, title = ''):
        QMainWindow.__init__(self)    # call the init for the parent class
        self.setWindowTitle(title)

        ### GUI 설정

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        gui_layout = QVBoxLayout()   # CentralWidget에 사용될 수직 나열 레이아웃
                                     #    배치될 것들 - GL Window + Control
        central_widget.setLayout(gui_layout)

        self.glWidget = MyGLWidget()  # OpenGL Widget
        gui_layout.addWidget(self.glWidget)

        self.controlGroup = QGroupBox('Control')
        gui_layout.addWidget(self.controlGroup)

        control_layout = QGridLayout()
        self.controlGroup.setLayout(control_layout)

        for i in range(3):     # 3 points
            for j in range(3): # RGB
                slider = QSlider(Qt.Horizontal)
                name = '{} {}'.format(i, j)
                slider.setObjectName(name)
                slider.valueChanged.connect(self.changeColor)
                control_layout.addWidget(slider, j, i)


    def changeColor(self, value):
        i,j = self.sender().objectName().split()
        self.glWidget.setColor(int(i),int(j), value)

def main(argv = []):
    app = QApplication(argv)
    window = MyWindow('Color Interpolation')
    window.setFixedSize(400, 800)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv)
