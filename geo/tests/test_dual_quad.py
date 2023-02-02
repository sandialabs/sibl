"""This module is a unit test of the dual_quad implementation.

To run
> conda activate siblenv
> cd ~/sibl
> pytest geo/tests/test_dual_quad.py -v
"""

import math
from itertools import chain
from typing import Final

import ptg.dual_quad as dquad


def test_Template_0000():
    template = dquad.Template_0000()
    assert template

    assert template.name == "0000"

    assert template.vertices == (
        (-1.0, -1.0),
        (-1.0, 0.0),
        (-1.0, 1.0),
        (0.0, -1.0),
        (0.0, 0.0),
        (0.0, 1.0),
        (1.0, -1.0),
        (1.0, 0.0),
        (1.0, 1.0),
    )

    assert template.vertices_revalence is None

    assert template.faces == (
        (0, 3, 4, 1),
        (1, 4, 5, 2),
        (3, 6, 7, 4),
        (4, 7, 8, 5),
    )

    assert template.vertices_dual == (
        (-0.5, -0.5),
        (-0.5, 0.5),
        (0.5, -0.5),
        (0.5, 0.5),
    )

    assert template.faces_dual == ((0, 2, 3, 1),)

    assert template.ports == (
        (-0.5, -1.0),
        (0.5, -1.0),
        (1.0, -0.5),
        (1.0, 0.5),
        (0.5, 1.0),
        (-0.5, 1.0),
        (-1.0, 0.5),
        (-1.0, -0.5),
    )

    assert template.boundaries_dual == ((0, 2), (2, 3), (3, 1), (1, 0))


def test_Template_0001_Base():
    template = dquad.Template_0001_Base()
    assert template

    assert template.name == "0001_Base"

    assert template.vertices == (
        (-1.0, -1.0),
        (-1.0, 0.0),
        (-1.0, 1.0),
        (0.0, -1.0),
        (0.0, 0.0),
        (0.0, 0.5),
        (0.0, 1.0),
        (0.5, 0.0),
        (0.5, 0.5),
        (0.5, 1.0),
        (1.0, -1.0),
        (1.0, 0.0),
        (1.0, 0.5),
        (1.0, 1.0),
    )

    assert template.vertices_revalence == (
        (
            (0.0, 0.5),
            (-0.5, 0.0),
            (0.0, -0.5),
            (0.5, 0.0),
        ),
    )

    assert template.faces == (
        (0, 3, 4, 1),
        (1, 4, 6, 2),
        (3, 10, 11, 4),
        (4, 7, 8, 5),
        (5, 8, 9, 6),
        (7, 11, 12, 8),
        (8, 12, 13, 9),
    )

    assert template.vertices_dual == (
        (-0.5, -0.5),
        (-0.5, 0.5),
        (-0.1665, -0.1665),
        (-0.1665, 0.1665),
        (0.1665, -0.1665),
        (0.25, 0.25),
        (0.25, 0.75),
        (0.5, -0.5),
        (0.75, 0.25),
        (0.75, 0.75),
    )

    assert template.faces_dual == (
        (0, 2, 3, 1),
        (0, 7, 4, 2),
        (2, 4, 5, 3),
        (3, 5, 6, 1),
        (4, 7, 8, 5),
        (5, 8, 9, 6),
    )

    assert template.ports == (
        (-0.5, -1.0),
        (0.5, -1.0),
        (1.0, -0.5),
        (1.0, 0.25),
        (1.0, 0.75),
        (0.75, 1.0),
        (0.25, 1.0),
        (-0.5, 1.0),
        (-1.0, 0.5),
        (-1.0, -0.5),
    )

    assert template.boundaries_dual == ((0, 7), (7, 8, 9), (9, 6, 1), (1, 0))


