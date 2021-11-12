"""This module is a unit test of the polygon implementation.

To run
> conda activate siblenv
> cd ~/sibl
> pytest geo/tests/test_polygon.py -v

to run just a single text, for example
pytest geo/tests/test_polygon.py::test_is_left -v
"""

from itertools import repeat

# import itertools
from functools import partial

import pytest

import ptg.polygon as pg
import xybind as xyb


def test_using_xybind_version():
    assert xyb.__version__ == "0.0.2"


def test_too_few_coordinates():
    """Tests that a ValueError is raised if the number of points composing the boundary
    is less than three."""
    pairs = ((0.0, 0.0), (1.0, 0.0))  # two 2D points
    coords = pg.coordinates(pairs=pairs)
    with pytest.raises(ValueError):
        _ = pg.Polygon2D(boundary=coords)


def test_is_left():
    """Test that the is_left() function properly reports +1 for a point to the
    left of a line, 0, for a point on the line, and -1 for a point to the right
    of a line.
    """
    # Create a point directed toward the positive y-axis, intersecting p0 and p1.
    p0 = pg.Coordinate2D(x=2.0, y=10.0)
    p1 = pg.Coordinate2D(x=2.0, y=40.0)

    # Use map() with function that uses keyword arguments.
    # https://stackoverflow.com/questions/13499824/using-map-function-with-keyword-arguments
    mapfunc = partial(pg.is_left, P0=p0, P1=p1)

    # Create several test points, all to the left of the above-created line.
    pairs_left = ((0, 0), (1, 0), (1, 1), (-1, 1), (-1, -1), (1, -1))
    lefts = pg.coordinates(pairs=pairs_left)
    found = tuple(map(mapfunc, lefts))
    assert all([a == 1 for a in found])

    # Create several test points, all to the right of the above-created line.
    pairs_right = ((4, 0), (5, 0), (5, 1), (3, 1), (3, -1), (3, -1))
    rights = pg.coordinates(pairs=pairs_right)
    found = tuple(map(mapfunc, rights))
    assert all([a == -1 for a in found])

    # Create several test points, all on the above-created line.
    pairs_zero = ((2, 0), (2, 10), (2, 1), (2, -10), (2, -1), (2, -20))
    zeros = pg.coordinates(pairs=pairs_zero)
    found = tuple(map(mapfunc, zeros))
    assert all([a == 0 for a in found])


def test_winding_number():
    """Test the winding number method implementation."""

    # create a square polygon as a closed boundary in 2D, oriented counter-clockwise
    pairs = ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0))
    coords = pg.coordinates(pairs=pairs)
    pgon = pg.Polygon2D(boundary=coords)
    assert len(pgon._boundary) == 4

    # A point with a winding number of 1
    p = pg.Coordinate2D(x=0.5, y=0.5)
    result = pgon.winding_number(probe=p)
    assert result == 1

    # A point with a winding number of 0
    p = pg.Coordinate2D(x=7, y=5)
    result = pgon.winding_number(probe=p)
    assert result == 0

    # Test four edge cases
    # A bottom edge is considered in
    p = pg.Coordinate2D(x=0.5, y=0.0)
    result = pgon.winding_number(probe=p)
    assert result == 1

    # A right edge is considered out
    p = pg.Coordinate2D(x=1.0, y=0.5)
    result = pgon.winding_number(probe=p)
    assert result == 0

    # A top edge is considered out
    p = pg.Coordinate2D(x=0.5, y=1.0)
    result = pgon.winding_number(probe=p)
    assert result == 0

    # A left edge is considered in
    p = pg.Coordinate2D(x=0.0, y=0.5)
    result = pgon.winding_number(probe=p)
    assert result == 1

    # create a square polygon as a closed boundary in 2D, oriented counter-clockwise
    # that wraps around a probe point twice
    pairs = (
        (0.0, 0.0),
        (1.0, 0.0),
        (1.0, 1.0),
        (0.0, 1.0),
        (0.0, 0.0),
        (1.0, 0.0),
        (1.0, 1.0),
        (0.0, 1.0),
    )
    coords = pg.coordinates(pairs=pairs)
    pgon = pg.Polygon2D(boundary=coords)
    assert len(pgon._boundary) == 8

    # A point with a winding number of 1
    p = pg.Coordinate2D(x=0.5, y=0.5)
    result = pgon.winding_number(probe=p)
    assert result == 2

    # A point with a winding number of 0
    p = pg.Coordinate2D(x=7, y=5)
    result = pgon.winding_number(probe=p)
    assert result == 0

    # create a square polygon as a closed boundary in 2D, oriented clockwise
    # that wraps around a probe point twice
    pairs = (
        (1.0, 1.0),
        (1.0, 3.0),
        (3.0, 3.0),
        (3.0, 1.0),
        (1.0, 1.0),
        (1.0, 3.0),
        (3.0, 3.0),
        (3.0, 1.0),
    )
    coords = pg.coordinates(pairs=pairs)
    pgon = pg.Polygon2D(boundary=coords)
    assert len(pgon._boundary) == 8

    # A point with a winding number of 1
    p = pg.Coordinate2D(x=2.1, y=2.2)
    result = pgon.winding_number(probe=p)
    assert result == -2

    # A point with a winding number of 0
    p = pg.Coordinate2D(x=7, y=5)
    result = pgon.winding_number(probe=p)
    assert result == 0


