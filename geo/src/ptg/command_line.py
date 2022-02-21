import pkg_resources  # part of setup tools


def say_hello():
    print("hello world!")


def version() -> str:
    ver = pkg_resources.require("ptg")[0].version
    print("SIBL Mesh Engine, ptg package version:")
    return ver