def test_Template_0001():
    template = dquad.Template_0001()
    assert template

    assert template.name == "0001"

    assert template.vertices == (
        (-1.0, -1.0),  # 0
        (-1.0, 0.0),  # 1
        (-1.0, 1.0),  # 2
        (0.0, -1.0),  # 3
        (0.0, 0.0),  # 4
        (0.0, 0.5),  # 5
        (0.0, 1.0),  # 6
        (0.5, 0.0),  # 7
        (1.0, -1.0),  # 8
        (1.0, 0.0),  # 9
    )

    assert template.vertices_revalence is None

    assert template.faces == (
        (0, 3, 4, 1),
        (1, 4, 6, 2),
        (3, 8, 9, 4),
    )

    assert template.vertices_dual == (
        (-0.5, -0.5),  # 0
        (-0.5, 0.5),  # 1
        (-0.1665, -0.1665),  # 2
        (-0.1665, 0.1665),  # 3
        (0.1665, -0.1665),  # 4
        (0.25, 0.25),  # 5
        (0.25, 0.75),  # 6
        (0.5, -0.5),  # 7
        (0.75, 0.25),  # 8
        (1.0, 0.25),  # -11
        (1.0, -0.5),  # -10
        (1.0, -1.0),  # -9
        (0.5, -1.0),  # -8
        (0.25, 1.0),  # -7
        (-0.5, 1.0),  # -6
        (-0.5, -1.0),  # -5
        (-1.0, 1.0),  # -4
        (-1.0, 0.5),  # -3
        (-1.0, -0.5),  # -2
        (-1.0, -1.0),  # -1
    )

    assert template.faces_dual == (
        (0, 2, 3, 1),
        (0, 7, 4, 2),
        (2, 4, 5, 3),
        (3, 5, 6, 1),
        (4, 7, 8, 5),
    )

    assert template.ports == (
        (1.0, 0.25),  # -11
        (1.0, -0.5),  # -10
        (1.0, -1.0),  # -9
        (0.5, -1.0),  # -8
        (0.25, 1.0),  # -7
        (-0.5, 1.0),  # -6
        (-0.5, -1.0),  # -5
        (-1.0, 1.0),  # -4
        (-1.0, 0.5),  # -3
        (-1.0, -0.5),  # -2
        (-1.0, -1.0),  # -1
    )

    assert template.faces_ports == (
        (-1, -5, 0, -2),
        (-2, 0, 1, -3),
        (-3, 1, -6, -4),
        (-5, -8, 7, 0),
        (1, 6, -7, -6),
        (-8, -9, -10, 7),
        (7, -10, -11, 8),
    )

    assert template.boundaries_dual == (
        (0, 7),
        (7, 8),
        (8, 5),
        (5, 6),
        (6, 1),
        (1, 0),
    )


def test_Template_0001_r0_p0():
    template = dquad.Template_0001_r0_p0()
    assert template
    assert template.name == "0001_r0_p0"

    assert template.vertices == (
        (-1.0, -1.0),  # 0
        (-1.0, 0.0),  # 1
        (-1.0, 1.0),  # 2
        (0.0, -1.0),  # 3
        (0.0, 0.0),  # 4
        (0.0, 0.5),  # 5
        (0.0, 1.0),  # 6
        (0.5, 0.0),  # 7
        (0.5, 0.5),  # 8
        (0.5, 1.0),  # 9
        (1.0, -1.0),  # 10
        (1.0, 0.0),  # 11
        (1.0, 0.5),  # 12
        (1.0, 1.0),  # 13
    )

    assert template.vertices_revalence is None

    assert template.faces == (
        (0, 3, 4, 1),
        (1, 4, 6, 2),
        (3, 10, 11, 4),
        (4, 7, 8, 5),
        (5, 8, 9, 6),
        (7, 11, 12, 8),
        (8, 12, 13, 9),
    )

    assert template.vertices_dual == (
        (-0.5, -0.5),  # 0
        (-0.5, 0.5),  # 1
        (-0.1665, -0.1665),  # 2
        (-0.1665, 0.1665),  # 3
        (0.1665, -0.1665),  # 4
        (0.25, 0.25),  # 5
        (0.25, 0.75),  # 6
        (0.5, -0.5),  # 7
        (0.75, 0.25),  # 8
        (0.75, 0.75),  # 9
        (1.0, 1.0),  # -14
        (1.0, 0.75),  # -13
        (1.0, 0.25),  # -12
        (1.0, -0.5),  # -11
        (1.0, -1.0),  # -10
        (0.75, 1.0),  # -9
        (0.5, -1.0),  # -8
        (0.25, 1.0),  # -7
        (-0.5, 1.0),  # -6
        (-0.5, -1.0),  # -5
        (-1.0, 1.0),  # -4
        (-1.0, 0.5),  # -3
        (-1.0, -0.5),  # -2
        (-1.0, -1.0),  # -1
    )

    assert template.faces_dual == (
        (0, 2, 3, 1),
        (0, 7, 4, 2),
        (2, 4, 5, 3),
        (3, 5, 6, 1),
        (4, 7, 8, 5),
        (5, 8, 9, 6),
    )

    assert template.ports == (
        (1.0, 1.0),  # -14
        (1.0, 0.75),  # -13
        (1.0, 0.25),  # -12
        (1.0, -0.5),  # -11
        (1.0, -1.0),  # -10
        (0.75, 1.0),  # -9
        (0.5, -1.0),  # -8
        (0.25, 1.0),  # -7
        (-0.5, 1.0),  # -6
        (-0.5, -1.0),  # -5
        (-1.0, 1.0),  # -4
        (-1.0, 0.5),  # -3
        (-1.0, -0.5),  # -2
        (-1.0, -1.0),  # -1
    )

    assert template.faces_ports == (
        (-1, -5, 0, -2),
        (-2, 0, 1, -3),
        (-3, 1, -6, -4),
        (-5, -8, 7, 0),
        (1, 6, -7, -6),
        (6, 9, -9, -7),
        (-8, -10, -11, 7),
        (7, -11, -12, 8),
        (8, -12, -13, 9),
        (9, -13, -14, -9),
    )

    assert template.boundaries_dual == (
        (-1, -5, -8, -10),
        (-10, -11, -12, -13, -14),
        (-14, -9, -7, -6, -4),
        (-4, -3, -2, -1),
    )


