# Front End Development

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
> import PySide2.QtCore
> print(PySide2.__version__)  # 5.15.0
> print(PySide2.QtCore.__version__)  # 5.15.0
```

Next, [Create a Simple Application](https://doc.qt.io/qtforpython/quickstart.html#create-a-simple-application).

* Completed the `hello_world.py` app, but found inconsistency (works sometimes, doesn't work others) in the click callback.
* Will try moving from PySide2 to PyQt5, which seems to be more battle-tested.  
