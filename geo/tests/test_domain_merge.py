"""This module is a unit test of the mesh_merge implementation.

To run
> conda activate siblenv
> cd ~/sibl
> pytest geo/tests/test_domain_merge.py -v
"""

import pytest

# from ptg.quadtree import Mesh, coordinates
import ptg.quadtree as qt
from ptg.domain_merge import domain_merge


def test_two_domains_non_union():
    """Tests merging of two domains (meshes + boundaries)
    and a non-union result because the boundaries are not
    sufficiently close to each other.

     -2->4      1         3         1->7      3->9     -2->10
      o---------+---------+    /    +---------+---------o   0.5
      |         |         |    /    |         |         |       ^
      |         |         |    /    |         |         |       |
      |         |         |    /    |         |         |       |
      o---------+---------+    /    +---------+---------o   0.0 y-axis
     -1->5      0         2         0->6      2->8     -1->11

    -1.0      -0.5       0.0   /   0.1       0.5       1.0  --> x-axis

    where
      "+" is a four-valenced node
      "o" is a port, or formerly a "+" and now designated as a port
    """

    # vertices (aka points or coordinates)
    v0 = qt.coordinates(
        pairs=(
            (-0.5, 0.0),  # 0
            (-0.5, 0.5),  # 1
            (0.0, 0.0),  # 2
            (0.0, 0.5),  # 3
            (-1.0, 0.5),  # -2
            (-1.0, 0.0),  # -1
        )
    )

    v1 = qt.coordinates(
        pairs=(
            (0.1, 0.0),  # 0
            (0.1, 0.5),  # 1
            (0.5, 0.0),  # 2
            (0.5, 0.5),  # 3
            (1.0, 0.5),  # -2
            (1.0, 0.0),  # -1
        )
    )

    # faces (aka elements or connectivity)
    c0 = (
        (0, 2, 3, 1),  # faces_dual
        (-1, 0, 1, -2),  # faces_ports
    )

    c1 = (
        (0, 2, 3, 1),  # faces_dual
        (2, -1, -2, 3),  # faces_ports
    )

    # meshes
    m0 = qt.Mesh(coordinates=v0, connectivity=c0)
    m1 = qt.Mesh(coordinates=v1, connectivity=c1)

    # boundaries
    b0 = (
        (
            -1,
            -2,
        ),
        (
            2,
            3,
        ),
    )

    b1 = (
        (
            0,
            1,
        ),
        (
            -1,
            -2,
        ),
    )

    # domains
    d0 = qt.Domain(mesh=m0, boundaries=b0)
    d1 = qt.Domain(mesh=m1, boundaries=b1)

    d2 = domain_merge(domain0=d0, domain1=d1, tolerance=1e-6)

    m2 = d2.mesh
    b2 = d2.boundaries
    assert m2.coordinates == v0 + v1

    assert m2.connectivity == ((0, 2, 3, 1), (5, 0, 1, 4), (6, 8, 9, 7), (8, 11, 10, 9))

    assert b2 == ((5, 4), (2, 3), (6, 7), (11, 10))


@pytest.mark.skip("work in progress")
def test_two_domains():
    """Tests merging of two domains along a single boundary.

     -2->4      1         3         1->7->3   3->9     -2->10
      o---------+---------+    /    +---------+---------o   0.5
      |         |         |    /    |         |         |       ^
      |         |         |    /    |         |         |       |
      |         |         |    /    |         |         |       |
      o---------+---------+    /    +---------+---------o   0.0 y-axis
     -1->5      0         2         0->6->2   2->8     -1->11

    -1.0      -0.5       0.0   /   0.0       0.5       1.0  --> x-axis

    where
      "+" is a four-valenced node
      "o" is a port, or formerly a "+" and now designated as a port
    """

    # vertices (aka points or coordinates)
    v0 = qt.coordinates(
        pairs=(
            (-0.5, 0.0),  # 0
            (-0.5, 0.5),  # 1
            (0.0, 0.0),  # 2
            (0.0, 0.5),  # 3
            (-1.0, 0.5),  # -2
            (-1.0, 0.0),  # -1
        )
    )

    v1 = qt.coordinates(
        pairs=(
            (0.0, 0.0),  # 0
            (0.0, 0.5),  # 1
            (0.5, 0.0),  # 2
            (0.5, 0.5),  # 3
            (1.0, 0.5),  # -2
            (1.0, 0.0),  # -1
        )
    )

    # faces (aka elements or connectivity)
    c0 = (
        (0, 2, 3, 1),  # faces_dual
        (-1, 0, 1, -2),  # faces_ports
    )

    c1 = (
        (0, 2, 3, 1),  # faces_dual
        (2, -1, -2, 3),  # faces_ports
    )

    # meshes
    m0 = qt.Mesh(coordinates=v0, connectivity=c0)
    m1 = qt.Mesh(coordinates=v1, connectivity=c1)

    # boundaries
    b0 = (
        (
            -1,
            -2,
        ),
        (
            2,
            3,
        ),
    )

    b1 = (
        (
            0,
            1,
        ),
        (
            -1,
            -2,
        ),
    )

    # domains
    d0 = qt.Domain(mesh=m0, boundaries=b0)
    d1 = qt.Domain(mesh=m1, boundaries=b1)

    d2 = domain_merge(domain0=d0, domain1=d1, tolerance=1e-6)

    m2 = d2.mesh
    b2 = d2.boundaries
    assert m2.coordinates == v0 + v1

    assert m2.connectivity == ((0, 2, 3, 1), (5, 0, 1, 4), (2, 8, 9, 3), (8, 11, 10, 9))

    assert b2 == ((5, 4), (11, 10))


@pytest.mark.skip("work in progress")
def test_domain_merge_key_0001_r0_p1_and_key_0001_r1_p0():
    ctr = qt.Coordinate(x=0.0, y=0.0)
    cell = qt.Cell(center=ctr, size=2.0)
    points = tuple([qt.Coordinate(0.6, 0.6)])

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

    d0 = domain_dual[0]
    d1 = domain_dual[1]

    d2 = domain_merge(domain0=d0, domain1=d1, tolerance=1e-6)

    m2 = d2.mesh
    b2 = d2.boundaries
