"""This module is a unit test of the dual_quad implementation.

To run
> conda activate siblenv
> cd ~/sibl
> pytest geo/tests/test_quadtree.py -v
"""

import pytest

from ptg.point import Point2D, Points
import ptg.quadtree as qt


# def test_coordinates():
#
#     pairs = ((0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0))
#     points = qt.coordinates(pairs=pairs)
#
#     for k, point in enumerate(points):
#         assert point == Point2D(pairs[k][0], pairs[k][1])


def test_levels_flatten_pairs():

    given = (
        ((0, 0), (1, 0), (1, 1), (0, 1)),
        (((10, 10), (11, 10), (11, 11), (10, 11))),
    )
    found = tuple(qt.QuadTree._levels_flatten(given))
    known = (0, 0, 1, 0, 1, 1, 0, 1, 10, 10, 11, 10, 11, 11, 10, 11)

    assert found == known


def test_levels_flatten_singletons():
    given = (
        (
            ((0,), 1),
            2,
        ),
        3,
    )
    found = tuple(qt.QuadTree._levels_flatten(given))
    known = (0, 1, 2, 3)
    assert found == known


def test_levels_flatten_recursion_pattern():
    given = ((1,), (1,), (1,), ((2,), (2,), (2,), (2,)))

    found = tuple(qt.QuadTree._levels_flatten(given))
    known = (1, 1, 1, 2, 2, 2, 2)
    assert found == known


def test_cell():
    # ctr = Point2D(x=3.0, y=4.0)
    ctr = Point2D(x=3.0, y=4.0)
    cell = qt.Cell(center=ctr, size=12.0)

    assert cell.center == ctr
    assert cell.west == -3.0  # 3.0 - 12.0 / 2 = -3.0
    assert cell.east == 9.0  # 3.0 + 12.0 / 2 = 9.0
    assert cell.south == -2.0  # 4.0 - 12.0 / 2 = -2.0
    assert cell.north == 10.0  # 4.0 + 12.0 / 2 = 10.0

    assert cell.has_children is False
    assert cell.vertices == ((-3.0, -2.0), (9.0, -2.0), (9.0, 10.0), (-3.0, 10.0))


def test_cell_contains():
    """
    ^
    |     *-----------*
    |     |           |
    *-----1-----2-----3-----4-->
    |     |           |
    |     *-----------*
    """
    # ctr = Point2D(x=2.0, y=0.0)
    ctr = Point2D(x=2.0, y=0.0)
    cell = qt.Cell(center=ctr, size=2.0)

    assert cell.vertices == ((1.0, -1.0), (3.0, -1.0), (3.0, 1.0), (1.0, 1.0))

    # y constant, delta x
    assert cell.contains(Point2D(x=0.9, y=0.0)) is False
    assert cell.contains(Point2D(x=1.0, y=0.0))
    assert cell.contains(Point2D(x=1.1, y=0.0))

    assert cell.contains(Point2D(x=2.9, y=0.0))
    assert cell.contains(Point2D(x=3.0, y=0.0))
    assert cell.contains(Point2D(x=3.1, y=0.0)) is False

    # x constant, delta yPoint2D
    assert cell.contains(Point2D(x=2.0, y=-1.1)) is False
    assert cell.contains(Point2D(x=2.0, y=-1.0))
    assert cell.contains(Point2D(x=2.0, y=-0.9))

    assert cell.contains(Point2D(x=2.0, y=0.9))
    assert cell.contains(Point2D(x=2.0, y=1.0))
    assert cell.contains(Point2D(x=2.1, y=1.01)) is False

    # four corners
    assert cell.contains(Point2D(x=1.0, y=-1.0))
    assert cell.contains(Point2D(x=3.0, y=-1.0))
    assert cell.contains(Point2D(x=3.0, y=1.0))
    assert cell.contains(Point2D(x=1.0, y=1.0))


