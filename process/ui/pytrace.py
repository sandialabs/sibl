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

from PySide2.QtWidgets import (QAction, QApplication, QComboBox, QDialog, QFileDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMessageBox, QPlainTextEdit, QPushButton, QSizePolicy, QVBoxLayout, QWidget)

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

        # buttons and edit boxes
        self.file_open_button_w = QPushButton("&Open...")
        self.file_open_button_w.setDefault(True)
        # file_open_button.clicked.connect(self.getfiles)
        #
        self.edit = QLineEdit("Type your name here...")
        self.button = QPushButton("Show Greetings")

        # actions
        # file_open_action_w = QAction('&Open file...', self)
        # file_open_action_w.triggered.connect(self.getfiles_w)

        # actions to buttons
        # self.file_open_button_w.addAction(file_open_action_w)

        # signals and slots
        self.file_open_button_w.clicked.connect(self.getfiles_w)
        self.button.clicked.connect(self.greetings)

        # layouts
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.file_open_button_w)
        self.layout.addWidget(self.edit)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    @Slot()
    def getfiles_w(self):
        # dlg = QFileDialog.getOpenFileName(self, 'Open file', '/', "csv files (*.csv)")
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        # dlg.setFilter("csv files (*.csv)")

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            # self.recentComboBox.addItem(filenames[0])

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
        self.app_name = "PyTrace"
        self.app_version = "0.0.2"
        # self.setWindowTitle("PyTrace 0.0.2")
        # self.setWindowTitle(self.app_name + ' ' + self.app_version)
        self.setWindowTitle(self.app_name)

        # menu container
        self.menu = self.menuBar()
        self.menu.setNativeMenuBar(False) # avoid macOS menu style, put menu inside the app window
        # menu items
        self.file_menu = self.menu.addMenu("&File")
        self.help_menu = self.menu.addMenu("Help")

        # buttons

        # status bar
        self.statusBar()

        # actions
        file_open_action = QAction('&Open file...', self)
        file_open_action.triggered.connect(self.getfiles)
        # menu not appearing on macOS
        # see https://stackoverflow.com/questions/39574105/missing-menubar-in-pyqt5
        quit_action = QAction('&Quit', self)
        quit_action.triggered.connect(self.quit_app)
        #
        about_action = QAction('About', self)
        about_action.triggered.connect(self.about)

        # actions to menus
        self.file_menu.addAction(file_open_action)
        self.file_menu.addAction(quit_action)
        self.help_menu.addAction(about_action)

        # main (central) widget
        self.setCentralWidget(widget)
        # self.setMinimumSize(800, 800)

    @Slot()
    def getfiles(self):
        # dlg = QFileDialog.getOpenFileName(self, 'Open file', '/', "csv files (*.csv)")
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        # dlg.setFilter("csv files (*.csv)")

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            # self.recentComboBox.addItem(filenames[0])

    @Slot()
    def about(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        txt_github = "<a href='https://github.com/sandialabs/sibl'>SIBL</a>"

        txt_copyright = "Copyright 2020 National Technology and Engineering Solutions of Sandia, LLC (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights in this software."

        msg.setTextFormat(Qt.RichText)  # makes the links clickable

        msg.setText(self.app_name + " is distributed by " + txt_github)

        msg.setInformativeText("Version " + self.app_version + "\n\n" + txt_copyright)
        msg.setWindowTitle(self.app_name)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

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
