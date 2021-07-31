"""This module is a unit test of the dual_quad implementation.

To run
> conda activate siblenv
> cd ~/sibl
> pytest geo/tests/test_quadtree.py -v
"""

import pytest

import ptg.quadtree as qt


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

    tree = qt.QuadTree(cell=cell, level=0, level_max=1, points=points)

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


# def test_plot_quadtree():
#     # set to False for regular testing, True for manual point testing
#     test = True
#     plot_shown = True
#     serialize = True
#
#     if test:
#         from pathlib import Path
#
#         import matplotlib.pyplot as plt
#         from matplotlib import rc
#
#         index_x, index_y = 0, 1  # avoid magic numbers later
#         latex = True
#         if latex:
#             rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
#             rc("text", usetex=True)
#
#         """
#         ^
#         |     *-----------*
#         |     |           |
#         *-----1-----2-----3-----4-->
#         |     |           |
#         |     *-----------*
#         """
#         ctr = qt.Coordinate(x=2.0, y=0.0)
#         cell = qt.Cell(center=ctr, size=2.0)
#         points = tuple([qt.Coordinate(2.1, 0.1), qt.Coordinate(2.6, 0.6)])
#
#         tree = qt.QuadTree(cell=cell, level=0, level_max=2, points=points)
#
#         quads = tree.quads()
#
#         for quad in quads:
#             if len(quad) == 4:
#
#             else
#
#
#         # quads = (
#         #     tree.cell.vertices,
#         #     tree.cell.sw.vertices,
#         #     tree.cell.nw.vertices,
#         #     tree.cell.se.vertices,
#         #     tree.cell.ne.vertices,
#         #     tree.cell.ne.sw.vertices,
#         #     tree.cell.ne.nw.vertices,
#         #     tree.cell.ne.se.vertices,
#         #     tree.cell.ne.ne.vertices,
#         # )
#
#         fig = plt.figure(figsize=(6.0, 6.0), dpi=100)
#         ax = fig.gca()
#
#         for quad in quads:
#             # xys = tree.cell.vertices
#             xs = [quad[k][index_x] for k in range(len(quad))]
#             ys = [quad[k][index_y] for k in range(len(quad))]
#             plt.fill(
#                 xs,
#                 ys,
#                 linestyle="dotted",
#                 edgecolor="magenta",
#                 alpha=0.5,
#                 facecolor="gray",
#             )
#
#         xs = [point.x for point in points]
#         ys = [point.y for point in points]
#         ax.scatter(xs, ys, linestyle="solid", edgecolor="black", color="tab:red")
#
#         ax.set_aspect("equal")
#
#         ax.set_xlabel(r"$x$")
#         ax.set_ylabel(r"$y$")
#
#         ax.set_xticks([1, 2, 3])
#         ax.set_yticks([-1, 0, 1])
#
#         if plot_shown:
#             plt.show()
#
#         if serialize:
#
#             extension = ".png"  # or '.'.png' | '.pdf' | '.svg'
#             filename = Path(__file__).stem + extension
#             fig.savefig(filename, bbox_inches="tight", pad_inches=0)
#             print(f"Serialized to {filename}")
