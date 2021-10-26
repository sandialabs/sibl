"""
This python module is run on the command line to install
the ptgbind module as follows:

> conda activate siblenv
> pip install -e .
"""

from setuptools import setup, Extension
from setuptools.command import build_ext
from pybind11 import get_include

setup(
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    description="SIBL PTG binding to C++ extension",
    long_description="",
    maintainer="Chad B. Hovey",
    maintainer_email="chovey@sandia.gov",
    name="xybind",
    python_requires=">=3.9",
    url="https://github.com/sandialabs/sibl",
    version="0.0.1",
    ext_modules=[
        Extension(
            "xybind",
            ["myadd.cpp"],
            include_dirs=[get_include()],
            language="c++",
            extra_compile_args=["-std=c++11"],
        )
    ],
    cmdclass={"build_ext": build_ext.build_ext},
)