def test_cell_divide():
    """
    ^
    |     *-----------*
    |     |           |
    *-----1-----2-----3-----4-->
    |     |           |
    |     *-----------*
    """
    ctr = Point2D(x=2.0, y=0.0)
    cell = qt.Cell(center=ctr, size=2.0)

    assert cell.has_children is False
    cell.divide()  # cell division into four children
    assert cell.has_children is True

    assert cell.sw.center == Point2D(x=1.5, y=-0.5)
    assert cell.sw.west == 1.0
    assert cell.sw.east == 2.0
    assert cell.sw.south == -1.0
    assert cell.sw.north == 0.0

    assert cell.nw.center == Point2D(x=1.5, y=0.5)
    assert cell.nw.west == 1.0
    assert cell.nw.east == 2.0
    assert cell.nw.south == 0.0
    assert cell.nw.north == 1.0

    assert cell.se.center == Point2D(x=2.5, y=-0.5)
    assert cell.se.west == 2.0
    assert cell.se.east == 3.0
    assert cell.se.south == -1.0
    assert cell.se.north == 0.0

    assert cell.ne.center == Point2D(x=2.5, y=0.5)
    assert cell.ne.west == 2.0
    assert cell.ne.east == 3.0
    assert cell.ne.south == 0.0
    assert cell.ne.north == 1.0


def test_quadtree():
    """
    ^
    |     *-----------*
    |     |           |
    *-----1-----2-----3-----4-->
    |     |           |
    |     *-----------*
    """
    ctr = Point2D(x=2.0, y=0.0)
    cell = qt.Cell(center=ctr, size=2.0)
    # points = tuple([Point2D(2.1, 0.1), Point2D(2.6, 0.6)])
    points = Points(pairs=((2.1, 0.1), (2.6, 0.6)))

    tree = qt.QuadTree(cell=cell, level=0, level_max=2, points=points)

    assert tree.cell.center == Point2D(2.0, 0.0)

    assert tree.cell.sw.center == Point2D(1.5, -0.5)
    assert tree.cell.nw.center == Point2D(1.5, 0.5)
    assert tree.cell.se.center == Point2D(2.5, -0.5)
    assert tree.cell.ne.center == Point2D(2.5, 0.5)

    assert tree.cell.sw.has_children is False
    assert tree.cell.nw.has_children is False
    assert tree.cell.se.has_children is False
    assert tree.cell.ne.has_children is True

    assert tree.cell.ne.sw.center == Point2D(2.25, 0.25)
    assert tree.cell.ne.nw.center == Point2D(2.25, 0.75)
    assert tree.cell.ne.se.center == Point2D(2.75, 0.25)
    assert tree.cell.ne.ne.center == Point2D(2.75, 0.75)

    assert tree.cell.ne.sw.has_children is False
    assert tree.cell.ne.nw.has_children is False
    assert tree.cell.ne.se.has_children is False
    assert tree.cell.ne.ne.has_children is False


def test_quadtree_bad_level_max():
    ctr = Point2D(x=2.0, y=0.0)
    cell = qt.Cell(center=ctr, size=2.0)
    points = Points(pairs=((2.1, 0.1), (2.6, 0.6)))

    bad_max = 0  # must have at least Level 1
    with pytest.raises(ValueError):
        _ = qt.QuadTree(cell=cell, level=0, level_max=bad_max, points=points)


