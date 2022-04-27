""" This module is a unit test of the Point implementation.
To run
> conda activate siblenv
> cd ~/sibl
> pytest geo/tests/test_point.py -v
"""

from ptg.point import Point2D, Points


def test_points():

    pairs = ((0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0))
    pts = Points(pairs=pairs)

    knownx = tuple(p[0] for p in pairs)
    knowny = tuple(p[1] for p in pairs)

    foundx = pts.xs
    foundy = pts.ys

    assert knownx == foundx
    assert knowny == foundy

    assert pts.length == 4
    assert pts.pairs == pairs

    known_point2Ds = (
        Point2D(x=0.0, y=0.0),
        Point2D(x=1.0, y=1.0),
        Point2D(x=2.0, y=4.0),
        Point2D(x=3.0, y=9.0),
    )

    found_point2Ds = pts.points2D

    assert known_point2Ds == found_point2Ds
