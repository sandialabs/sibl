"""This module allows Python setuptools to talk with CMake.

Example use:
> conda activate siblenv
> cd ~/sibl/geo/src/bind/mesher
> python setup.py develop  # install code so that code can be developed on the installation

⋊> ~/s/g/s/b/mesher on master ⨯ python setup.py develop                        (siblenv)  Sat Oct 30 11:56:46 2021
running develop
running egg_info
writing src/mesher.egg-info/PKG-INFO
writing dependency_links to src/mesher.egg-info/dependency_links.txt
writing top-level names to src/mesher.egg-info/top_level.txt
reading manifest file 'src/mesher.egg-info/SOURCES.txt'
writing manifest file 'src/mesher.egg-info/SOURCES.txt'
running build_ext
-- The C compiler identification is AppleClang 12.0.0.12000032
-- The CXX compiler identification is AppleClang 12.0.0.12000032
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: /Library/Developer/CommandLineTools/usr/bin/cc - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /Library/Developer/CommandLineTools/usr/bin/c++ - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- This project requires the CGAL library, and will not be compiled.
-- Configuring done
-- Generating done
CMake Warning:
  Manually-specified variables were not used by the project:

    CMAKE_LIBRARY_OUTPUT_DIRECTORY
    PYTHON_EXECUTABLE


-- Build files have been written to: /Users/sparta/sibl/geo/src/bind/mesher/build/temp.macosx-10.9-x86_64-3.9

Creating /Users/sparta/opt/miniconda3/envs/siblenv/lib/python3.9/site-packages/mesher.egg-link (link to src)
Adding mesher 0.1 to easy-install.pth file

Installed /Users/sparta/sibl/geo/src/bind/mesher/src
Processing dependencies for mesher==0.1
Finished processing dependencies for mesher==0.1

> python
>>> import mesher.cgal_mesher
"""

import os
import re
import sys
import platform
import subprocess

from distutils.version import LooseVersion
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the following extensions: "
                + ", ".join(e.name for e in self.extensions)
            )

        if platform.system() == "Windows":
            cmake_version = LooseVersion(
                re.search(r"version\s*([\d.]+)", out.decode()).group(1)
            )
            if cmake_version < "3.1.0":
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + extdir,
            "-DPYTHON_EXECUTABLE=" + sys.executable,
        ]

        cfg = "Debug" if self.debug else "Release"
        build_args = ["--config", cfg]

        if platform.system() == "Windows":
            cmake_args += [
                "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}".format(cfg.upper(), extdir)
            ]
            if sys.maxsize > 2 ** 32:
                cmake_args += ["-A", "x64"]
            build_args += ["--", "/m"]
        else:
            cmake_args += ["-DCMAKE_BUILD_TYPE=" + cfg]
            build_args += ["--", "-j2"]

        env = os.environ.copy()
        env["CXXFLAGS"] = '{} -DVERSION_INFO=\\"{}\\"'.format(
            env.get("CXXFLAGS", ""), self.distribution.get_version()
        )
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        # 2021-10-31: CBH debug start
        print(f"cmake_args: {cmake_args}\n")
        print(f"self.build_temp: {self.build_temp}\n")
        print("env dictionary contains:")
        for key, value in env.items():
            print(f"'{key}:' {value}")
        # 2021-10-31: CBH debug stop

        print("\ncheck call extensions")
        subprocess.check_call(
            ["cmake", ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env
        )

        print("check call build")
        subprocess.check_call(
            ["cmake", "--build", "."] + build_args, cwd=self.build_temp
        )
        print()  # Add an empty line for cleaner output


setup(
    name="mesher",
    version="0.1",
    author="Robert Smallshire",
    author_email="rob@sixty-north.com",
    description="Triangular meshes using CGAL",
    long_description="",
    packages=find_packages("src"),
    package_dir={"": "src"},
    ext_modules=[CMakeExtension("mesher/cgal_mesher")],
    cmdclass=dict(build_ext=CMakeBuild),
    zip_safe=False,
)
