"""This module is a unit test of the xybind module.

To run
> conda activate siblenv
> cd ~/sibl/geo/src/bind
# > python setup.py develop  # no longer used
# > pip install -e .  # assumes already pip installed
> pytest test_xybind.py -v
"""


# from myadd import add
# from xybind import myadd

import pytest

import xybind as xyb

# help(xyb.add)


@pytest.mark.skip("not yet deployed")
def test_version():
    assert xyb.__version__ == "0.0.2"


def test_add():
    known = 7
    found = xyb.add(3, 4)
    assert known == found


def test_subtract():
    assert xyb.subtract(1, 2) == -1


@pytest.mark.skip("work in progress")
def test_multiply():
    # test not yet written
    pass


def test_attributes():
    known = 42
    found = xyb.the_answer
    assert known == found

    known = 0
    found = xyb.zero
    assert known == found


def test_power():
    a = 2.0
    b = 3.0
    known = a ** b

    found = xyb.exponent(base=a, exponent=b)
    assert known == found

    assert isinstance(found, float)


def test_pet():
    known = "Alice"
    p = xyb.Pet("Alice")
    found = p.name
    assert known == found

    # overwrite the name
    new_known = "Bob"
    p.name = "Bob"
    found = p.name
    assert new_known == found