def test_quads_and_levels():
    """
    ^
    |     *-----------*
    |     |           |
    *-----1-----2-----3-----4-->
    |     |           |
    |     *-----------*
    """
    ctr = Point2D(x=2.0, y=0.0)
    cell = qt.Cell(center=ctr, size=2.0)
    points = Points(pairs=((2.1, 0.1), (2.6, 0.6)))

    tree = qt.QuadTree(cell=cell, level=0, level_max=2, points=points)

    quads = tree.quads()

    # terse version
    assert quads == (
        ((1.0, -1.0), (2.0, -1.0), (2.0, 0.0), (1.0, 0.0)),
        ((1.0, 0.0), (2.0, 0.0), (2.0, 1.0), (1.0, 1.0)),
        ((2.0, -1.0), (3.0, -1.0), (3.0, 0.0), (2.0, 0.0)),
        ((2.0, 0.0), (2.5, 0.0), (2.5, 0.5), (2.0, 0.5)),
        ((2.0, 0.5), (2.5, 0.5), (2.5, 1.0), (2.0, 1.0)),
        ((2.5, 0.0), (3.0, 0.0), (3.0, 0.5), (2.5, 0.5)),
        ((2.5, 0.5), (3.0, 0.5), (3.0, 1.0), (2.5, 1.0)),
    )

    # verbose version
    assert quads == (
        qt.Quad(
            sw=Point2D(1.0, -1.0),
            se=Point2D(2.0, -1.0),
            ne=Point2D(2.0, 0.0),
            nw=Point2D(1.0, 0.0),
        ),
        qt.Quad(
            sw=Point2D(1.0, 0.0),
            se=Point2D(2.0, 0.0),
            ne=Point2D(2.0, 1.0),
            nw=Point2D(1.0, 1.0),
        ),
        qt.Quad(
            sw=Point2D(2.0, -1.0),
            se=Point2D(3.0, -1.0),
            ne=Point2D(3.0, 0.0),
            nw=Point2D(2.0, 0.0),
        ),
        qt.Quad(
            sw=Point2D(2.0, 0.0),
            se=Point2D(2.5, 0.0),
            ne=Point2D(2.5, 0.5),
            nw=Point2D(2.0, 0.5),
        ),
        qt.Quad(
            sw=Point2D(2.0, 0.5),
            se=Point2D(2.5, 0.5),
            ne=Point2D(2.5, 1.0),
            nw=Point2D(2.0, 1.0),
        ),
        qt.Quad(
            sw=Point2D(2.5, 0.0),
            se=Point2D(3.0, 0.0),
            ne=Point2D(3.0, 0.5),
            nw=Point2D(2.5, 0.5),
        ),
        qt.Quad(
            sw=Point2D(2.5, 0.5),
            se=Point2D(3.0, 0.5),
            ne=Point2D(3.0, 1.0),
            nw=Point2D(2.5, 1.0),
        ),
    )

    quad_levels = tree.quad_levels()
    assert quad_levels == (
        1,
        1,
        1,
        2,
        2,
        2,
        2,
    )


def test_manual_0000():
    quads_recursive = ((1,), (1,), (1,), (1,))
    quad_corners = tuple(len(corner) for corner in quads_recursive)
    assert quad_corners == (1, 1, 1, 1)

    template_key = qt.template_key(quad_corners=quad_corners, level=0, partial=False)
    assert template_key == "key_0000"
    factory = qt.TemplateFactory()

    template = getattr(factory, template_key)
    assert template.name == "0000"


def test_manual_0001():
    quads_recursive = ((1,), (1,), (1,), ((2,), (2,), (2,), (2,)))
    quad_corners = tuple(len(corner) for corner in quads_recursive)
    assert quad_corners == (1, 1, 1, 4)

    template_key = qt.template_key(quad_corners=quad_corners, level=0, partial=False)
    assert template_key == "key_0001_r0_p0"
    factory = qt.TemplateFactory()

    template = getattr(factory, template_key)
    assert template.name == "0001_r0_p0"


def test_manual_0010():
    quads_recursive = ((1,), (1,), ((2,), (2,), (2,), (2,)), (1,))
    quad_corners = tuple(len(corner) for corner in quads_recursive)
    assert quad_corners == (1, 1, 4, 1)

    template_key = qt.template_key(quad_corners=quad_corners, level=0, partial=False)
    assert template_key == "key_0010"
    factory = qt.TemplateFactory()

    template = getattr(factory, template_key)
    assert template.name == "0010"


def test_manual_0100():
    quads_recursive = ((1,), ((2,), (2,), (2,), (2,)), (1,), (1,))
    quad_corners = tuple(len(corner) for corner in quads_recursive)
    assert quad_corners == (1, 4, 1, 1)

    template_key = qt.template_key(quad_corners=quad_corners, level=0, partial=False)
    assert template_key == "key_0100"
    factory = qt.TemplateFactory()

    template = getattr(factory, template_key)
    assert template.name == "0100"


def test_manual_1000():
    quads_recursive = (((2,), (2,), (2,), (2,)), (1,), (1,), (1,))
    quad_corners = tuple(len(corner) for corner in quads_recursive)
    assert quad_corners == (4, 1, 1, 1)

    template_key = qt.template_key(quad_corners=quad_corners, level=0, partial=False)
    assert template_key == "key_1000"
    factory = qt.TemplateFactory()

    template = getattr(factory, template_key)
    assert template.name == "1000"


