#!/bin/bash 

# Linux and Python 3, produces xybind.cpython-36m-x86_64-linux.gnu.so
# c++ -O3 -Wall -Werror -shared -std=c++11 -fPIC $(python -m pybind11 --includes) main.cpp -o xybind$(python3-config --extension-suffix)

# macOS and Python 3, produces xybind.cpython-39-darwin.so
c++ -O3 -Wall -Werror -shared -std=c++11 -fPIC -undefined dynamic_lookup $(python -m pybind11 --includes) main.cpp -o xybind$(python3-config --extension-suffix)

# Windows - to be determined


# Reference
# https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Downloaded 
# Visual Studio with C++ Community 2019
# from
# https://visualstudio.microsoft.com/downloads/
# run
# VisualStudioSetup.exe

# chadh@Titan MINGW64 ~/sibl/geo/src/bind (master)
# $ pip install -e .
# Obtaining file:///C:/Users/chadh/sibl/geo/src/bind
#   Preparing metadata (setup.py): started
#   Preparing metadata (setup.py): finished with status 'done'
# Installing collected packages: xybind
#   Running setup.py develop for xybind
#     ERROR: Command errored out with exit status 1:
#      command: 'C:\Users\chadh\miniconda3\envs\siblenv\python.exe' -c 'import io, os, sys, setuptools, tokenize; sys.argv[0] = '"'"'C:\\Users\\chadh\\sibl\\geo\\src\\bind\\setup.py'"'"'; __file__='"'"'C:\\Users\\chadh\\sibl\\geo\\src\\bind\\setup.py'"'"';f = getattr(tokenize, '"'"'open'"'"', open)(__file__) if os.path.exists(__file__) else io.StringIO('"'"'from setuptools import setup; setup()'"'"');code = f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' develop --no-deps
#          cwd: C:\Users\chadh\sibl\geo\src\bind\
#     Complete output (11 lines):
#     running develop
#     running egg_info
#     writing xybind.egg-info\PKG-INFO
#     writing dependency_links to xybind.egg-info\dependency_links.txt
#     writing requirements to xybind.egg-info\requires.txt
#     writing top-level names to xybind.egg-info\top_level.txt
#     reading manifest file 'xybind.egg-info\SOURCES.txt'
#     writing manifest file 'xybind.egg-info\SOURCES.txt'
#     running build_ext
#     building 'xybind' extension
#     error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/
