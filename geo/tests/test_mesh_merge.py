"""This module is a unit test of the mesh_merge implementation.

To run
> conda activate siblenv
> cd ~/sibl
> pytest geo/tests/test_mesh_merge.py -v
"""

import pytest

from ptg.quadtree import Mesh, coordinates
from ptg.mesh_merge import Domain, mesh_merge


def test_two_elements_non_union():
    """Tests merging of two meshes with two elements each
    and a non-union result because the boundaries are not
    sufficiently close to each other.

    -1.0      -0.5       0.0   /   0.1       0.5       1.0  --> x-axis

     -2         1         3         1         3        -2
      o---------+---------+    /    +---------+---------o   0.5
      |         |         |    /    |         |         |       ^
      |         |         |    /    |         |         |       |
      |         |         |    /    |         |         |       |
      o---------+---------+    /    +---------+---------o   0.0 y-axis
     -1         0         2         0         2        -1

    -1.0      -0.5       0.0   /   0.1       0.5       1.0  --> x-axis

    where
      "+" is a four-valenced node
      "o" is a port, or formerly a "+" and now designated as a port
    """

    v0 = coordinates(
        pairs=(
            (-0.5, 0.0),  # 0
            (-0.5, 0.5),  # 1
            (0.0, 0.0),  # 2
            (0.0, 0.5),  # 3
            (-1.0, 0.5),  # -2
            (-1.0, 0.0),  # -1
        )
    )

    v1 = coordinates(
        pairs=(
            (0.1, 0.0),  # 0
            (0.1, 0.5),  # 1
            (0.5, 0.0),  # 2
            (0.5, 0.5),  # 3
            (1.0, 0.5),  # -2
            (1.0, 0.0),  # -1
        )
    )

    c0 = (
        (0, 2, 3, 1),  # faces_dual
        (-1, 0, 1, -2),  # faces_ports
    )

    c1 = (
        (0, 2, 3, 1),  # faces_dual
        (2, -1, -2, 3),  # faces_ports
    )

    m0 = Mesh(coordinates=v0, connectivity=c0)
    m1 = Mesh(coordinates=v1, connectivity=c1)

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

    d0 = Domain(mesh=m0, boundaries=b0)
    d1 = Domain(mesh=m1, boundaries=b1)

    d2 = mesh_merge(d0=d0, d1=d1, tolerance=1e-6)

    m2 = d2.mesh
    b2 = d2.boundaries
    assert m2.coordinates == v0 + v1

    assert m2.connectivity == ((0, 2, 3, 1), (5, 0, 1, 4), (6, 8, 9, 7), (8, 11, 10, 9))

    assert b2 == ((5, 4), (2, 3), (6, 7), (11, 10))


@pytest.mark.skip("work in progress")
def test_two_elements():
    """Tests merging of two meshes with two elements each.

    -1.0      -0.5       0.0   /   0.0       0.5       1.0  --> x-axis

     -2         1         3         1         3        -2
      o---------+---------+    /    +---------+---------o   0.5
      |         |         |    /    |         |         |       ^
      |         |         |    /    |         |         |       |
      |         |         |    /    |         |         |       |
      o---------+---------+    /    +---------+---------o   0.0 y-axis
     -1         0         2         0         2        -1

    -1.0      -0.5       0.0   /   0.0       0.5       1.0  --> x-axis

    where
      "+" is a four-valenced node
      "o" is a port, or formerly a "+" and now designated as a port
    """

    v0 = coordinates(
        pairs=(
            (-0.5, 0.0),  # 0
            (-0.5, 0.5),  # 1
            (0.0, 0.0),  # 2
            (0.0, 0.5),  # 3
            (-1.0, 0.5),  # -2
            (-1.0, 0.0),  # -1
        )
    )

    v1 = coordinates(
        pairs=(
            (0.0, 0.0),  # 0
            (0.0, 0.5),  # 1
            (0.5, 0.0),  # 2
            (0.5, 0.5),  # 3
            (1.0, 0.5),  # -2
            (1.0, 0.0),  # -1
        )
    )

    c0 = (
        (0, 2, 3, 1),  # faces_dual
        (-1, 0, 1, -2),  # faces_ports
    )

    c1 = (
        (0, 2, 3, 1),  # faces_dual
        (2, -1, -2, 3),  # faces_ports
    )

    m0 = Mesh(coordinates=v0, connectivity=c0)
    m1 = Mesh(coordinates=v1, connectivity=c1)

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

    d0 = Domain(mesh=m0, boundaries=b0)
    d1 = Domain(mesh=m1, boundaries=b1)

    mout = mesh_merge(d0=d0, d1=d1)

    assert True
