"""This module is a unit test of the dual_quad implementation.

To run
> conda activate siblenv
> cd ~/sibl
> pytest geo/tests/test_quadtree.py -v
"""

import ptg.quadtree as qt


def test_cell():
    ctr = qt.Coordinate(x=3.0, y=4.0)
    cell = qt.Cell(center=ctr, size=12.0)

    assert cell.center == ctr
    assert cell.west == -3.0  # 3.0 - 12.0 / 2 = -3.0
    assert cell.east == 9.0  # 3.0 + 12.0 / 2 = 9.0
    assert cell.south == -2.0  # 4.0 - 12.0 / 2 = -2.0
    assert cell.north == 10.0  # 4.0 + 12.0 / 2 = 10.0

    assert len(cell.children) == 0  # empty list
    # assert cell.children is None


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

    # assert cell.children is None  # empty list
    assert len(cell.children) == 0  # empty list
    cell.divide()  # cell division into four children
    assert len(cell.children) == 1  # single list of four children

    children = cell.children[0]

    child_sw = children.southwest
    assert child_sw.center == qt.Coordinate(x=1.5, y=-0.5)
    assert child_sw.west == 1.0
    assert child_sw.east == 2.0
    assert child_sw.south == -1.0
    assert child_sw.north == 0.0

    child_nw = children.northwest
    assert child_nw.center == qt.Coordinate(x=1.5, y=0.5)
    assert child_nw.west == 1.0
    assert child_nw.east == 2.0
    assert child_nw.south == 0.0
    assert child_nw.north == 1.0

    child_se = children.southeast
    assert child_se.center == qt.Coordinate(x=2.5, y=-0.5)
    assert child_se.west == 2.0
    assert child_se.east == 3.0
    assert child_se.south == -1.0
    assert child_se.north == 0.0

    child_ne = children.northeast
    assert child_ne.center == qt.Coordinate(x=2.5, y=0.5)
    assert child_ne.west == 2.0
    assert child_ne.east == 3.0
    assert child_ne.south == 0.0
    assert child_ne.north == 1.0


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

    tree = qt.QuadTree(cell=cell, level=0, level_max=1, points=points)
    a = 4
    assert tree.cell.center == qt.Coordinate(2.0, 0.0)
    assert tree.cell.children[0].southwest.center == qt.Coordinate(1.5, -0.5)
    assert tree.cell.children[0].northwest.center == qt.Coordinate(1.5, 0.5)
    assert tree.cell.children[0].southeast.center == qt.Coordinate(2.5, -0.5)
    assert tree.cell.children[0].northeast.center == qt.Coordinate(2.5, 0.5)

    assert len(tree.cell.children[0].southwest.children) == 0
    assert len(tree.cell.children[0].northwest.children) == 0
    assert len(tree.cell.children[0].southeast.children) == 0
    assert len(tree.cell.children[0].northeast.children) == 1

    assert tree.cell.children[0].northeast.children[
        0
    ].southwest.center == qt.Coordinate(2.25, 0.25)

    assert tree.cell.children[0].northeast.children[
        0
    ].northwest.center == qt.Coordinate(2.25, 0.75)

    assert tree.cell.children[0].northeast.children[
        0
    ].southeast.center == qt.Coordinate(2.75, 0.25)

    assert tree.cell.children[0].northeast.children[
        0
    ].northeast.center == qt.Coordinate(2.75, 0.75)
