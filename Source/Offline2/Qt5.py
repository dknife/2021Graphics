
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from OpenGL.GL import *
from OpenGL.GLU import *
import math
import sys

class MyOpenGLWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()

    def initializeGL(self):
        glClearColor(1.0, 1.0, 0.0, 1.0)        

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)

        n = 20
        theta = 2 * 3.141592 / n

        glBegin(GL_POLYGON)
        # n 개의 점을 그린다.
        for i in range(n):
            glVertex2f(math.cos(i*theta), math.sin(i*theta))
        glEnd()

    def resizeGL(self, w, h):
        pass

    def changeN(self, value):
        print(value)


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        glWidget = MyOpenGLWidget()
        slider = QSlider(Qt.Horizontal)

        container = QWidget()
        layout = QVBoxLayout()

        self.setCentralWidget(container)
        container.setLayout(layout)

        layout.addWidget(glWidget)
        layout.addWidget(slider)

        slider.valueChanged.connect(glWidget.changeN)
        


def main():
    app = QApplication(sys.argv)

    win = MyWindow()
    win.show()

    app.exec()

###################################
if __name__ == '__main__':
    main()