import sys
import random
from PySide2 import QtCore, QtWidgets, QtGui
# import PySide2.QtWidgets
# from PySide2.QtWidgets import (QApplication, QLabel, QPushButton, QVBoxLayout, QWidget)
# from PySide2.QtCore import Slot, Qt

# class MyWidget(QtWidgets.QWidget):
class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["(1) Hallo Welt", "(2) Hei maaila", "(3) Hola Mundo"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.counter = 0
        self.text = QtWidgets.QLabel("(0) Hello World")
        self.text.setAlignment(QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        # self.button.clicked.connect(self.magic)
        self.button.clicked.connect(self.magic)

    # @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

        # if self.counter == len(self.hello):
        #     self.counter = 0  # reset to original state
        # self.text.setText(self.hello[self.counter])
        # self.counter += 1

if __name__ == "__main__": 
    app = QtWidgets.QApplication([])
    # app = QtWidgets.QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())