def test_manual_0112():
    quads_recursive = (
        (1,),
        ((2,), (2,), (2,), (2,)),
        ((2,), (2,), (2,), (2,)),
        (
            (3,),
            (3,),
            (3,),
            (3,),
            (3,),
            (3,),
            (3,),
            (3,),
            (3,),
            (3,),
            (3,),
            (3,),
            (3,),
            (3,),
            (3,),
            (3,),
        ),
    )
    quad_corners = tuple(len(corner) for corner in quads_recursive)
    assert quad_corners == (1, 4, 4, 16)

    template_key = qt.template_key(quad_corners=quad_corners, level=0, partial=False)
    assert template_key == "key_0112"
    factory = qt.TemplateFactory()

    template = getattr(factory, template_key)
    assert template.name == "0112"


def test_scale_then_translate():
    ref = Points(pairs=((-1.0, -1.0), (1.0, -1.0), (1.0, 1.0), (-1.0, 1.0)))

    bad_scale = 0
    scale = 100
    translate = Point2D(x=10.0, y=20.0)

    with pytest.raises(ValueError):
        _ = qt.scale_then_translate(ref=ref, scale=bad_scale, translate=translate)

    known = Points(
        pairs=((-90.0, -80.0), (110.0, -80.0), (110.0, 120.0), (-90.0, 120.0))
    )

    found = qt.scale_then_translate(ref=ref, scale=scale, translate=translate)

    assert known.xs == found.xs
    assert known.ys == found.ys


def test_known_quad_corners():
    known_true_corners = (
        (1, 1, 1, 1),  # flat-L1
        (1, 1, 1, 4),  # concave has four variations
        (1, 1, 4, 1),
        (1, 4, 1, 1),
        (4, 1, 1, 1),
        (1, 1, 4, 4),  # wave has four variations
        (1, 4, 4, 1),
        (4, 1, 4, 1),
        (4, 4, 1, 1),
        (1, 4, 4, 1),  # diagonal has two variations
        (4, 1, 1, 4),
        (1, 4, 4, 4),  # concave has four variations
        (4, 1, 4, 4),
        (4, 4, 1, 4),
        (4, 4, 4, 1),
        (4, 4, 4, 4),  # flat-L2
        (1, 4, 4, 16),  # weak transition has four variations
        (4, 1, 16, 4),
        (4, 16, 1, 4),
        (16, 4, 4, 1),
    )

    for item in known_true_corners:
        assert qt.known_quad_corners(quad_corners=item)

    known_false_corners = (
        (7, 1, 1, 1),  # level_max = 3 of southwest quad
        (10, 1, 1, 1),  # level_max = 4 of southwest quad
        (13, 1, 1, 1),  # level_max = 5 of southwest quad
    )

    for item in known_false_corners:
        assert not qt.known_quad_corners(quad_corners=item)


def test_static_domain_dual_key_0000():
    ctr = Point2D(x=0.0, y=0.0)
    cell = qt.Cell(center=ctr, size=2.0)
    # points = tuple([Point2D(0.6, 0.6)])
    points = Points(pairs=((0.6, 0.6),))

    # test key_0000 dual mesh construction
    tree = qt.QuadTree(cell=cell, level=0, level_max=1, points=points)
    domain_dual = tree.domain_dual()

    known_coordinates = Points(
        pairs=((-0.5, -0.5), (-0.5, 0.5), (0.5, -0.5), (0.5, 0.5))
    )
    known_connectivity = ((0, 2, 3, 1),)

    found_coordinates = domain_dual[0].mesh.coordinates
    found_connectivity = domain_dual[0].mesh.connectivity

    assert known_coordinates.xs == found_coordinates.xs
    assert known_coordinates.ys == found_coordinates.ys
    assert known_connectivity == found_connectivity

    known_boundaries_dual = (
        (0, 2),
        (2, 3),
        (3, 1),
        (1, 0),
    )

    found_boundaries_dual = domain_dual[0].boundaries

    assert known_boundaries_dual == found_boundaries_dual


