# Bind C++ for use with Python

## Goals

With the *SIBL Mesh Engine* C++ source code, compile C++ **binding code** on macOS, Linux, and Windows to the `xybind` library for use with Python.

## Steps

### macOS

* Create the `xybind` library:

```bash
> conda activate siblenv
> cd ~/sibl/geo/src/bind
> pip install -e .
Obtaining file:///Users/chovey/sibl/geo/src/bind
  Preparing metadata (setup.py) ... done
Installing collected packages: xybind
  Attempting uninstall: xybind
    Found existing installation: xybind 0.0.7
    Uninstalling xybind-0.0.7:
      Successfully uninstalled xybind-0.0.7
  Running setup.py develop for xybind
Successfully installed xybind-0.0.7
```

* Test the `xybind` library:

```bash
> cd ~/sibl/geo/tests
> pytest test_xybind.py -v                                                     (siblenv)
===================================================== test session starts ======================================================
platform darwin -- Python 3.9.7, pytest-6.2.5, py-1.9.0, pluggy-0.12.0 -- /Users/chovey/opt/miniconda3/envs/siblenv/bin/python
cachedir: .pytest_cache
rootdir: /Users/chovey/sibl/geo
plugins: cov-2.10.1
collected 10 items

test_xybind.py::test_version PASSED                                               [ 10%]
test_xybind.py::test_add PASSED                                                   [ 20%]
test_xybind.py::test_subtract PASSED                                              [ 30%]
test_xybind.py::test_attributes PASSED                                            [ 40%]
test_xybind.py::test_power PASSED                                                 [ 50%]
test_xybind.py::test_pet PASSED                                                   [ 60%]
test_xybind.py::test_unit_square_contains PASSED                                  [ 70%]
test_xybind.py::test_unit_squares_inType PASSED                                   [ 80%]
test_xybind.py::test_qt_node_counts PASSED                                        [ 90%]
test_xybind.py::test_unit_circle_quad_mesh PASSED                                 [100%]

============================= 10 passed in 0.63s =======================================
```

* Run two methods from `xybind` interactively with Python:

```
> pythPython 3.9.7 (default, Sep 16 2021, 08:50:36)
[Clang 10.0.0 ] :: Anaconda, Inc. on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import xybind as xyb
>>> xyb.add(3, 4)
7
>>> xyb.subtract(3, 4)
-1
```


### Linux

Same as [macOS](#macos).

### Windows

* Replace the `acsokol` user name in the example with the user name and path as appropriate for your local environment.

```bash
> cd ~/sibl/geo/src/dual
> g++ -O3 -Wall -shared -std=c++11 -fPIC -fvisibility=hidden -IC:/Users/acsokol/Miniconda3/Include -IC:/Users/acsokol/Miniconda3/lib/site-packages/pybind11/include  main.cpp -o xybind.pyd -LC:/Users/acsokol/Miniconda3 -lpython39
```

#### Details

Split it up into a few different parts:

* First set of compiler flags are pretty standard, the two items that have required messing with were as follows:
  * The `visibility` flag which seems to be a newer pybind11 thing. 
  * The other is `Werror`, which I had to remove. It says to treat warnings as errors which we do not want.

```bash
> g++ -O3 -Wall -Werror -shared -std=c++11 -fPIC -fvisibility=hidden
```

#### Include Locations

These were the locations returned by the python include line, `$(python -m pybind11 --includes)`, that just runs nicely in Linux/macOS.  I loaded python and typed in the command to get the correct responses.

* `-IC:/Users/acsokol/Miniconda3/Include`
* `-IC:/Users/acsokol/Miniconda3/lib/site-packages/pybind11/include`
 
The list of cpp files to compile (later will include other cpp files) `main.cpp`.

This line gets filled in by `python-config` which didn't work either on windows, `xybind$(python3-config --extension-suffix)`.  The `pyd` seems to be a windows dll equivalent?? `xybind` name has to also appear in the `PYBIND11_MODULE(xybind, m)` line in the cpp file.
 
* `-o xybind.pyd`

This was the hangup for a long time, telling it where the `python39.dll` file was located and getting the correct syntax to link it. The capital `L` tells the compiler what folder to look in and the lower case `l` tells it the file with some assumed platform dependent extension.

* `-LC:/Users/acsokol/Miniconda3 -lpython39`

[Index](README.md)
