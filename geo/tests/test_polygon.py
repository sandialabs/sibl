"""This module is a unit test of the polygon implementation.

To run
> conda activate siblenv
> cd ~/sibl
> pytest geo/tests/test_polygon.py -v
"""

import ptg.polygon as pg

import pytest


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
    # pairs = ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0))  # closed boundary in 2D counter-clockwise
    pairs = (
        (0.0, 0.0),
        (0.0, 1.0),
        (1.0, 1.0),
        (1.0, 0.0),
    )  # closed boundary in 2D but clockwise
    coords = pg.coordinates(pairs=pairs)

    pgon = pg.Polygon2D(boundary=coords)
    assert len(pgon._boundary) == 4

    # test points that are either contained in the boundary or not
    # points = pg.coordinates(pairs=((0.5, 0.5), (1.5, 1.5)))
    points = pg.coordinates(pairs=((0.0, 0.0), (1.0, 1.0)))

    known = (True, False)
    found = pgon.contains(points=points)

    assert known == found


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
    found = pgon.contains(points=points)

    assert known == found
