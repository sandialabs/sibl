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

__version__ = "0.0.8"

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


"""
Copyright 2023 Sandia National Laboratories

Notice: This computer software was prepared by National Technology and Engineering Solutions of
Sandia, LLC, hereinafter the Contractor, under Contract DE-NA0003525 with the Department of Energy
(DOE). All rights in the computer software are reserved by DOE on behalf of the United States
Government and the Contractor as provided in the Contract. You are authorized to use this computer
software for Governmental purposes but it is not to be released or distributed to the public.
NEITHER THE U.S. GOVERNMENT NOR THE CONTRACTOR MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR ASSUMES
ANY LIABILITY FOR THE USE OF THIS SOFTWARE. This notice including this sentence must appear on any
copies of this computer software. Export of this data may require a license from the United States
Government.
"""
