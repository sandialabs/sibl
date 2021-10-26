#!/bin/bash 


# Linux and Python 3, produces myadd.cpython-36m-x86_64-linux.gnu.so

# c++ -O3 -Wall -Werror -shared -std=c++11 -fPIC $(python -m pybind11 --includes) myadd.cpp -o myadd$(python3-config --extension-suffix)

# macOS and Python 3, produces myadd.cpython-39-darwin.so

c++ -O3 -Wall -Werror -shared -std=c++11 -fPIC -undefined dynamic_lookup $(python -m pybind11 --includes) myadd.cpp -o myadd$(python3-config --extension-suffix)
