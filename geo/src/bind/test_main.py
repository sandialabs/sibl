# from myadd import add
# from xybind import myadd

import pytest

import xybind as xyb

# help(xyb.add)


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
