"""This module is a unit test of the dual_quad implementation.

To run
> conda activate siblenv
> cd ~/sibl
> pytest geo/tests/test_quadtree.py -v
"""

import pytest

import ptg.quadtree as qt


def test_coordinates():

    pairs = ((0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0))
    points = qt.coordinates(pairs=pairs)

    for k, point in enumerate(points):
        assert point == qt.Coordinate(pairs[k][0], pairs[k][1])


def test_tuple_flatten_pairs():

    given = (
        ((0, 0), (1, 0), (1, 1), (0, 1)),
        (((10, 10), (11, 10), (11, 11), (10, 11))),
    )
    found = tuple(qt.QuadTree._tuple_flatten(given))
    known = (0, 0, 1, 0, 1, 1, 0, 1, 10, 10, 11, 10, 11, 11, 10, 11)

    assert found == known


def test_tuple_flatten_singletons():
    given = (
        (
            ((0,), 1),
            2,
        ),
        3,
    )
    found = tuple(qt.QuadTree._tuple_flatten(given))
    known = (0, 1, 2, 3)
    assert found == known


def test_cell():
    ctr = qt.Coordinate(x=3.0, y=4.0)
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
    ctr = qt.Coordinate(x=2.0, y=0.0)
    cell = qt.Cell(center=ctr, size=2.0)

    assert cell.vertices == ((1.0, -1.0), (3.0, -1.0), (3.0, 1.0), (1.0, 1.0))

    # y constant, delta x
    assert cell.contains(qt.Coordinate(x=0.9, y=0.0)) is False
    assert cell.contains(qt.Coordinate(x=1.0, y=0.0))
    assert cell.contains(qt.Coordinate(x=1.1, y=0.0))

    assert cell.contains(qt.Coordinate(x=2.9, y=0.0))
    assert cell.contains(qt.Coordinate(x=3.0, y=0.0))
    assert cell.contains(qt.Coordinate(x=3.1, y=0.0)) is False

    # x constant, delta y
    assert cell.contains(qt.Coordinate(x=2.0, y=-1.1)) is False
    assert cell.contains(qt.Coordinate(x=2.0, y=-1.0))
    assert cell.contains(qt.Coordinate(x=2.0, y=-0.9))

    assert cell.contains(qt.Coordinate(x=2.0, y=0.9))
    assert cell.contains(qt.Coordinate(x=2.0, y=1.0))
    assert cell.contains(qt.Coordinate(x=2.1, y=1.01)) is False

    # four corners
    assert cell.contains(qt.Coordinate(x=1.0, y=-1.0))
    assert cell.contains(qt.Coordinate(x=3.0, y=-1.0))
    assert cell.contains(qt.Coordinate(x=3.0, y=1.0))
    assert cell.contains(qt.Coordinate(x=1.0, y=1.0))


def test_cell_divide():
    """
    ^
    |     *-----------*
    |     |           |
    *-----1-----2-----3-----4-->
    |     |           |
    |     *-----------*
    """
    ctr = qt.Coordinate(x=2.0, y=0.0)
    cell = qt.Cell(center=ctr, size=2.0)

    assert cell.has_children is False
    cell.divide()  # cell division into four children
    assert cell.has_children is True

    assert cell.sw.center == qt.Coordinate(x=1.5, y=-0.5)
    assert cell.sw.west == 1.0
    assert cell.sw.east == 2.0
    assert cell.sw.south == -1.0
    assert cell.sw.north == 0.0

    assert cell.nw.center == qt.Coordinate(x=1.5, y=0.5)
    assert cell.nw.west == 1.0
    assert cell.nw.east == 2.0
    assert cell.nw.south == 0.0
    assert cell.nw.north == 1.0

    assert cell.se.center == qt.Coordinate(x=2.5, y=-0.5)
    assert cell.se.west == 2.0
    assert cell.se.east == 3.0
    assert cell.se.south == -1.0
    assert cell.se.north == 0.0

    assert cell.ne.center == qt.Coordinate(x=2.5, y=0.5)
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
    ctr = qt.Coordinate(x=2.0, y=0.0)
    cell = qt.Cell(center=ctr, size=2.0)
    points = tuple([qt.Coordinate(2.1, 0.1), qt.Coordinate(2.6, 0.6)])

    tree = qt.QuadTree(cell=cell, level=0, level_max=2, points=points)

    assert tree.cell.center == qt.Coordinate(2.0, 0.0)

    assert tree.cell.sw.center == qt.Coordinate(1.5, -0.5)
    assert tree.cell.nw.center == qt.Coordinate(1.5, 0.5)
    assert tree.cell.se.center == qt.Coordinate(2.5, -0.5)
    assert tree.cell.ne.center == qt.Coordinate(2.5, 0.5)

    assert tree.cell.sw.has_children is False
    assert tree.cell.nw.has_children is False
    assert tree.cell.se.has_children is False
    assert tree.cell.ne.has_children is True

    assert tree.cell.ne.sw.center == qt.Coordinate(2.25, 0.25)
    assert tree.cell.ne.nw.center == qt.Coordinate(2.25, 0.75)
    assert tree.cell.ne.se.center == qt.Coordinate(2.75, 0.25)
    assert tree.cell.ne.ne.center == qt.Coordinate(2.75, 0.75)

    assert tree.cell.ne.sw.has_children is False
    assert tree.cell.ne.nw.has_children is False
    assert tree.cell.ne.se.has_children is False
    assert tree.cell.ne.ne.has_children is False


