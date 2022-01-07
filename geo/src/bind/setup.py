"""
This python module is run on the command line to install
the xybind module as follows:

> conda activate siblenv
> cd ~/sibl/geo/src/bind
> pip install -e .

which will create, on macOS for example, xybind.cpython-39-darwin.so, which can
then be used as a library in Python code, e.g., see the test_main.py code
"""

from setuptools import setup

from pybind11.setup_helpers import Pybind11Extension, build_ext

__version__ = "0.0.7"

ext_modules = [
    Pybind11Extension(
        "xybind",
        [
            "main.cpp",
            "../dual/Curve.cpp",
            "../dual/QuadTree.cpp",
            "../dual/NodeList.cpp",
            "../dual/Mesh.cpp",
        ],
        # Example: passing in the version to the compiled code
        define_macros=[("VERSION_INFO", __version__)],
    ),
]


setup(
    name="xybind",
    version=__version__,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    description="SIBL PTG binding to C++ extension",
    long_description="",
    maintainer="Chad B. Hovey",
    maintainer_email="chovey@sandia.gov",
    url="https://github.com/sandialabs/sibl",
    ext_modules=ext_modules,
    extras_require={"test": "pytest"},
    cmdclass={"build_ext": build_ext},
    python_requires=">=3.9",
)
