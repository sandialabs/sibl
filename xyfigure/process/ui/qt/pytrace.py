# PyTrace
import json
import sys
import xml
from pathlib import Path  # stop using os.path, use pathlib instead


# from PySide2 import QtCore, QtWidgets, QtGui, QtWebEngine
from PySide2.QtCore import Qt, QUrl, Slot

from PySide2.QtGui import QFont, QPalette

from PySide2.QtWidgets import (
    QAction,
    QApplication,
    QComboBox,
    QDialog,
    QFileDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from PySide2.QtWebEngineWidgets import QWebEngineView

import toyplot as toy
import toyplot.html as toyhtml
import numpy as np

# References
# https://build-system.fman.io/qt-designer-download
# https://build-system.fman.io/pyqt5-tutorial


class Widget(QWidget):
    def __init__(self):
        # super().__init__(self)
        QWidget.__init__(self)

        # model
        cwd = Path.cwd()
        # self.app_path = Path(".").resolve()
        self.app_path = Path(__file__).resolve().parent
        self.data_path = self.app_path.joinpath("../", "data").resolve()

        self.path_file_previous = (
            None  # revert current to previous model if next model fails
        )
        self.path_file_current = None
        # self.path_file_default = Path.joinpath(cwd, 'test_1234_quadratic.csv')
        # self.path_file_default = Path.joinpath(cwd, 'welcome.csv')
        self.path_file_default = Path.joinpath(self.data_path, "test-000-welcome.csv")
        self._index_x = 0
        self._index_y = 1

        # buttons, edit boxes, etc.
        self.button_file_open = QPushButton("&Open...")
        self.button_file_open.setDefault(True)
        self.button_file_open.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        #
        self.combo_box_recent_files = QComboBox()
        self.combo_box_recent_files.setDuplicatesEnabled(
            False
        )  # make certain singletons only, no duplicate items
        self.combo_box_recent_files.currentIndexChanged.connect(self.plot_update)

        self.window = QWebEngineView()
        self.window.setZoomFactor(0.95)
        self.window.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        # self.log.setStyleSheet("background-color: transparent;")
        # self.log.setMaximumBlockCount(2)
        self.log.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.log.appendPlainText("Welcome.")
        self.log.setMaximumHeight(100)  # maximum height in pixels

        # signals and slots
        self.button_file_open.clicked.connect(self.dialog_file_open)

        # layouts
        self.row_one = QHBoxLayout()
        self.row_one.addWidget(self.button_file_open)
        self.row_one.addWidget(self.combo_box_recent_files)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.row_one)
        self.layout.addWidget(self.window)
        self.layout.addWidget(self.log)
        self.setLayout(self.layout)

        # update model at end of initialization, trigger updates of views too
        self.files = []  # empty list
        self.models = []  # emtpy list
        self.model_update(self.path_file_default)

    @Slot()
    def dialog_file_open(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        # dlg.setFilter("csv files (*.csv)")

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            filename = Path(filenames[0])
            self.model_update(filename)
            a = 4

    @Slot()
    def model_update(self, path_file_new):
        if path_file_new in self.files:
            self.log.appendPlainText(
                f"Warning: selected file, {path_file_new}, is already open; not opened again."
            )
        else:
            self.log.appendPlainText(f"Model update from file: {path_file_new}")
            try:
                with open(path_file_new) as fin:
                    if path_file_new.suffix == ".json":
                        db = json.load(fin)
                        config_schema = [
                            "class",
                            "cal-path",
                            "cal-file",
                            "dat-path",
                            "dat-file",
                        ]
                        keys_present = 0
                        # check .json input schema
                        for kw in config_schema:
                            key = db.get(kw, None)
                            if not key:
                                self.log.appendPlainText(
                                    f"Error: keyword '{kw}' not found in the .json config file."
                                )
                            else:
                                keys_present += 1

                        files_and_folders_exist = False

                        cal_path = db.get("cal-path")
                        cal_path_expanded = Path(cal_path).expanduser()
                        cal_file = db.get("cal-file")

                        dat_path = db.get("dat-path")
                        dat_path_expanded = Path(dat_path).expanduser()
                        dat_file = db.get("dat-file")

                        if (
                            Path(cal_path_expanded).is_dir()
                            and Path(cal_path_expanded).joinpath(cal_file).is_file()
                            and Path(dat_path_expanded).is_dir()
                            and Path(dat_path_expanded).joinpath(dat_file).is_file()
                        ):
                            files_and_folders_exist = True
                        else:
                            raise ValueError("Invalid cal or dat paths or files.")

                        if (
                            keys_present == len(config_schema)
                            and files_and_folders_exist
                        ):
                            # all keys are present
                            new_data = [
                                [0.0, 1.0],
                                [1.0, 2.0],
                                [2.0, 4.0],
                                [3.0, 0.5],
                            ]
                        else:
                            raise ValueError(".json I/O error.")

                    else:  # then assume ".csv"
                        new_data = np.genfromtxt(
                            fin,
                            dtype="float",
                            delimiter=",",
                            skip_header=1,
                            usecols=(0, 1),
                        ).tolist()
                    self.models.append(new_data)

                self.files.append(path_file_new)
                self.combo_box_add(str(path_file_new))
                # self.plot_update()  # trigger from combobox currentIndexChanged
            except ValueError as error:
                # print(f'Error: {error}')
                # print(f'Unable to open file: {path_file_new}')
                self.log.appendPlainText(f"Error: {error}")
                self.log.appendPlainText(f"Unable to open file: {path_file_new}")

    @Slot()
    def combo_box_add(self, item):
        self.combo_box_recent_files.addItem(item)
        index = self.combo_box_recent_files.findText(item)
        self.combo_box_recent_files.setCurrentIndex(index)

    @Slot()
    def plot_update(self):
        print("Updating toyplot...")
        index = self.combo_box_recent_files.currentIndex()
        xymodel = self.models[index]
        x = [item[self._index_x] for item in xymodel]
        y = [item[self._index_y] for item in xymodel]

        canvas, axes, mark = toy.plot(x, y)
        base_url = QUrl("http://www.sandia.gov/toyplot")
        html_content = xml.etree.ElementTree.tostring(
            toyhtml.render(canvas), encoding="unicode", method="html"
        )
        self.window.setHtml(html_content, baseUrl=base_url)


class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.app_name = "PyTrace"
        self.app_version = "0.0.2"
        self.setWindowTitle(self.app_name)

        # menu container
        self.menu = self.menuBar()
        self.menu.setNativeMenuBar(
            False
        )  # avoid macOS menu style, put menu inside the app window
        # menu items
        self.file_menu = self.menu.addMenu("&File")
        self.help_menu = self.menu.addMenu("Help")

        # buttons

        # status bar
        self.statusBar()  # to come

        # actions
        # file_open_action = QAction('&Open file...', self)
        # file_open_action.triggered.connect(self.getfiles)
        # menu not appearing on macOS
        # see https://stackoverflow.com/questions/39574105/missing-menubar-in-pyqt5
        quit_action = QAction("&Quit", self)
        quit_action.triggered.connect(self.quit_app)
        #
        about_action = QAction("About", self)
        about_action.triggered.connect(self.about)

        # actions to menus
        # self.file_menu.addAction(file_open_action)
        self.file_menu.addAction(quit_action)
        self.help_menu.addAction(about_action)

        # main (central) widget
        self.setCentralWidget(widget)
        # self.setMinimumSize(800, 800)

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


if __name__ == "__main__":
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
    window.resize(1200, 800)
    window.show()

    sys.exit(app.exec_())