def test_Template_0001_r0_p1():
    template = dquad.Template_0001_r0_p1()
    assert template
    assert template.name == "0001_r0_p1"

    assert template.faces == (
        (0, 3, 4, 1),
        (1, 4, 6, 2),
        (3, 10, 11, 4),
        (4, 7, 8, 5),
        (5, 8, 9, 6),
        (7, 11, 12, 8),
        # (8, 12, 13, 9),  # not included
    )

    assert template.faces_dual == (
        (0, 2, 3, 1),
        (0, 7, 4, 2),
        (2, 4, 5, 3),
        (3, 5, 6, 1),
        (4, 7, 8, 5),
        # (5, 8, 9, 6),  # not included
    )

    assert template.faces_ports == (
        (-1, -5, 0, -2),
        (-2, 0, 1, -3),
        (-3, 1, -6, -4),
        (-5, -8, 7, 0),
        (1, 6, -7, -6),
        # (6, 9, -9, -7),  # not included
        (-8, -10, -11, 7),
        (7, -11, -12, 8),
        # (8, -12, -13, 9),  # not included
        # (9, -13, -14, -9),
    )

    assert template.boundaries_dual == (
        (-1, -5, -8, -10),
        (-10, -11, -12),
        (-12, 8, 5),
        (5, 6, -7),
        (-7, -6, -4),
        (-4, -3, -2, -1),
    )


def test_Template_0001_r1_p0():
    template = dquad.Template_0001_r1_p0()
    assert template
    assert template.name == "0001_r1_p0"

    assert template.faces_ports == (
        # (-1, -5, 0, -2),  # not included
        # (-2, 0, 1, -3),
        # (-3, 1, -6, -4),
        # (-5, -8, 7, 0),
        (1, 6, -7, -6),
        (6, 9, -9, -7),
        # (-8, -10, -11, 7),  # not included
        (7, -11, -12, 8),
        (8, -12, -13, 9),
        (9, -13, -14, -9),
    )

    assert template.boundaries_dual == (
        (0, 7, -11),
        (-11, -12, -13, -14),
        (-14, -9, -7, -6),
        (-6, 1, 0),
    )


def test_Template_0001_r1_p1():
    template = dquad.Template_0001_r1_p1()
    assert template
    assert template.name == "0001_r1_p1"

    assert template.faces == (
        (0, 3, 4, 1),
        (1, 4, 6, 2),
        (3, 10, 11, 4),
        (4, 7, 8, 5),
        (5, 8, 9, 6),
        (7, 11, 12, 8),
        # (8, 12, 13, 9),  # not included
    )

    assert template.faces_dual == (
        (0, 2, 3, 1),
        (0, 7, 4, 2),
        (2, 4, 5, 3),
        (3, 5, 6, 1),
        (4, 7, 8, 5),
        # (5, 8, 9, 6),  # not included
    )

    assert template.faces_ports == (
        # (-1, -5, 0, -2),  # not included
        # (-2, 0, 1, -3),
        # (-3, 1, -6, -4),
        # (-5, -8, 7, 0),
        (1, 6, -7, -6),
        # (6, 9, -9, -7),  # not included
        # (-8, -10, -11, 7),
        (7, -11, -12, 8),
        # (8, -12, -13, 9),  # not included
        # (9, -13, -14, -9),
    )

    assert template.boundaries_dual == (
        (0, 7, -11),
        (-11, -12),
        (-12, 8, 5),
        (5, 6, -7),
        (-7, -6),
        (-6, 1, 0),
    )


