""" This module is a unit test of the Point implementation.

To run:
conda activate siblenv
cd ~/sibl
pytest geo/tests/test_point.py -v

For coverage:
pytest geo/tests/test_point.py -v --cov=geo/src/ptg --cov-report term-missing

For black style:
black --check geo/tests/test_point.py --diff

For flake8:
flake8 --ignore E203,E501,W503 geo/tests/test_point.py --statistics
"""

import pytest

# from ptg.point import Point2D, Points
import ptg.point as pp

@pytest.fixture
def argv():
    return "input/example_old.yml"


@pytest.fixture
def x_coor():
    return (-1.0, 0.0, 1.0, -1.0, 0.0, 1.0, -1.0, 0.0, 1.0)


@pytest.fixture
def y_coor():
    return (-1.0, -1.0, -1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0)


def test_to_pairs(x_coor, y_coor):
    known = (
        (-1.0, -1.0),
        (0.0, -1.0),
        (1.0, -1.0),
        (-1.0, 0.0),
        (0.0, 0.0),
        (1.0, 0.0),
        (-1.0, 1.0),
        (0.0, 1.0),
        (1.0, 1.0),
    )

    found = pp.pairs(x_coor, y_coor)
    assert len(known) == len(found)
    assert known == found


def test_quadrant_one(x_coor, y_coor):
    known = (
        # (-1.0, -1.0),
        # (0.0, -1.0),
        # (1.0, -1.0),
        # (-1.0, 0.0),
        (0.0, 0.0),
        (1.0, 0.0),
        # (-1.0, 1.0),
        (0.0, 1.0),
        (1.0, 1.0),
    )

    found = pp.quadrant_one(pp.pairs(x_coor, y_coor))
    assert len(known) == len(found)
    assert known == found


def test_quadrant_two(x_coor, y_coor):
    known = (
        # (-1.0, -1.0),
        # (0.0, -1.0),
        # (1.0, -1.0),
        (-1.0, 0.0),
        # (0.0, 0.0),
        # (1.0, 0.0),
        (-1.0, 1.0),
        # (0.0, 1.0),
        # (1.0, 1.0),
    )

    found = pp.quadrant_two(pp.pairs(x_coor, y_coor))
    assert len(known) == len(found)
    assert known == found


def test_quadrant_three(x_coor, y_coor):
    known = (
        (-1.0, -1.0),
        # (0.0, -1.0),
        # (1.0, -1.0),
        # (-1.0, 0.0),
        # (0.0, 0.0),
        # (1.0, 0.0),
        # (-1.0, 1.0),
        # (0.0, 1.0),
        # (1.0, 1.0),
    )

    found = pp.quadrant_three(pp.pairs(x_coor, y_coor))
    assert len(known) == len(found)
    assert known == found


def test_quadrant_four(x_coor, y_coor):
    known = (
        # (-1.0, -1.0),
        (0.0, -1.0),
        (1.0, -1.0),
        # (-1.0, 0.0),
        # (0.0, 0.0),
        # (1.0, 0.0),
        # (-1.0, 1.0),
        # (0.0, 1.0),
        # (1.0, 1.0),
    )

    found = pp.quadrant_four(pp.pairs(x_coor, y_coor))
    assert len(known) == len(found)
    assert known == found


def test_points():

    pairs = ((0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0))
    pts = pp.Points(pairs=pairs)

    knownx = tuple(p[0] for p in pairs)
    knowny = tuple(p[1] for p in pairs)

    foundx = pts.xs
    foundy = pts.ys

    assert knownx == foundx
    assert knowny == foundy

    assert pts.length == 4
    assert pts.pairs == pairs

    known_point2Ds = (
        pp.Point2D(x=0.0, y=0.0),
        pp.Point2D(x=1.0, y=1.0),
        pp.Point2D(x=2.0, y=4.0),
        pp.Point2D(x=3.0, y=9.0),
    )

    found_point2Ds = pts.points2D

    assert known_point2Ds == found_point2Ds
