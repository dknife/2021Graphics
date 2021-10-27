# import 
### OpenGL import 
from OpenGL.GL import *
from OpenGL.GLU import *
import sys

### PyQt import 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# global variables
selected = 0

# GL Widget
class MyGLWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()

    # 1. initGL
    def initializeGL(self):
        glClearColor(0.0, 0.0, 1.0, 1.0)
        glLineWidth(3)

    # 2. resizeGL
    def resizeGL(self, w: int, h: int):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

    # 3. paintGL
    def paintGL(self):
        glBegin(GL_LINES)
        glVertex2f(-1.0, 0.0)
        glVertex2f(1.0, 0.0)
        glEnd()


# Window Widget
class MyWindow(QMainWindow):
    def __init__(self, title=''):
        super().__init__()
        self.setWindowTitle(title)

        # 1. MyGLWidget 생성
        self.glWidget = MyGLWidget()

        # 2. Combo box 생성
        self.control = QComboBox()

        for i in range(100):
            self.control.addItem(str(i))

        # 3. 이 윈도의 central widget과 layout 생성
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # 4. layout에 1, 2에서 생성한 GLWidget/Combobox 달기
        layout.addWidget(self.glWidget)
        layout.addWidget(self.control)


# main function
def main(argv = []):
    app = QApplication(argv)
    window = MyWindow('Curves')
    window.setFixedSize(400, 420)
    window.show()
    sys.exit(app.exec_())


# calling main function
main(sys.argv)

