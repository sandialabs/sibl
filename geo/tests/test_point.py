""" This module is a unit test of the Point implementation.
To run
> conda activate siblenv
> cd ~/sibl
> pytest geo/tests/test_point.py -v
"""

import pytest

from ptg.point import Point2D, Points
import ptg.point as pp


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


def test_mesh_point_string_to_tuple():
    """Point tests of a three strings in mesh format
    'x y z faceid'
    gets converted to a tuple of floats (x, y, z)."""
    given = ["0 0 0 5 \n", "0.5 0 0 2 \n", "1 0 0 3 \n"]
    desired = ((0.0, 0.0, 0.0), (0.5, 0.0, 0.0), (1.0, 0.0, 0.0))

    for (aa, bb) in zip(given, desired):
        assert pp.mesh_point_string_to_tuple(aa) == bb


def test_enumerated_tuple_to_inp_mesh_point_string():
    given = ((0.0, 0.0, 0.0), (0.5, 0.0, 0.0), (1.0, 0.0, 0.0))
    desired = ["1, 0.0, 0.0, 0.0\n", "2, 0.5, 0.0, 0.0\n", "3, 1.0, 0.0, 0.0\n"]

    for k, (gg, dd) in enumerate(zip(given, desired)):
        # assert(pp.enumerated_tuple_to_inp_mesh_point_string(k + 1, gg) == dd
        found = pp.enumerated_tuple_to_inp_mesh_point_string(k + 1, gg)
        assert found == dd


@pytest.mark.skip("work in progress")
def test_hex222_mesh_points_to_inp_points():
    """This test uses the hex222 mesh, which consists of a 3D cube with
    two hexahedral elements in the x, y, and z dimensions.

    given_points = [
        "0 0 0 5 \n",
        "0.5 0 0 2 \n",
        "1 0 0 3 \n",
        "0 0.5 0 5 \n",
        "0.5 0.5 0 1 \n",
        "1 0.5 0 3 \n",
        "0 1 0 5 \n",
        "0.5 1 0 4 \n",
        "1 1 0 4 \n",
        "0 0 0.5 5 \n",
        "0.5 0 0.5 2 \n",
        "1 0 0.5 3 \n",
        "0 0.5 0.5 5 \n",
        "0.5 0.5 0.5 0 \n",
        "1 0.5 0.5 3 \n",
        "0 1 0.5 5 \n",
        "0.5 1 0.5 4 \n",
        "1 1 0.5 4 \n",
        "0 0 1 6 \n",
        "0.5 0 1 6 \n",
        "1 0 1 6 \n",
        "0 0.5 1 6 \n",
        "0.5 0.5 1 6 \n",
        "1 0.5 1 6 \n",
        "0 1 1 6 \n",
        "0.5 1 1 6 \n",
        "1 1 1 6 \n",
    ]

    # hexahedral elements

    given_elements = [
        "1 2 5 4 10 11 14 13 1\n",
        "2 3 6 5 11 12 15 14 1\n",
        "4 5 8 7 13 14 17 16 1\n",
        "5 6 9 8 14 15 18 17 1\n",
        "10 11 14 13 19 20 23 22 1\n",
        "11 12 15 14 20 21 24 23 1\n",
        "13 14 17 16 22 23 26 25 1\n",
        "14 15 18 17 23 24 27 26 1\n",
    ]

    desired_points = [
        "1, 0.0, 0.0, 0.0\n",
        "2, 0.5, 0.0, 0.0\n",
        "3, 1.0, 0.0, 0.0\n",
        "4, 0.0, 0.5, 0.0\n",
        "5, 0.5, 0.5, 0.0\n",
        "6, 1.0, 0.5, 0.0\n",
        "7, 0.0, 1.0, 0.0\n",
        "8, 0.5, 1.0, 0.0\n",
        "9, 1.0, 1.0, 0.0\n",
        "10, 0.0, 0.0, 0.5\n",
        "11, 0.5, 0.0, 0.5\n",
        "12, 1.0, 0.0, 0.5\n",
        "13, 0.0, 0.5, 0.5\n",
        "14, 0.5, 0.5, 0.5\n",
        "15, 1.0, 0.5, 0.5\n",
        "16, 0.0, 1.0, 0.5\n",
        "17, 0.5, 1.0, 0.5\n",
        "18, 1.0, 1.0, 0.5\n",
        "19, 0.0, 0.0, 1.0\n",
        "20, 0.5, 0.0, 1.0\n",
        "21, 1.0, 0.0, 1.0\n",
        "22, 0.0, 0.5, 1.0\n",
        "23, 0.5, 0.5, 1.0\n",
        "24, 1.0, 0.5, 1.0\n",
        "25, 0.0, 1.0, 1.0\n",
        "26, 0.5, 1.0, 1.0\n",
        "27, 1.0, 1.0, 1.0\n",
    ]

    desired_elements = [
        "25, 1, 2, 5, 4, 10, 11, 14, 13\n",
        "26, 2, 3, 6, 5, 11, 12, 15, 14\n",
        "27, 4, 5, 8, 7, 13, 14, 17, 16\n",
        "28, 5, 6, 9, 8, 14, 15, 18, 17\n",
        "29, 10, 11, 14, 13, 19, 20, 23, 22\n",
        "30, 11, 12, 15, 14, 20, 21, 24, 23\n",
        "31, 13, 14, 17, 16, 22, 23, 26, 25\n",
        "32, 14, 15, 18, 17, 23, 24, 27, 26\n",
    ]
    """
