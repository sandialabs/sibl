"""This module is a unit test of the polygon implementation.

To run
> conda activate siblenv
> cd ~/sibl
> pytest geo/tests/test_polygon.py -v
"""

from itertools import repeat
import itertools

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