def test_Template_0100():
    template = dquad.Template_0100()
    assert template
    assert template.name == "0100"

    TOL: Final = 1.0e-9

    # template vertices
    known = (
        (1.0, -1.0),
        (0.0, -1.0),
        (-1.0, -1.0),
        (1.0, 0.0),
        (0.0, 0.0),
        (-0.5, 0.0),
        (-1.0, 0.0),
        (0.0, 0.5),
        (-0.5, 0.5),
        (-1.0, 0.5),
        (1.0, 1.0),
        (0.0, 1.0),
        (-0.5, 1.0),
        (-1.0, 1.0),
    )

    found = template.vertices

    assert all(map(lambda a, b: abs(a - b) < TOL, chain(*known), chain(*found)))

    # template vertices_revalence
    known = (
        (
            (-0.5, 0.0),
            (0.0, -0.5),
            (0.5, 0.0),
            (0.0, 0.5),
        ),
    )
    known_flatten_one = tuple(chain(*known))

    found = template.vertices_revalence
    found_flatten_one = tuple(chain(*found))

    assert all(
        map(
            lambda a, b: abs(a - b) < TOL,
            chain(*known_flatten_one),
            chain(*found_flatten_one),
        )
    )

    assert template.faces == (
        (0, 3, 4, 1),
        (1, 4, 6, 2),
        (3, 10, 11, 4),
        (4, 7, 8, 5),
        (5, 8, 9, 6),
        (7, 11, 12, 8),
        (8, 12, 13, 9),
    )

    # template vertices_dual

    known = (
        (0.5, -0.5),
        (-0.5, -0.5),
        (0.1665, -0.1665),
        (-0.1665, -0.1665),
        (0.1665, 0.1665),
        (-0.25, 0.25),
        (-0.75, 0.25),
        (0.5, 0.5),
        (-0.25, 0.75),
        (-0.75, 0.75),
    )

    found = template.vertices_dual

    assert all(map(lambda a, b: abs(a - b) < TOL, chain(*known), chain(*found)))

    assert template.faces_dual == (
        (0, 2, 3, 1),
        (0, 7, 4, 2),
        (2, 4, 5, 3),
        (3, 5, 6, 1),
        (4, 7, 8, 5),
        (5, 8, 9, 6),
    )

    # template ports

    known = (
        (1.0, -0.5),
        (1.0, 0.5),
        (0.5, 1.0),
        (-0.25, 1.0),
        (-0.75, 1.0),
        (-1.0, 0.75),
        (-1.0, 0.25),
        (-1.0, -0.5),
        (-0.5, -1.0),
        (0.5, -1.0),
    )

    found = template.ports

    assert all(map(lambda a, b: abs(a - b) < TOL, chain(*known), chain(*found)))

    assert template.boundaries_dual == (
        (0, 7),
        (7, 8, 9),
        (9, 6, 1),
        (1, 0),
    )


def test_Template_0011():
    template = dquad.Template_0011()
    assert template

    assert template.name == "0011"

    assert template.vertices == (
        (-1.0, -1.0),
        (-1.0, 0.0),
        (-1.0, 1.0),
        (0.0, -1.0),
        (0.0, -0.5),
        (0.0, 0.0),
        (0.0, 0.5),
        (0.0, 1.0),
        (0.5, -1.0),
        (0.5, -0.5),
        (0.5, 0.0),
        (0.5, 0.5),
        (0.5, 1.0),
        (1.0, -1.0),
        (1.0, -0.5),
        (1.0, 0.0),
        (1.0, 0.5),
        (1.0, 1.0),
    )

    assert template.vertices_revalence == (
        (
            (0.0, 0.5),
            (-0.5, 0.0),
            (0.0, -0.5),
        ),
    )

    assert template.faces == (
        (0, 3, 5, 1),
        (1, 5, 7, 2),
        (3, 8, 9, 4),
        (4, 9, 10, 5),
        (5, 10, 11, 6),
        (6, 11, 12, 7),
        (8, 13, 14, 9),
        (9, 14, 15, 10),
        (10, 15, 16, 11),
        (11, 16, 17, 12),
    )

    assert template.vertices_dual == (
        (-0.5, -0.5),
        (-0.5, 0.5),
        (-0.1665, -0.1665),
        (-0.1665, 0.1665),
        (0.25, -0.75),
        (0.25, -0.25),
        (0.25, 0.25),
        (0.25, 0.75),
        (0.75, -0.75),
        (0.75, -0.25),
        (0.75, 0.25),
        (0.75, 0.75),
    )

    assert template.faces_dual == (
        (0, 2, 3, 1),
        (0, 4, 5, 2),
        (2, 5, 6, 3),
        (3, 6, 7, 1),
        (4, 8, 9, 5),
        (5, 9, 10, 6),
        (6, 10, 11, 7),
    )

    assert template.ports == (
        (-0.5, -1.0),
        (0.25, -1.0),
        (0.75, -1.0),
        (1.0, -0.75),
        (1.0, -0.25),
        (1.0, 0.25),
        (1.0, 0.75),
        (0.75, 1.0),
        (0.25, 1.0),
        (-0.5, 1.0),
        (-1.0, 0.5),
        (-1.0, -0.5),
    )

    assert template.boundaries_dual == (
        (0, 4, 8),
        (8, 9, 10, 11),
        (11, 7, 1),
        (1, 0),
    )


