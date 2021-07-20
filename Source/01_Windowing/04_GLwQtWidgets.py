from OpenGL.GL import *
from OpenGL.GLU import *

import sys

#from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QOpenGLWidget
from PyQt5.QtWidgets import QOpenGLWidget, QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import *

class MyGLWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super(MyGLWidget, self).__init__(parent)
        self.r = self.g = self.b = 0.0

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
        glColor3f(self.r, self.g, self.b)
        glBegin(GL_TRIANGLES)
        glVertex3fv([-1.0, 0.0, 0.0])
        glVertex3fv([ 1.0, 0.0, 0.0])
        glVertex3fv([ 0.0, 1.0, 0.0])
        glEnd()

        # 그려진 프레임버퍼를 화면으로 송출
        glFlush()

    def setR(self, val):
        self.r = val/99
        self.update()
    def setG(self, val):
        self.g = val/99
        self.update()
    def setB(self, val):
        self.b = val/99
        self.update()

class MyWindow(QMainWindow):

    def __init__(self, title = ''):
        QMainWindow.__init__(self)    # call the init for the parent class
        self.setWindowTitle(title)

        self.glWidget = MyGLWidget()

        ### GUI 설정
        gui_layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(gui_layout)

        self.setCentralWidget(central_widget)
        gui_layout.addWidget(self.glWidget)

        sliderX = QSlider(Qt.Horizontal)
        sliderX.valueChanged.connect(lambda val: self.glWidget.setR(val))

        sliderY = QSlider(Qt.Horizontal)
        sliderY.valueChanged.connect(lambda val: self.glWidget.setG(val))

        sliderZ = QSlider(Qt.Horizontal)
        sliderZ.valueChanged.connect(lambda val: self.glWidget.setB(val))

        gui_layout.addWidget(sliderX)
        gui_layout.addWidget(sliderY)
        gui_layout.addWidget(sliderZ)



def main(argv = []):
    app = QApplication(argv)
    window = MyWindow('GL with Qt Widgets')
    window.setFixedSize(600, 600)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv)
