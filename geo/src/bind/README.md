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

The balance of this workflow, to include install, test, and interactive, is 
contained in [Lesson a00](../../doc/dual/lesson_a00.md).

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
