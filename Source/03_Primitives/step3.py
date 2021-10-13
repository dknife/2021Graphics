# opengl 라이브러리 임포트
from OpenGL.GL import *
from OpenGL.GLU import *

# pyQt 임포트
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter, QPen

import sys
import numpy as np

PRIMITIVES = ['GL_POINTS', 'GL_LINES', 'GL_LINE_STRIP',
              'GL_LINE_LOOP', 'GL_TRIANGLES', 'GL_TRIANGLE_STRIP',
              'GL_TRIANGLE_FAN', 'GL_QUADS', 'GL_QUAD_STRIP', 'GL_POLYGON']

PRIMITIVE_VALUES = [GL_POINTS, GL_LINES, GL_LINE_STRIP,
              GL_LINE_LOOP, GL_TRIANGLES, GL_TRIANGLE_STRIP,
              GL_TRIANGLE_FAN, GL_QUADS, GL_QUAD_STRIP, GL_POLYGON]

selected = 0

points = [ [0, 0], [10, 10], [100, 50]]

class MyWindow(QMainWindow):
    def __init__(self, title=''):
        super().__init__()

        central_widget = QWidget()
        layout = QHBoxLayout()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(layout)

        # 1. OpenGL Widget
        self.opengl = MyGLWidget()
        # 2. Control Widget
        self.control = QGroupBox('Control')
        self.make_control()
        # 3. Painter Widget
        self.input = Drawer(parent = self)

        layout.addWidget(self.opengl)
        layout.addWidget(self.control)
        layout.addWidget(self.input)

    def make_control(self):
        control_layout = QVBoxLayout()
        selectCombo = QComboBox()
        resetButton = QPushButton('reset points', self)
        control_layout.addWidget(selectCombo)
        control_layout.addWidget(resetButton)
        self.control.setLayout(control_layout)
        
        for i in range( len(PRIMITIVES)) :
            selectCombo.addItem(PRIMITIVES[i])

        selectCombo.currentIndexChanged.connect(self.select)

    def select(self, value):
        global selected

        selected = value
        self.opengl.update()

class MyGLWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()

    def initializeGL(self):
        # OpenGL 그리기를 수행하기 전에 각종 상태값을 초기화
        glClearColor(0.8, 0.8, 0.6, 1.0)
    
    def resizeGL(self, w: int, h: int):
        # 카메라의 투영 특성을 여기서 설정
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # 새로운 렌즈를 사용한다.
        glOrtho(0, 250, 360, 0, -1, 1)

    def paintGL(self):
        
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        print(selected)
        glBegin(PRIMITIVE_VALUES[selected])
        for i in range(len(points)):
            glVertex2fv( points[i])
        glEnd()

class Drawer(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.painter = QPainter()

    def paintEvent(self, event):
        global points

        self.painter.begin(self)

        self.painter.setPen( QPen(Qt.red, 6))
        for i in range( len(points) ):
            self.painter.drawPoint( points[i][0], points[i][1] )

        self.painter.end()
    
    def mousePressEvent(self, event):
        points.append( [event.x(), event.y()] )
        self.update()
        self.parent.opengl.update()

def main():
    app = QApplication(sys.argv)
    win = MyWindow('My Primitive Test App')
    win.setFixedSize(800, 400)
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


