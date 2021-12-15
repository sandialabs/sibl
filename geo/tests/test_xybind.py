"""This module is a unit test of the xybind module.

To run
> conda activate siblenv
> cd ~/sibl/geo/src/bind
# > python setup.py develop  # no longer used
# > pip install -e .  # assumes already pip installed
#
> cd ~/sibl/geo/tests
> pytest test_xybind.py -v
"""

# import pytest

import xybind as xyb


def test_version():
    assert xyb.__version__ == "0.0.3"


def test_add():
    known = 7
    found = xyb.add(3, 4)
    assert known == found


def test_subtract():
    assert xyb.subtract(1, 2) == -1


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


def test_unit_square_contains():
    """Tests if simple points are in the unit square via the xybind library."""

    # boundary coordinates
    bx = [0.0, 1.0, 1.0, 0.0]
    by = [0.0, 0.0, 1.0, 1.0]

    # boundary = xyb.Parade(bx, by)
    poly = xyb.Polygon(bx, by)

    # probe coordinates
    # TODO: need to investigate edge cases on boundary, since (1, 1) is known True
    # but tests as False.
    px = [-0.5, 0.0, 0.5, 0.9, 1.5]
    py = px

    known = [False, True, True, True, False]

    found = poly.contains(probe_x=px, probe_y=py)

    assert known == found

    # # pairs = ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0))  # closed boundary in 2D counter-clockwise
    # pairs = (
    #     (0.0, 0.0),
    #     (0.0, 1.0),
    #     (1.0, 1.0),
    #     (1.0, 0.0),
    # )  # closed boundary in 2D but clockwise
    # coords = pg.coordinates(pairs=pairs)

    # pgon = pg.Polygon2D(boundary=coords)
    # assert len(pgon._boundary) == 4

    # # test points that are either contained in the boundary or not
    # # points = pg.coordinates(pairs=((0.5, 0.5), (1.5, 1.5)))
    # points = pg.coordinates(pairs=((0.0, 0.0), (1.0, 1.0)))

    # known = (True, False)
    # found = pgon.contains(points=points)

    # assert known == found
