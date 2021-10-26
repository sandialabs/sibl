# pybind11 example

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

*See [Mermaid cheat sheet](https://jojozhuang.github.io/tutorial/mermaid-cheat-sheet/) for flow diagram examples.*

```mermaid
graph TD
  subgraph Create Python binding
    subgraph Create C++ library
      A1[my_library.hpp] -->B
      A2[my_library.cpp] -->B
      A3[tasks.py] -->|$ invoke build-cppmult| B(libcppmult.so)
    end
    B --> B2[pybind11_wrapper.cpp]
  end
  B2 -->|$ invoke build-pybind11| C(my_module.cpython-39-darwin.so)
  C -. use as module library in Python .-> D[my_python.py]
```

<img src="fig/mermaid_2021_10_26.png" alt="mermaid_2021_10_26" width="400px">

```Python
#!/usr/bin/env python
# my_python.py
from . import my_module as mm
```

## Configuration

```bash
> conda activate siblenv
> python -m pip install invoke
> python -m pip install pybind11
```

## Source Files

* [`cppmult.cpp`](../src/ptg/cppmult.cpp)
* [`cppmult.hpp`](../src/ptg/cppmult.hpp)
* [`tasks.py`](../src/ptg/tasks.py)
* [`pybind11_wrapper`](../src/ptg/pybind11_wrapper.cpp)

## Output Files 

*Tested on macOS 2021-10-25*

```bash
⋊> ~/s/g/s/ptg on master ◦ invoke build-cppmult                   (siblenv)  Mon Oct 25 18:48:52 2021
==================================================
= Building C++ Library
* Complete (Chad says hi!)
⋊> ~/s/g/s/ptg on master ◦
```

created `libcppmult.so` and

```bash
⋊> ~/s/g/s/ptg on master ◦ invoke build-pybind11             (siblenv) 665ms Mon Oct 25 18:50:11 2021
==================================================
= Building C++ Library
* Complete (Chad says hi!)
==================================================
= Building PyBind11 Module
* Complete
⋊> ~/s/g/s/ptg on master ◦
```

created `pybind11_example.cpython-39-darwin.so`.

## Testing File

*Dot not use the original name, `pybind11_test.py`, since this interferes with the `pytest -v` auto discovery used with continuous integration on this repository.*

* [`pybind11_testing.py`](../src/ptg/pybind11_testing.py)

```bash
⋊> ~/s/g/s/ptg on master ◦ python pybind11_testing.py                (siblenv)  Mon Oct 25 18:56:39 2021
    In cppmult: int 6 float 2.3 returning 13.8
    In Python: int: 6 float 2.3 return val 13.8
⋊> ~/s/g/s/ptg on master ◦
```

```bash
⋊> ~/s/g/s/ptg on master ◦ pwd
/Users/sparta/sibl/geo/src/ptg

⋊> ~/s/g/s/ptg on master ◦ python                                 (siblenv)  Mon Oct 25 19:01:32 2021

Python 3.9.5 (default, May 18 2021, 12:31:01)
[Clang 10.0.0 ] :: Anaconda, Inc. on darwin
Type "help", "copyright", "credits" or "license" for more information.

>>> import ptg.pybind11_example as pp
>>> dir(pp)
['__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'cpp_function']
>>> pp.__doc__
'pybind11 example plugin'
>>>
```

## References

* C++ in Python the Easy Way! #pybind11 [video](https://youtu.be/_5T70cAXDJ0)
* [Real Python](https://realpython.com/python-bindings-overview/#pybind11)
* [Real Python GitHub repo](https://github.com/realpython/materials/tree/master/python-bindings)
* Smallshire, Robert. Integrate Python and C++ with pybind11, 25 Sep 2018, NDC Conferences. [video](https://youtu.be/YReJ3pSnNDo)
  * Example is wrap of C++ library Computational Geometry Algorithms Library (CGAL) https://www.cgal.org
  * *"Even the author of SWIG recommends not to use SWIG anymore."*
  * Exposes Conforming and Constrained Triangulations from CGAL.
  * Source: https://github.com/rob-smallshire/mesher
* Smirnov, Ivan.  pybind11 - seamless operability between C++11 and Python, 28 Oct 2017, EuroPython Conference. [video](https://youtu.be/jQedHfF1Jfw)
  * [code](https://github.com/pybind/python_example/blob/master/setup.py)
  * Problems with Cython (4:21 of 37:58)
    * Debugging is a huge **pain**
    * It is neither C nor Python
    * Two-line Cython translates into 2000 lines of C
    * Two build steps (.pyx -> .c -> .so)
    * Bad IDE support
    * Limited C++ support