def test_quadtree_bad_level_max():
    ctr = qt.Coordinate(x=2.0, y=0.0)
    cell = qt.Cell(center=ctr, size=2.0)
    points = tuple([qt.Coordinate(2.1, 0.1), qt.Coordinate(2.6, 0.6)])

    bad_max = -1  # must have at least Level 0
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
    ctr = qt.Coordinate(x=2.0, y=0.0)
    cell = qt.Cell(center=ctr, size=2.0)
    points = tuple([qt.Coordinate(2.1, 0.1), qt.Coordinate(2.6, 0.6)])

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
            sw=qt.Coordinate(1.0, -1.0),
            se=qt.Coordinate(2.0, -1.0),
            ne=qt.Coordinate(2.0, 0.0),
            nw=qt.Coordinate(1.0, 0.0),
        ),
        qt.Quad(
            sw=qt.Coordinate(1.0, 0.0),
            se=qt.Coordinate(2.0, 0.0),
            ne=qt.Coordinate(2.0, 1.0),
            nw=qt.Coordinate(1.0, 1.0),
        ),
        qt.Quad(
            sw=qt.Coordinate(2.0, -1.0),
            se=qt.Coordinate(3.0, -1.0),
            ne=qt.Coordinate(3.0, 0.0),
            nw=qt.Coordinate(2.0, 0.0),
        ),
        qt.Quad(
            sw=qt.Coordinate(2.0, 0.0),
            se=qt.Coordinate(2.5, 0.0),
            ne=qt.Coordinate(2.5, 0.5),
            nw=qt.Coordinate(2.0, 0.5),
        ),
        qt.Quad(
            sw=qt.Coordinate(2.0, 0.5),
            se=qt.Coordinate(2.5, 0.5),
            ne=qt.Coordinate(2.5, 1.0),
            nw=qt.Coordinate(2.0, 1.0),
        ),
        qt.Quad(
            sw=qt.Coordinate(2.5, 0.0),
            se=qt.Coordinate(3.0, 0.0),
            ne=qt.Coordinate(3.0, 0.5),
            nw=qt.Coordinate(2.5, 0.5),
        ),
        qt.Quad(
            sw=qt.Coordinate(2.5, 0.5),
            se=qt.Coordinate(3.0, 0.5),
            ne=qt.Coordinate(3.0, 1.0),
            nw=qt.Coordinate(2.5, 1.0),
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


def test_duals():
    """Tests dual quads in the quad tree."""
    ctr = qt.Coordinate(x=0.0, y=0.0)
    cell = qt.Cell(center=ctr, size=2.0)
    points = tuple([qt.Coordinate(0.6, -0.6)])

    # level_max = 0, base domain, no cell division
    tree = qt.QuadTree(cell=cell, level=0, level_max=0, points=points)
    quads = tree.quads()
    assert len(quads) == 1
    assert len(quads[0]) == 4
    quad_levels = tree.quad_levels()
    assert quad_levels == (0,)
    with pytest.raises(ValueError):
        _ = tree.duals()

    # level_max = 1, single cell division, four quads
    tree = qt.QuadTree(cell=cell, level=0, level_max=1, points=points)
    quads = tree.quads()
    assert len(quads) == 4
    assert len(quads[0]) == 4
    quad_levels = tree.quad_levels()
    assert quad_levels == (
        1,
        1,
        1,
        1,
    )
    duals = tree.duals()
    assert duals == (qt.DualHash(sw=0, nw=0, se=0, ne=0),)

    # level_max = 2, one to four cell division(s), seven to 16 quads in general, and
    # this example, with one trigger point, generates seven quads, and the
    # 0001 dual factory template.
    tree = qt.QuadTree(cell=cell, level=0, level_max=2, points=points)
    quads = tree.quads()
    assert len(quads) == 7
    duals = tree.duals()
    # assert duals == (qt.DualHash(sw=0, nw=0, se=0, ne=0),)


def test_manual_0001():
    quads_recursive = ((1,), (1,), (1,), ((2,), (2,), (2,), (2,)))
    quad_corners = tuple(len(corner) for corner in quads_recursive)
    assert quad_corners == (1, 1, 1, 4)

    template_key = qt.template_key(quad_corners=quad_corners)
    assert template_key == "key_0001"
    factory = qt.TemplateFactory()

    template = getattr(factory, template_key)
    assert template.name == "0001"


def test_manual_0010():
    quads_recursive = ((1,), (1,), ((2,), (2,), (2,), (2,)), (1,))
    quad_corners = tuple(len(corner) for corner in quads_recursive)
    assert quad_corners == (1, 1, 4, 1)

    template_key = qt.template_key(quad_corners=quad_corners)
    assert template_key == "key_0010"
    factory = qt.TemplateFactory()

    template = getattr(factory, template_key)
    assert template.name == "0010"


def test_manual_0100():
    quads_recursive = ((1,), ((2,), (2,), (2,), (2,)), (1,), (1,))
    quad_corners = tuple(len(corner) for corner in quads_recursive)
    assert quad_corners == (1, 4, 1, 1)

    template_key = qt.template_key(quad_corners=quad_corners)
    assert template_key == "key_0100"
    factory = qt.TemplateFactory()

    template = getattr(factory, template_key)
    assert template.name == "0100"


def test_manual_1000():
    quads_recursive = (((2,), (2,), (2,), (2,)), (1,), (1,), (1,))
    quad_corners = tuple(len(corner) for corner in quads_recursive)
    assert quad_corners == (4, 1, 1, 1)

    template_key = qt.template_key(quad_corners=quad_corners)
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

    template_key = qt.template_key(quad_corners=quad_corners)
    assert template_key == "key_0112"
    factory = qt.TemplateFactory()

    template = getattr(factory, template_key)
    assert template.name == "0112"


@pytest.mark.skip("Work in progress.")
def test_manual_nested_0001():
    quads_recursive = ((1,), (1,), (1,), ((2,), (2,), (2,), ((3,), (3,), (3,), (3,))))
    quad_corners = tuple(len(corner) for corner in quads_recursive)
    assert quad_corners == (1, 1, 1, 4)

    template_key = qt.template_key(quad_corners=quad_corners)
    assert template_key == "key_0001"
    factory = qt.TemplateFactory()

    template = getattr(factory, template_key)
    assert template.name == "0001"


@pytest.mark.skip("Work in progress.")
def test_dual_mesh_0000():
    ctr = qt.Coordinate(x=0.0, y=0.0)
    cell = qt.Cell(center=ctr, size=2.0)
    # Generate template_0000 and template_0001
    # points = tuple([qt.Coordinate(0.6, 0.6)])

    # Generate template_0011
    # points = tuple([qt.Coordinate(0.6, 0.6), qt.Coordinate(0.6, -0.6)])

    # Generate template_0110
    # points = tuple([qt.Coordinate(-0.6, 0.6), qt.Coordinate(0.6, -0.6)])

    # Generate template_0111
    points = tuple(
        [qt.Coordinate(-0.6, 0.6), qt.Coordinate(0.6, 0.6), qt.Coordinate(0.6, -0.6)]
    )

    level_max = 2
    tree = qt.QuadTree(cell=cell, level=0, level_max=level_max, points=points)
    quads = tree.quads()
    quad_levels = tree.quad_levels()
    quad_levels_recursive = tree.quad_levels_recursive()
    quads_dual = tree.quads_dual()
    aa = 4
