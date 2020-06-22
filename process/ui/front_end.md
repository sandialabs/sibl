# Front End Development

## 2020-06-22 PySide2 Tutorials and Examples

* [Tutorials](https://doc.qt.io/qtforpython/tutorials/index.html)
* [Examples](https://doc.qt.io/qtforpython/examples/index.html)
  * [Application Example](https://doc.qt.io/qtforpython/overviews/qtwidgets-mainwindows-application-example.html)

## 2020-06-17 Move from PySide2 to PyQt5 

*and then back again to PySide2, with end-of-day discovery*

* PySide2 is newer but with identical API to PyQt, which is still supported, and been widely tested and proven over time.

### References

* [PyQt5 versus PySide2](https://www.learnpyqt.com/blog/pyqt5-vs-pyside2/)
* [PyPi install of PyQt5 5.15.0 by Phil Thompson](https://pypi.org/project/PyQt5/), version 5.15.0 was released 2020-05-31.
* [PyQt5 Reference Guide](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
* [PyQt5 tutorial with fman build system](https://build-system.fman.io/pyqt5-tutorial)
* [PyQt5 examples 2020](https://github.com/pyqt/examples)
* [Qt for Python documentation 5.15.0](https://doc.qt.io/qtforpython/)

### Notes

Set up a virtual environment and install:

```bash 
$ cd ~/sibl/process/ui
# verify Python 3.5 at a minimum
$ python --version  # verify 3.7.6

# verify conda is installed
$ conda info

# update conda to the current version (4.8.3 as of 2020-06-16)
$ conda update conda

# assess the environments prior to making a new environment
$ conda env list

# create a virtual environment named 'pyqt5'
# which will be located at
# /Users/Apollo/opt/anaconda3/envs/pyqt5
$ conda create --name pyqt5

# verify the ui environment is now in the list
$ conda env list

# change from current env to ui env
$ conda activate pyqt5

# since Miniconda is minimal, install some basics
$ conda install pip scipy
$ conda list
$ pip install xyfigure
$ pip install PyQt5  # this is (55 MB)

# show details, which confirms PyQt5 version 5.15.0
$ pip show PyQt5

# Notice the `Location`.  This will install PyQt5 to
/Users/Apollo/opt/anaconda3/envs/pyqt5/lib/python3.8/site-packages/PyQt5
```

**Qt Designer** 

* From [fman](https://build-system.fman.io/qt-designer-download) didn't work because my Mac cannot verify the app publisher.
o, use the Designer.app from yesterday's PySide2 work instead: /Users/Apollo/opt/anaconda3/envs/ui/lib/python3.8/site-packages/PySide2/Designer.app

**Toyplot**

```bash
# Install Toyplot
(pyqt5) $ pip install toyplot  # installed version 0.19.0
```

**API Deficiency Discovered**  

* While Toyplot recommends embedding as a `QWebView` (see [here](https://toyplot.readthedocs.io/en/stable/embedding.html)), this no longer exists in PyQt 5.15.0.  
* Instead it appears [`QWebEngineView`](https://doc.qt.io/qtforpython/PySide2/QtWebEngineWidgets/QWebEngineView.html) has replaced it.  
* But PyQt5 doesn't (yet) implement this class (it is listed as [TODO](https://www.riverbankcomputing.com/static/Docs/PyQt5/api/qtwebengine/qtwebengine-module.html)); whereas, [PySide2] does.  So, now change back from PyQt5 to PySide2.

```bash
$ conda deactivate

$ conda activate ui
(ui) $ pip install toyplot  # installed version 0.19.0 
```

## 2020-06-16

Set up a virtual environment and install:

```bash 
$ cd ~/sibl/process/ui
# verify Python 3.7 at a minimum
$ python --version  # verify 3.7.6

# verify conda is installed
$ conda info

# update conda to the current version (4.8.3 as of 2020-06-16)
$ conda update conda

# assess the environments prior to making a new environment
$ conda env list

# create a virtual environment named 'ui'
$ conda create --name ui

# verify the ui environment is now in the list
$ conda env list

# change from current env to ui env
$ conda activate ui

# since Miniconda is minimal, install some basics
$ conda install pip scipy
$ conda list
$ pip install xyfigure
$ pip install PySide2  # this is (154 MB), it requires some install time

# show details of the PySide2 install
$ pip show PySide2

# Notice the `Location`.  This will install the Designer.app at
/Users/Apollo/opt/anaconda3/envs/ui/lib/python3.8/site-packages/PySide2/Designer.app
```

Test the Install:

```python
$ python
>>> import PySide2.QtCore
>>> print(PySide2.__version__)  # 5.15.0
>>> print(PySide2.QtCore.__version__)  # 5.15.0
```

Next, [Create a Simple Application](https://doc.qt.io/qtforpython/quickstart.html#create-a-simple-application).

* Completed the `hello_world.py` app, but found inconsistency (works sometimes, doesn't work others) in the click callback.
* Will try moving from PySide2 to PyQt5, which seems to be more battle-tested.  