@pytest.mark.skip(reason="Work in progress.")
def test_three_points_not_colinear():
    pass


@pytest.mark.skip(reason="Work in progress.")
def test_unit_square():
    """Tests if simple points are in the unit square."""

    # closed boundary in 2D counter-clockwise
    pairs = ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0))

    # closed boundary in 2D clockwise
    # pairs = ((0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0))
    coords = pg.coordinates(pairs=pairs)

    pgon = pg.Polygon2D(boundary=coords)
    assert len(pgon._boundary) == 4

    xs, ys = zip(*pairs)
    xyb_pgon = xyb.Polygon(xs, ys)

    """
    Test probe points p0, p1, ...

                        y
                        ^
                        |
                        |

                p12     p11  p10   p9      p8

              (0.0, 1.0)            (1.0, 1.0)
                p13     *----------*       p7
                        |          |
                p14     |          |       p6
                        |          |
                p15     *----------*       p5   --> x
              (0.0, 0.0)            (1.0, 0.0)

                p0      p1   p2   p3       p4
    """

    # test outside boundary
    px = (-1, 0, 0.5, 1, 2, 2, 2, 2, 2, 1, 0.5, 0, -1, -1, -1, -1)
    py = (-1, -1, -1, -1, -1, 0, 0.5, 1, 2, 2, 2, 2, 2, 1, 0.5, 1)
    assert len(px) == len(py)
    points = pg.coordinates(pairs=tuple(zip(px, py)))

    known = tuple(repeat(False, len(px)))
    found = pgon.contains(probes=points)
    assert known == found

    found_xybind = xyb_pgon.contains(probe_x=px, probe_y=px)
    assert list(known) == found_xybind

    # test inside boundary
    px = (0.25, 0.75, 0.75, 0.25)
    py = (0.25, 0.25, 0.75, 0.75)
    assert len(px) == len(py)
    points = pg.coordinates(pairs=tuple(zip(px, py)))

    known = tuple(repeat(True, len(px)))
    found = pgon.contains(probes=points)
    assert known == found

    found_xybind = xyb_pgon.contains(probe_x=px, probe_y=px)
    assert list(known) == found_xybind

    """
    # test on the boundary
    px = (0, 0.5, 1, 1, 1, 0.5, 0, 0)
    py = (0, 0, 0, 0.5, 1, 1, 1, 0.5)

    assert len(px) == len(py)
    points = pg.coordinates(pairs=tuple(zip(px, py)))

    known = tuple(repeat(True, len(px)))
    found = pgon.contains(probes=points)
    assert known == found
    """


@pytest.mark.skip(reason="Work in progress.")
def test_pentagon():
    """Tests the pentagon shape described in
    https://www.tutorialspoint.com/program-to-check-given-point-in-inside-or-boundary-of-given-polygon-or-not-in-python
    """
    # do counter-clockwise ordering, whereas the example page did a clockwise ordering
    pairs = ((0.0, 0.0), (4.0, 0.0), (6.0, 2.0), (4.0, 4.0), (1.0, 3.0))
    coords = pg.coordinates(pairs=pairs)

    pgon = pg.Polygon2D(boundary=coords)
    assert len(pgon._boundary) == 5  # a pentagon
    points = pg.coordinates(
        pairs=((0.0, 0.0), (1.0, -1.0), (3.0, 1.0), (5.0, 0.0), (5.0, 1.0), (6.0, 1.0))
    )

    known = (True, False, True, False, True, False)
    found = pgon.contains(probes=points)

    assert known == found
