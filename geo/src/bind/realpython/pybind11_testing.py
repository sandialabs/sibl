#!/usr/bin/env python
# from .pybind11_example import cpp_function as pbcppj
# import .pybind11_example as pb
# from import pybind11_example as pb
import pybind11_example as pb

if __name__ == "__main__":
    # Sample data for our call:
    x, y = 6, 2.3

    answer = pb.cpp_function(x, y)
    print(f"    In Python: int: {x} float {y:.1f} return val {answer:.1f}")
