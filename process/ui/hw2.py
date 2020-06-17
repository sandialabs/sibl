# hello world with PyQt5 and https://build-system.fman.io/pyqt5-tutorial

# from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtWidgets import QApplication, QLabel
app = QApplication([])
label = QLabel('Hello World!')
label.show()

app.exec_()
