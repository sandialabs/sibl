# pybind11

## Motivation

* Reuse: Leverage existing C and C++ libraries in Python
* Performance: make Python faster by using C and C++
* Test: Verify C and C++ libraries with Python testing framework, e.g., `pytest`

## Introduction

* We focus on pybind11 because it focuses on C++ (not C), and is restricted to C++11.
* pybind11 enables:
  * binding: C++ to be used in Python 
    * (embedding: Python used in C++, which is not covered here)
* pybind11 uses C++ as the wrapper to the C++ code to be exposed in Python.
* pybind11 can expose date types that Python likes to use, such as tuples.

## Background

* A CPython extension module is a Python module *not* written in Python
  * Rather, it is typically written in C or C++
  * CPython provides an API to C

## Workflow

* [main.cpp](main.cpp)
* [setup.py](setup.py)
* **DEPRECATED(?)**:  [command_line_compile.sh](command_line_compile.sh) produces a file, for example, on macOS, as `xybind.cpython-39-darwin.so`, which can be now used in Python as

### Compile via pip install and `setup.py`

```bash
[sparta ~/sibl/geo/src/bind]$ pip install -e .
Obtaining file:///Users/sparta/sibl/geo/src/bind
  Preparing metadata (setup.py) ... done
Installing collected packages: xybind
  Attempting uninstall: xybind
    Found existing installation: xybind 0.0.2
    Uninstalling xybind-0.0.2:
      Successfully uninstalled xybind-0.0.2
  Running setup.py develop for xybind
Successfully installed xybind-0.0.2
```

### Run via pytest

```bash
[sparta ~/sibl/geo/src/bind]$ pytest test_xybind.py -v
==================================================== test session starts =====================================================
platform darwin -- Python 3.9.7, pytest-6.2.4, py-1.9.0, pluggy-0.12.0 -- /Users/sparta/opt/miniconda3/envs/siblenv/bin/python
cachedir: .pytest_cache
rootdir: /Users/sparta/sibl/geo/src/bind
plugins: cov-2.10.1
collected 7 items

test_xybind.py::test_version SKIPPED (not yet deployed)                                                                [ 14%]
test_xybind.py::test_add PASSED                                                                                        [ 28%]
test_xybind.py::test_subtract PASSED                                                                                   [ 42%]
test_xybind.py::test_multiply SKIPPED (work in progress)                                                               [ 57%]
test_xybind.py::test_attributes PASSED                                                                                 [ 71%]
test_xybind.py::test_power PASSED                                                                                      [ 85%]
test_xybind.py::test_pet PASSED                                                                                        [100%]

================================================ 5 passed, 2 skipped in 0.15s ================================================
[sparta ~/sibl/geo/src/bind]$
```

### Run via command line

```bash
> Python
>>> 
Python 3.9.7 (default, Sep 16 2021, 08:50:36)
[Clang 10.0.0 ] :: Anaconda, Inc. on darwin
Type "help", "copyright", "credits" or "license" for more information
>>> import xybind as xyb
>>> xyb.add(3, 4)
7
>>> xyb.subtract(4, 3)
1
```

## References

* C++ in Python the Easy Way! #pybind11 [video](https://youtu.be/_5T70cAXDJ0)
* Smallshire, Robert. *Integrate Python and C++ with pybind11*, 25 Sep 2018, NDC Conferences. [video](https://youtu.be/YReJ3pSnNDo)
  * Example is wrap of C++ library Computational Geometry Algorithms Library (CGAL) https://www.cgal.org
  * [Tutorial](mesher/README.md)
  * *"Even the author of SWIG recommends that you don't use SWIG anymore."* (3:40/48:19)
  * Exposes Conforming and Constrained Triangulations from CGAL.
  * Source: https://github.com/rob-smallshire/mesher
  * His books: https://leanpub.com/b/python-craftsman, with Austin Bingham and Sixty North
* Smirnov, Ivan.  *pybind11 - seamless operability between C++11 and Python*, 28 Oct 2017, EuroPython Conference. [video](https://youtu.be/jQedHfF1Jfw)
  * [code](https://github.com/pybind/python_example/blob/master/setup.py)
  * Problems with Cython (4:21 of 37:58)
    * Debugging is a huge **pain**
    * It is neither C nor Python
    * Two-line Cython translates into 2000 lines of C
    * Two build steps (.pyx -> .c -> .so)
    * Bad IDE support
    * Limited C++ support
