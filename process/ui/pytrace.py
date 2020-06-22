# PyTrace
import sys
import xml

###   ### from PyQt5 import uic
###   from PyQt5.QtCore import Qt
###   # from PyQt5.QtWebKitWidgets import QWebView
###   from PyQt5.QtWebEngine import QtWebEngine
###   from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog, QFileDialog, QGridLayout, QHBoxLayout, QLabel, QPushButton)
###   # from PyQt5.QtWidgets.QWidget import QWebView
###   # from PtyQt5.QWebEngineView import QWebView
###   # from PyQt5.QtWidgets import QWebView
###   # from PyQt5.Qtweb

# from PySide2 import QtCore, QtWidgets, QtGui, QtWebEngine
from PySide2.QtCore import (Qt, QUrl, Slot)

from PySide2.QtWidgets import (QAction, QApplication, QComboBox, QDialog, QFileDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPlainTextEdit, QPushButton, QSizePolicy, QVBoxLayout, QWidget)

from PySide2.QtWebEngineWidgets import QWebEngineView


# import toyplot as tp
import toyplot as toy
import toyplot.html as toyhtml
import numpy as np

# References
# https://build-system.fman.io/qt-designer-download
# https://build-system.fman.io/pyqt5-tutorial

###  Form, Window = uic.loadUiType("pytrace.ui")
###  
###  app = QApplication([])
###  window = Window()
###  form = Form()
###  form.setupUi(window)
###  window.show()
###  app.exec_()

class Widget(QWidget):
    def __init__(self):
        # super().__init__(self)
        QWidget.__init__(self)

        self.edit = QLineEdit("Type your name here...")
        self.button = QPushButton("Show Greetings")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.edit)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        # signals and slots
        self.button.clicked.connect(self.greetings)

    @Slot()
    def greetings(self):
        print("Hello %s" % self.edit.text())



# class TraceDialog(QDialog):
class MainWindow(QMainWindow):
    # def __init__(self, parent=None):
    # def __init__(self):
    def __init__(self, widget):
        # super().__init__(parent)
        # super().__init__()
        # super().__init__(self)
        QMainWindow.__init__(self)
        self.setWindowTitle("PyTrace 0.0.2")

        # menu
        self.menu = self.menuBar()
        self.menu.setNativeMenuBar(False) # avoid macOS menu style, put menu inside the app window
        self.file_menu = self.menu.addMenu("&File")

        self.statusBar()

        # exit QAction
        # menu not appearing on macOS
        # exit_action = QAction("Exit", self)
        # see https://stackoverflow.com/questions/39574105/missing-menubar-in-pyqt5
        quit_action = QAction('&Quit', self)
        # exit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.quit_app)

        self.file_menu.addAction(quit_action)
        self.setCentralWidget(widget)

        # self.setMinimumSize(800, 800)

    @Slot()
    def quit_app(self, checked):
        QApplication.quit()

#         self.textEdit = QPlainTextEdit()
#         self.setCentralWidget(self.textEdit)
# 
#         self
# 
#         self.edit = QLineEdit("Type your name here...")
#         self.button = QPushButton("Show Greetings")
# 
#         layout = QVBoxLayout()
#         layout.addWidget(self.edit)
#         layout.addWidget(self.button)
# 
#         # self.setLayout(layout)
#         self.setLayout(layout)

# 
#         fileOpenButton = QPushButton("&Open...")
#         fileOpenButton.setDefault(True)
#         fileOpenButton.clicked.connect(self.getfiles)
# 
#         self.recentComboBox = QComboBox()
#         self.recentComboBox.addItem("<none>")
#         self.recentComboBox.setDuplicatesEnabled(False)
# 
#         recentLabel = QLabel("&Input File:")
#         recentLabel.setBuddy(self.recentComboBox)
# 
#         topLayout = QHBoxLayout()
#         topLayout.addWidget(fileOpenButton)
#         topLayout.addWidget(recentLabel)
#         topLayout.addWidget(self.recentComboBox)
# 
#         # window = QWebView()
#         window = QWebEngineView()
#         # window.setZoomFactor(0.95)
#         window.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#         x = np.linspace(0, 10, 100)
#         y = np.sin(x)
#         # canvas, axes, mark = tp.plot(x, y)
#         canvas, axes, mark = toy.plot(x, y)
#         # the_html = xml.etree.ElementTree.tostring(tp.html.render(canvas), method="html")
#         # the_html = xml.etree.ElementTree.tostring(toyplot.html.render(canvas), method="html")
#         # html_content = xml.etree.ElementTree.tostring(toyhtml.render(canvas), method="html")
#         base_url = QUrl("http://www.sandia.gov/toyplot")
#         html_content = xml.etree.ElementTree.tostring(toyhtml.render(canvas), encoding="unicode", method="html")
#         # html_content = binary_html_content.decode('utf-8')
#         # window.setHtml(xml.etree.ElementTree.tostring(tp.html.render(canvas), method="html"))
#         midLayout = QHBoxLayout()
#         # window.setHtml(the_html)
#         # window.setHtml(html_content)
#         # window.setContent(html_content, baseUrl=base_url)
#         window.setHtml(html_content, baseUrl=base_url)
#         # window.setHtml(html_content, method="html")
#         # window.setContent(html_content, mimeType="html")
#         midLayout.addWidget(window)
# 
#         # Layout of widgets on dialog box
#         mainLayout = QGridLayout()
#         # mainLayout.addWidget(fileOpenButton, 0, 0)
#         # mainLayout.addWidget(recentLabel, 1, 0)
#         # mainLayout.addWidget(self.recentComboBox, 2, 0)
#         mainLayout.addLayout(topLayout, 0, 0, 1, 1, Qt.AlignTop)
#         # mainLayout.addWidget(window, 1, 0)
#         mainLayout.addLayout(midLayout, 1, 0, 1, 1, Qt.AlignCenter)
# 
#         # mainLayout.addLayout(topLayout, 0, 0, 1, 2, Qt.AlignLeft)
#         # mainLayout.addLayout(midLayout, 1, 0, 1, 2, Qt.AlignCenter)
#         # mainLayout.addLayout(topLayout, 0, 0, 1, 1, Qt.AlignRight)
#         # mainLayout.setRowStretch(1, 1)
#         self.setLayout(mainLayout)


    def getfiles(self):
        # dlg = QFileDialog.getOpenFileName(self, 'Open file', '/', "csv files (*.csv)")
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        # dlg.setFilter("csv files (*.csv)")

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self.recentComboBox.addItem(filenames[0])

if __name__ == '__main__':
    # app = QApplication([])
    app = QApplication(sys.argv)  # this appears as newer syntax

    # dialog = TraceDialog()
    # dialog.show()

    # window = MainWindow()
    # window.show()

    widget = Widget()

    # QMainWindow using QWidget as the central widget
    window = MainWindow(widget)
    # window = MainWindow()
    window.resize(800, 600)
    window.show()


    sys.exit(app.exec_())