def test_static_domain_dual_key_0001_r0_p0():
    ctr = Point2D(x=0.0, y=0.0)
    cell = qt.Cell(center=ctr, size=2.0)
    points = Points(pairs=((0.6, 0.6),))

    # test key_0001
    tree = qt.QuadTree(cell=cell, level=0, level_max=2, points=points)
    domain_dual = tree.domain_dual()

    known_coordinates = Points(
        pairs=(
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
    )

    known_connectivity = (
        (0, 2, 3, 1),  # faces_dual
        (0, 7, 4, 2),
        (2, 4, 5, 3),
        (3, 5, 6, 1),
        (4, 7, 8, 5),
        (5, 8, 9, 6),
        (-1, -5, 0, -2),  # faces_ports
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

    found_coordinates = domain_dual[0].mesh.coordinates
    found_connectivity = domain_dual[0].mesh.connectivity

    assert known_coordinates.xs == found_coordinates.xs
    assert known_coordinates.ys == found_coordinates.ys
    assert known_connectivity == found_connectivity

    known_boundaries_dual = (
        (-1, -5, -8, -10),
        (-10, -11, -12, -13, -14),
        (-14, -9, -7, -6, -4),
        (-4, -3, -2, -1),
    )

    found_boundaries_dual = domain_dual[0].boundaries

    assert known_boundaries_dual == found_boundaries_dual


def test_static_domain_dual_key_0001_r0_p1_and_key_0001_r1_p0():
    ctr = Point2D(x=0.0, y=0.0)
    cell = qt.Cell(center=ctr, size=2.0)
    points = Points(pairs=((0.6, 0.6),))

    # test key_0001 nested once with self
    tree = qt.QuadTree(cell=cell, level=0, level_max=3, points=points)
    known_quad_levels_recursive = (
        (1,),
        (1,),
        (1,),
        ((2,), (2,), (2,), ((3,), (3,), (3,), (3,))),
    )
    found_quad_levels_recursive = tree.quad_levels_recursive()
    assert known_quad_levels_recursive == found_quad_levels_recursive

    domain_dual = tree.domain_dual()

    known_coordinates_parent = Points(
        pairs=(
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
    )
    known_connectivity_parent = (
        (0, 2, 3, 1),  # faces_dual
        (0, 7, 4, 2),
        (2, 4, 5, 3),
        (3, 5, 6, 1),
        (4, 7, 8, 5),
        # (5, 8, 9, 6),  # does not include this dual face
        (-1, -5, 0, -2),
        (-2, 0, 1, -3),
        (-3, 1, -6, -4),
        (-5, -8, 7, 0),
        (1, 6, -7, -6),
        # (6, 9, -9, -7),  # does not include this port face
        (-8, -10, -11, 7),
        (7, -11, -12, 8),
        # (8, -12, -13, 9),  # does not include this port face
        # (9, -13, -14, -9),  # does not include this port face
    )

    known_boundaries_dual_parent = (
        (-1, -5, -8, -10),
        (-10, -11, -12),
        (-12, 8, 5),
        (5, 6, -7),
        (-7, -6, -4),
        (-4, -3, -2, -1),
    )

    known_coordinates_child = Points(
        pairs=(
            (0.25, 0.25),  # 0
            (0.25, 0.75),  # 1
            (0.41675, 0.41675),  # 2
            (0.41675, 0.58325),  # 3
            (0.58325, 0.41675),  # 4
            (0.625, 0.625),  # 5
            (0.625, 0.875),  # 6
            (0.75, 0.25),  # 7
            (0.875, 0.625),  # 8
            (0.875, 0.875),  # 9
            (1.0, 1.0),  # -14
            (1.0, 0.875),  # -13
            (1.0, 0.625),  # -12
            (1.0, 0.25),  # -11
            (1.0, 0.0),  # -10
            (0.875, 1.0),  # -9
            (0.75, 0.0),  # -8
            (0.625, 1.0),  # -7
            (0.25, 1.0),  # -6
            (0.25, 0.0),  # -5
            (0.0, 1.0),  # -4
            (0.0, 0.75),  # -3
            (0.0, 0.25),  # -2
            (0.0, 0.0),  # -1
        )
    )
    known_connectivity_child = (
        (0, 2, 3, 1),  # faces_dual
        (0, 7, 4, 2),
        (2, 4, 5, 3),
        (3, 5, 6, 1),
        (4, 7, 8, 5),
        (5, 8, 9, 6),
        # (-1, -5, 0, -2),  # does not include these port faces
        # (-2, 0, 1, -3),
        # (-3, 1, -6, -4),
        # (-5, -8, 7, 0),
        (1, 6, -7, -6),
        (6, 9, -9, -7),
        # (-8, -10, -11, 7),  # does include this port face
        (7, -11, -12, 8),
        (8, -12, -13, 9),
        (9, -13, -14, -9),
    )

    known_boundaries_dual_child = (
        (0, 7, -11),
        (-11, -12, -13, -14),
        (-14, -9, -7, -6),
        (-6, 1, 0),
    )

    found_coordinates_parent = domain_dual[0].mesh.coordinates
    found_connectivity_parent = domain_dual[0].mesh.connectivity
    found_boundaries_dual_parent = domain_dual[0].boundaries
    assert known_coordinates_parent.xs == found_coordinates_parent.xs
    assert known_coordinates_parent.ys == found_coordinates_parent.ys
    assert known_connectivity_parent == found_connectivity_parent
    assert known_boundaries_dual_parent == found_boundaries_dual_parent

    found_coordinates_child = domain_dual[1].mesh.coordinates
    found_connectivity_child = domain_dual[1].mesh.connectivity
    found_boundaries_dual_child = domain_dual[1].boundaries
    assert known_coordinates_child.xs == found_coordinates_child.xs
    assert known_coordinates_child.ys == found_coordinates_child.ys
    assert known_connectivity_child == found_connectivity_child
    assert known_boundaries_dual_child == found_boundaries_dual_child


def test_centroid():
    """Tests that the centroid of various polygons is correctly calculated."""

    # tall rectangle with counter-clockwise boundary order
    ps0 = Points(pairs=((0.0, 0.0), (1.0, 0.0), (1.0, 10.0), (0.0, 10.0)))
    known = Point2D(x=0.5, y=5.0)
    found = qt.centroid(coordinates=ps0)
    assert known == found

    # tall rectangle with clockwise boundary order
    ps1 = Points(pairs=((0.0, 0.0), (0.0, 10.0), (1.0, 10.0), (1.0, 0.0)))
    known = Point2D(x=0.5, y=5.0)
    found = qt.centroid(coordinates=ps1)
    assert known == found

    # tall rectangle twisted into bow-tie shape
    ps3 = Points(pairs=((0.0, 0.0), (1.0, 10.0), (0.0, 10.0), (1.0, 0.0)))
    known = Point2D(x=0.5, y=5.0)
    found = qt.centroid(coordinates=ps3)
    assert known == found

    # right triangle
    ps4 = Points(pairs=((0.0, 0.0), (9.0, 0.0), (9.0, 9.0)))
    known = Point2D(x=6.0, y=3.0)
    found = qt.centroid(coordinates=ps4)
    assert known == found


@pytest.mark.skip("work in progress")
def test_trim():
    """Tests the 'trim' function under the edge case when a boundary
    does not contain any of the elements in the mesh.  Returns an emtpy tuple mesh.
    """

    # two-element tall mesh unit square mesh tall mesh
    """
    2----5
    |    |
    1----4    b4---b3
    |    |    |    |
    0----3    b0---b1

    0    1    2    3
    """

    ps = Points(
        pairs=(
            (0.0, 0.0),
            (0.0, 1.0),
            (0.0, 2.0),
            (1.0, 0.0),
            (1.0, 1.0),
            (1.0, 2.0),
        )
    )
    cs = (
        (0, 3, 4, 1),
        (1, 4, 5, 2),
    )
    # m0 = qt.Mesh(coordinates=ps, connectivity=cs)
    _ = qt.Mesh(coordinates=ps, connectivity=cs)

    # boundary that doesn't contain this mesh
    # b0 = Points(pairs=((2.0, 0.0), (3.0, 0.0), (3.0, 1.0), (2.0, 1.0)))
    _ = Points(pairs=((2.0, 0.0), (3.0, 0.0), (3.0, 1.0), (2.0, 1.0)))

    # _ = qt.trim(mesh=m0, boundary=b0)