def test_Template_0110():
    template = dquad.Template_0110()
    assert template

    assert template.name == "0110"

    assert template.vertices == (
        (-1.0, -1.0),
        (-1.0, 0.0),
        (-1.0, 0.5),
        (-1.0, 1.0),
        (-0.5, 0.0),
        (-0.5, 0.5),
        (-0.5, 1.0),
        (0.0, -1.0),
        (0.0, -0.5),
        (0.0, 0.0),
        (0.0, 0.5),
        (0.0, 1.0),
        (0.5, -1.0),
        (0.5, -0.5),
        (0.5, 0.0),
        (1.0, -1.0),
        (1.0, -0.5),
        (1.0, 0.0),
        (1.0, 1.0),
    )

    assert template.vertices_revalence == (
        (
            (-0.5, 0.0),
            (0.0, -0.5),
        ),
        (
            (0.5, 0.0),
            (0.0, 0.5),
        ),
    )

    assert template.faces == (
        (0, 7, 9, 1),
        (1, 4, 5, 2),
        (2, 5, 6, 3),
        (4, 9, 10, 5),
        (5, 10, 11, 6),
        (7, 12, 13, 8),
        (8, 13, 14, 9),
        (12, 15, 16, 13),
        (13, 16, 17, 14),
        (9, 17, 18, 11),
    )

    assert template.vertices_dual == (
        (-0.5, -0.5),
        (-0.75, 0.25),
        (-0.75, 0.75),
        (-0.1665, -0.1665),
        (-0.25, 0.25),
        (-0.25, 0.75),
        (0.25, -0.75),
        (0.25, -0.25),
        (0.1665, 0.1665),
        (0.75, -0.75),
        (0.75, -0.25),
        (0.5, 0.5),
    )

    assert template.faces_dual == (
        (0, 3, 4, 1),
        (1, 4, 5, 2),
        (0, 6, 7, 3),
        (3, 7, 8, 4),
        (4, 8, 11, 5),
        (6, 9, 10, 7),
        (7, 10, 11, 8),
    )

    assert template.ports == (
        (-0.5, -1.0),
        (0.25, -1.0),
        (0.75, -1.0),
        (1.0, -0.75),
        (1.0, -0.25),
        (1.0, 0.5),
        (0.5, 1.0),
        (-0.25, 1.0),
        (-0.75, 1.0),
        (-1.0, 0.75),
        (-1.0, 0.25),
        (-1.0, -0.5),
    )

    assert template.boundaries_dual == (
        (0, 6, 9),
        (9, 10, 11),
        (11, 5, 2),
        (2, 1, 0),
    )


