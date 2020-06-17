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
from PySide2.QtCore import Qt

from PySide2.QtWidgets import (QApplication, QComboBox, QDialog, QFileDialog, QGridLayout, QHBoxLayout, QLabel, QPushButton)

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

class TraceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        fileOpenButton = QPushButton("&Open...")
        fileOpenButton.setDefault(True)
        fileOpenButton.clicked.connect(self.getfiles)

        self.recentComboBox = QComboBox()
        self.recentComboBox.addItem("<none>")
        self.recentComboBox.setDuplicatesEnabled(False)

        recentLabel = QLabel("&Input File:")
        recentLabel.setBuddy(self.recentComboBox)

        topLayout = QHBoxLayout()
        topLayout.addWidget(fileOpenButton)
        topLayout.addWidget(recentLabel)
        topLayout.addWidget(self.recentComboBox)

        # window = QWebView()
        window = QWebEngineView()
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        # canvas, axes, mark = tp.plot(x, y)
        canvas, axes, mark = toy.plot(x, y)
        # the_html = xml.etree.ElementTree.tostring(tp.html.render(canvas), method="html")
        # the_html = xml.etree.ElementTree.tostring(toyplot.html.render(canvas), method="html")
        html_content = xml.etree.ElementTree.tostring(toyhtml.render(canvas), method="html")
        # html_content = binary_html_content.decode('utf-8')
        # window.setHtml(xml.etree.ElementTree.tostring(tp.html.render(canvas), method="html"))
        midLayout = QHBoxLayout()
        # window.setHtml(the_html)
        # window.setHtml(html_content)
        window.setContent(html_content)
        # window.setHtml(html_content, method="html")
        # window.setContent(html_content, mimeType="html")
        midLayout.addWidget(window)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2, Qt.AlignLeft)
        mainLayout.addLayout(midLayout, 1, 0, 1, 2, Qt.AlignCenter)
        # mainLayout.addLayout(topLayout, 0, 0, 1, 1, Qt.AlignRight)
        mainLayout.setRowStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("PyTrace")

    def getfiles(self):
        # dlg = QFileDialog.getOpenFileName(self, 'Open file', '/', "csv files (*.csv)")
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        # dlg.setFilter("csv files (*.csv)")

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self.recentComboBox.addItem(filenames[0])

if __name__ == '__main__':
    app = QApplication([])

    dialog = TraceDialog()
    dialog.show()

    sys.exit(app.exec_())
