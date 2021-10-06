
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget
import sys

class MainWindow(QMainWindow) :
    def __init__(self) :
        super().__init__()

        self.setWindowTitle('Hello World')

        
        label = QLabel('This is a text label')
        l_edit = QLineEdit()

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(l_edit)

        view = QWidget()
        view.setLayout(layout)

        self.setCentralWidget(view)

        l_edit.textChanged.connect(label.setText)



app = QApplication(sys.argv)

win = MainWindow()
win.show()

app.exec()