def test_Template_0111():
    template = dquad.Template_0111()
    assert template

    assert template.name == "0111"

    assert template.vertices == (
        (-1.0, -1.0),
        (-1.0, 0.0),
        (-1.0, 0.5),
        (-1.0, 1.0),
        (-0.5, 0.0),
        (-0.5, 0.5),
        (-0.5, 1.0),
        (0.0, -1.0),
        (0.0, -0.5),
        (0.0, 0.0),
        (0.0, 0.5),
        (0.0, 1.0),
        (0.5, -1.0),
        (0.5, -0.5),
        (0.5, 0.0),
        (0.5, 0.5),
        (0.5, 1.0),
        (1.0, -1.0),
        (1.0, -0.5),
        (1.0, 0.0),
        (1.0, 0.5),
        (1.0, 1.0),
    )

    assert template.vertices_revalence == (
        (
            (-0.5, 0.0),
            (0.0, -0.5),
        ),
    )

    assert template.faces == (
        (0, 7, 9, 1),
        (1, 4, 5, 2),
        (2, 5, 6, 3),
        (4, 9, 10, 5),
        (5, 10, 11, 6),
        (7, 12, 13, 8),
        (8, 13, 14, 9),
        (9, 14, 15, 10),
        (10, 15, 16, 11),
        (12, 17, 18, 13),
        (13, 18, 19, 14),
        (14, 19, 20, 15),
        (15, 20, 21, 16),
    )

    assert template.vertices_dual == (
        (-0.5, -0.5),
        (-0.75, 0.25),
        (-0.75, 0.75),
        (-0.1665, -0.1665),
        (-0.25, 0.25),
        (-0.25, 0.75),
        (0.25, -0.75),
        (0.25, -0.25),
        (0.25, 0.25),
        (0.25, 0.75),
        (0.75, -0.75),
        (0.75, -0.25),
        (0.75, 0.25),
        (0.75, 0.75),
    )

    assert template.faces_dual == (
        (0, 3, 4, 1),
        (1, 4, 5, 2),
        (0, 6, 7, 3),
        (3, 7, 8, 4),
        (4, 8, 9, 5),
        (6, 10, 11, 7),
        (7, 11, 12, 8),
        (8, 12, 13, 9),
    )

    assert template.ports == (
        (-0.5, -1.0),
        (0.25, -1.0),
        (0.75, -1.0),
        (1.0, -0.75),
        (1.0, -0.25),
        (1.0, 0.25),
        (1.0, 0.75),
        (0.75, 1.0),
        (0.25, 1.0),
        (-0.25, 1.0),
        (-0.75, 1.0),
        (-1.0, 0.75),
        (-1.0, 0.25),
        (-1.0, -0.5),
    )

    assert template.boundaries_dual == (
        (0, 6, 10),
        (10, 11, 12, 13),
        (13, 9, 5, 2),
        (2, 1, 0),
    )


def test_Template_1111():
    template = dquad.Template_1111()
    assert template

    assert template.name == "1111"

    assert template.vertices == (
        (-1.0, -1.0),
        (-1.0, -0.5),
        (-1.0, 0.0),
        (-1.0, 0.5),
        (-1.0, 1.0),
        (-0.5, -1.0),
        (-0.5, -0.5),
        (-0.5, 0.0),
        (-0.5, 0.5),
        (-0.5, 1.0),
        (0.0, -1.0),
        (0.0, -0.5),
        (0.0, 0.0),
        (0.0, 0.5),
        (0.0, 1.0),
        (0.5, -1.0),
        (0.5, -0.5),
        (0.5, 0.0),
        (0.5, 0.5),
        (0.5, 1.0),
        (1.0, -1.0),
        (1.0, -0.5),
        (1.0, 0.0),
        (1.0, 0.5),
        (1.0, 1.0),
    )

    assert template.vertices_revalence is None

    assert template.faces == (
        (0, 5, 6, 1),
        (1, 6, 7, 2),
        (2, 7, 8, 3),
        (3, 8, 9, 4),
        (5, 10, 11, 6),
        (6, 11, 12, 7),
        (7, 12, 13, 8),
        (8, 13, 14, 9),
        (10, 15, 16, 11),
        (11, 16, 17, 12),
        (12, 17, 18, 13),
        (13, 18, 19, 14),
        (15, 20, 21, 16),
        (16, 21, 22, 17),
        (17, 22, 23, 18),
        (18, 23, 24, 19),
    )

    assert template.vertices_dual == (
        (-0.75, -0.75),
        (-0.75, -0.25),
        (-0.75, 0.25),
        (-0.75, 0.75),
        (-0.25, -0.75),
        (-0.25, -0.25),
        (-0.25, 0.25),
        (-0.25, 0.75),
        (0.25, -0.75),
        (0.25, -0.25),
        (0.25, 0.25),
        (0.25, 0.75),
        (0.75, -0.75),
        (0.75, -0.25),
        (0.75, 0.25),
        (0.75, 0.75),
    )

    assert template.faces_dual == (
        (0, 4, 5, 1),
        (1, 5, 6, 2),
        (2, 6, 7, 3),
        (4, 8, 9, 5),
        (5, 9, 10, 6),
        (6, 10, 11, 7),
        (8, 12, 13, 9),
        (9, 13, 14, 10),
        (10, 14, 15, 11),
    )

    assert template.ports == (
        (-0.75, -1.0),
        (-0.25, -1.0),
        (0.25, -1.0),
        (0.75, -1.0),
        (1.0, -0.75),
        (1.0, -0.25),
        (1.0, 0.25),
        (1.0, 0.75),
        (0.75, 1.0),
        (0.25, 1.0),
        (-0.25, 1.0),
        (-0.75, 1.0),
        (-1.0, 0.75),
        (-1.0, 0.25),
        (-1.0, -0.25),
        (-1.0, -0.75),
    )

    assert template.boundaries_dual == (
        (0, 4, 8, 12),
        (12, 13, 14, 15),
        (15, 11, 7, 3),
        (3, 2, 1, 0),
    )


