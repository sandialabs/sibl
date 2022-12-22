# Copyright 2020 National Technology and Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
# certain rights in this software.


import pkg_resources  # part of setup tools


def say_hello():
    print("hello world!")


def version() -> str:
    ver = pkg_resources.require("ptg")[0].version
    print("SIBL Mesh Engine, ptg package version:")
    return ver