def test_Template_0112():
    template = dquad.Template_0112()
    assert template

    assert template.name == "0112"

    assert template.vertices == (
        (-1.0, -1.0),  # 0
        (-1.0, 0.0),  # 1
        (-1.0, 0.5),  # 2
        (-1.0, 1.0),  # 3
        (-0.5, 0.0),  # 4
        (-0.5, 0.5),  # 5
        (-0.5, 1.0),  # 6
        (0.0, -1.0),  # 7
        (0.0, -0.5),  # 8
        (0.0, 0.0),  # 9
        (0.0, 0.25),  # 10
        (0.0, 0.5),  # 11
        (0.0, 0.75),  # 12
        (0.0, 1.0),  # 13
        (0.25, 0.0),  # 14
        (0.25, 0.25),  # 15
        (0.25, 0.5),  # 16
        (0.25, 0.75),  # 17
        (0.25, 1.00),  # 18
        (0.5, -1.0),  # 19
        (0.5, -0.5),  # 20
        (0.5, 0.0),  # 21
        (0.5, 0.25),  # 22
        (0.5, 0.5),  # 23
        (0.5, 0.75),  # 24
        (0.5, 1.0),  # 25
        (0.75, 0.0),  # 26
        (0.75, 0.25),  # 27
        (0.75, 0.5),  # 28
        (0.75, 0.75),  # 29
        (0.75, 1.00),  # 30
        (1.0, -1.0),  # 31
        (1.0, -0.5),  # 32
        (1.0, 0.0),  # 33
        (1.0, 0.25),  # 24
        (1.0, 0.5),  # 35
        (1.0, 0.75),  # 36
        (1.0, 1.0),  # 37
    )

    assert template.vertices_revalence == (
        (
            (-0.5, 0.0),
            (0.0, -0.5),
        ),
        (
            (0.0, 0.25),
            (-0.25, 0.5),
            (0.0, 0.75),
        ),
        (
            (0.25, 0.0),
            (0.50, -0.25),
            (0.75, 0.0),
        ),
    )

    assert template.faces == (
        (0, 7, 9, 1),
        (1, 4, 5, 2),
        (2, 5, 6, 3),
        (4, 9, 11, 5),
        (5, 11, 13, 6),
        (7, 19, 20, 8),
        (8, 20, 21, 9),
        (9, 14, 15, 10),
        (10, 15, 16, 11),
        (11, 16, 17, 12),
        (12, 17, 18, 13),
        (14, 21, 22, 15),
        (15, 22, 23, 16),
        (16, 23, 24, 17),
        (17, 24, 25, 18),
        (19, 31, 32, 20),
        (20, 32, 33, 21),
        (21, 26, 27, 22),
        (22, 27, 28, 23),
        (23, 28, 29, 24),
        (24, 29, 30, 25),
        (26, 33, 34, 27),
        (27, 34, 35, 28),
        (28, 35, 36, 29),
        (29, 36, 37, 30),
    )

    assert template.vertices_dual == (
        (-0.5, -0.5),  # 0
        (-0.75, 0.25),  # 1
        (-0.75, 0.75),  # 2
        (-0.5 / 3.0, -0.5 / 3.0),  # 3
        (-0.25, 0.25),  # 4
        (-0.25 / 3.0, 0.5 - 0.25 / 3.0),  # 5
        (-0.25 / 3.0, 0.5 + 0.25 / 3.0),  # 6
        (-0.25, 0.75),  # 7
        (0.25, -0.75),  # 8
        (0.25, -0.25),  # 9
        (0.5 - 0.25 / 3.0, -0.25 / 3.0),  # 10
        (0.125, 0.125),  # 11
        (0.125, 0.375),  # 12
        (0.125, 0.625),  # 13
        (0.125, 0.875),  # 14
        (0.375, 0.125),  # 15
        (0.375, 0.375),  # 16
        (0.375, 0.625),  # 17
        (0.375, 0.875),  # 18
        (0.75, -0.75),  # 19
        (0.75, -0.25),  # 20
        (0.5 + 0.25 / 3.0, -0.25 / 3.0),  # 21
        (0.625, 0.125),  # 22
        (0.625, 0.375),  # 23
        (0.625, 0.625),  # 24
        (0.625, 0.875),  # 25
        (0.875, 0.125),  # 26
        (0.875, 0.375),  # 27
        (0.875, 0.625),  # 28
        (0.875, 0.875),  # 29
    )

    assert template.faces_dual == (
        (0, 3, 4, 1),
        (1, 4, 7, 2),
        (0, 8, 9, 3),
        (8, 19, 20, 9),
        (3, 9, 11, 4),
        (4, 11, 12, 5),
        (4, 5, 6, 7),
        (5, 12, 13, 6),
        (7, 6, 13, 14),
        (9, 10, 15, 11),
        (9, 20, 21, 10),
        (10, 21, 22, 15),
        (20, 26, 22, 21),
        (11, 15, 16, 12),
        (12, 16, 17, 13),
        (13, 17, 18, 14),
        (15, 22, 23, 16),
        (16, 23, 24, 17),
        (17, 24, 25, 18),
        (22, 26, 27, 23),
        (23, 27, 28, 24),
        (24, 28, 29, 25),
    )

    assert template.ports == (
        (-0.5, -1.0),  # s-sw
        (0.25, -1.0),  # s-se
        (0.75, -1.0),  # s-se
        (1.0, -0.75),  # e-se
        (1.0, -0.25),  # e-se
        (1.0, 0.125),  # e-ne
        (1.0, 0.375),  # e-ne
        (1.0, 0.625),  # e-ne
        (1.0, 0.875),  # e-ne
        (0.875, 1.0),  # n-ne
        (0.625, 1.0),  # n-ne
        (0.375, 1.0),  # n-ne
        (0.125, 1.0),  # n-ne
        (-0.25, 1.0),  # n-nw
        (-0.75, 1.0),  # n-nw
        (-1.0, 0.75),  # w-nw
        (-1.0, 0.25),  # w-nw
        (-1.0, -0.5),  # s-sw
    )

    assert template.boundaries_dual == (
        (0, 8, 19),
        (19, 20, 26, 27, 28, 29),
        (29, 25, 18, 14, 7, 2),
        (2, 1, 0),
    )


def test_rotate():
    given_x_axis = (1.0, 0.0)
    given_y_axis = (0.0, 1.0)
    # some vector at 60 deg in reference config
    # given_vector = (500.0, 866.0)
    given_vector = (500.0, 1000.0 * math.sqrt(3.0) / 2.0)
    given = (given_x_axis, given_y_axis, given_vector)

    deg_to_rad = math.pi / 180.0
    ang_d = 30.0  # degrees
    ang_r = ang_d * deg_to_rad  # radians

    known_x_axis = (math.cos(ang_r), math.sin(ang_r))
    known_y_axis = (-1.0 * math.sin(ang_r), math.cos(ang_r))
    # some vector moved 30 degrees, now at 90 deg in current config
    known_vector = (0.0, 1000.0)
    known = (known_x_axis, known_y_axis, known_vector)

    found = dquad.rotate(ref=given, angle=ang_d)

    kx, ky = zip(*known)
    knowns = kx + ky

    fx, fy = zip(*found)
    founds = fx + fy

    TOL: Final = 1.0e-9
    assert all(map(lambda a, b: abs(a - b) < TOL, knowns, founds))


"""
Copyright 2023 Sandia National Laboratories

Notice: This computer software was prepared by National Technology and Engineering Solutions of
Sandia, LLC, hereinafter the Contractor, under Contract DE-NA0003525 with the Department of Energy
(DOE). All rights in the computer software are reserved by DOE on behalf of the United States
Government and the Contractor as provided in the Contract. You are authorized to use this computer
software for Governmental purposes but it is not to be released or distributed to the public.
NEITHER THE U.S. GOVERNMENT NOR THE CONTRACTOR MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR ASSUMES
ANY LIABILITY FOR THE USE OF THIS SOFTWARE. This notice including this sentence must appear on any
copies of this computer software. Export of this data may require a license from the United States
Government.
"""
