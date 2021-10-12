"""This module is a unit test of the mesh_merge implementation.

To run
> conda activate siblenv
> cd ~/sibl
> pytest geo/tests/test_domain_merge.py -v
"""

import pytest

import ptg.quadtree as qt
from ptg.domain_merge import boundary_match, boundary_substraction, domain_merge


def test_boundary_subtraction():
    # test boundary
    b0 = ((0, 1, 2, 3), (3, 4, 5), (5, 6), (6, 0))

    # test boundary subset
    s0 = ((3, 4, 5), (6, 0))

    known_result = ((0, 1, 2, 3), (5, 6))

    found_result = boundary_substraction(boundary=b0, subtracted=s0)

    assert known_result == found_result


def test_two_domains_non_union():
    """Tests merging of two domains (meshes + boundaries)
    and a non-union result because the boundaries are not
    sufficiently close to each other.

     -2->4      1         3         1->7      3->9     -2->10
      o---------+---------+    /    +---------+---------o   0.5
      |         |         |    /    |         |         |       ^
      |    1    |    0    |    /    |    0    |    1    |       |
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

    # boundaries, counterclockwise contour from lower left corner
    b0 = (
        (
            2,
            3,
        ),
        (
            -2,
            -1,
        ),
    )

    b1 = (
        (
            -1,
            -2,
        ),
        (
            1,
            0,
        ),
    )

    match2 = boundary_match(
        boundary0=b0, coordinates0=v0, boundary1=b1, coordinates1=v1, tolerance=1e-6
    )

    assert match2 == ((0, 0), (0, 0))

    # domains
    d0 = qt.Domain(mesh=m0, boundaries=b0)
    d1 = qt.Domain(mesh=m1, boundaries=b1)

    d2 = domain_merge(domain0=d0, domain1=d1, tolerance=1e-6)

    m2 = d2.mesh
    b2 = d2.boundaries
    assert m2.coordinates == v0 + v1

    assert m2.connectivity == ((0, 2, 3, 1), (5, 0, 1, 4), (6, 8, 9, 7), (8, 11, 10, 9))

    # assert b2 == ((5, 4), (2, 3), (6, 7), (11, 10))
    assert b2 == ((2, 3), (4, 5), (11, 10), (7, 6))


def test_two_domains():
    """Tests merging of two domains along a single boundary.

     -2->4      1         3         1->7->3   3->9     -2->10
      o---------+---------+    /    +---------+---------o   0.5
      |         |         |    /    |         |         |       ^
      |    1    |    0    |    /    |    0    |    1    |       |
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

    # boundaries, counterclockwise contour from lower left corner
    b0 = (
        (
            2,
            3,
        ),
        (
            -2,
            -1,
        ),
    )

    b1 = (
        (
            -1,
            -2,
        ),
        (
            1,
            0,
        ),
    )

    match2 = boundary_match(
        boundary0=b0, coordinates0=v0, boundary1=b1, coordinates1=v1, tolerance=1e-6
    )

    assert match2 == ((0, -1), (0, 0))

    # domains
    d0 = qt.Domain(mesh=m0, boundaries=b0)
    d1 = qt.Domain(mesh=m1, boundaries=b1)

    d2 = domain_merge(domain0=d0, domain1=d1, tolerance=1e-6)

    m2 = d2.mesh
    b2 = d2.boundaries
    assert m2.coordinates == v0 + v1

    assert m2.connectivity == ((0, 2, 3, 1), (5, 0, 1, 4), (2, 8, 9, 3), (8, 11, 10, 9))

    # assert b2 == ((5, 4), (11, 10))
    assert b2 == ((4, 5), (11, 10))


def test_two_domains_six_boundary_segments():
    """Tests merging a child 'L-shape' (domain1) into a parent 'L-shape' (domain0).

                              -1->27->9o---------o -2->26
                                       |         |
               -5->11    -7->9         |    3    |
    2.0          o---------o           |         |
                 |         |   2->18->2+---------+5->21
                 |    5    |           |         |
                 |         |           |    1    |
    1.5    -4->12o---------+2          |         |4->20   7->23    -4->24
                 |         |   1->17->1+---------+---------+---------o
                 |    2    |           |         |         |         |
                 |         |           |    0    |    2    |    4    |
    1.0    -3->13o---------+1          |         |         |         |
                 |         |           +---------+---------+---------o
                 |    1    |        0->16->0  3->19->3  6->22->4  -3->25->5
                 |         |0        3         4      -11->5
    0.5    -2->14o---------+---------+---------+---------o   0.5
                 |         |         |         |         |       ^
                 |    0    |    3    |    4    |    6    |       |
                 |         |         |         |         |       |
    0.0          o---------o---------o---------o---------o   0.0 y-axis
               -1->15    -6->10    -8->8     -9->7    -10->6

               -1.0      -0.5       0.0       0.5       1.0  --> x-axis

            nnp0 = 16 = number of nodal points in mesh0
            nnp1 = 12 = number of nodal points in mesh1

            where
              "+" is a four-valenced node
              "o" is a port, or formerly a "+" and now designated as a port
    """

    # vertices (aka points or coordinates)
    v0 = qt.coordinates(
        pairs=(
            (-0.5, 0.5),  # 0
            (-0.5, 1.0),  # 1
            (-0.5, 1.5),  # 2
            (0.0, 0.5),  # 3
            (0.5, 0.5),  # 4
            (1.0, 0.5),  # -11
            (1.0, 0.0),  # -10
            (0.5, 0.0),  # -9
            (0.0, 0.0),  # -8
            (-0.5, 2.0),  # -7
            (-0.5, 0.0),  # -6
            (-1.0, 2.0),  # -5
            (-1.0, 1.5),  # -4
            (-1.0, 1.0),  # -3
            (-1.0, 0.5),  # -2
            (-1.0, 0.0),  # -1
        )
    )

    v1 = qt.coordinates(
        pairs=(
            (-0.5, 0.5),  # 0
            (-0.5, 1.0),  # 1
            (-0.5, 1.5),  # 2
            (0.0, 0.5),  # 3
            (0.0, 1.0),  # 4
            (0.0, 1.5),  # 5
            (0.5, 0.5),  # 6
            (0.5, 1.0),  # 7
            (1.0, 1.0),  # -4
            (1.0, 0.5),  # -3
            (0.0, 2.0),  # -2
            (-0.5, 2.0),  # -1
        )
    )

    # faces (aka elements or connectivity)
    c0 = (
        (-1, -6, 0, -2),  # faces_dual, 0
        (-2, 0, 1, -3),  # 1
        (-3, 1, 2, -4),  # 2
        (-6, -8, 3, 0),  # 3
        (-8, -9, 4, 3),  # 4
        (-4, 2, -7, -5),  # faces_ports, 5
        (-9, -10, -11, 4),  # 6
    )

    c1 = (
        (0, 3, 4, 1),  # faces_dual, 0
        (1, 4, 5, 2),  # 1
        (3, 6, 7, 4),  # 2
        (2, 5, -2, -1),  # faces_ports, 3
        (6, -3, -4, 7),  # 4
    )

    # meshes
    m0 = qt.Mesh(coordinates=v0, connectivity=c0)
    m1 = qt.Mesh(coordinates=v1, connectivity=c1)

    # boundaries, counterclockwise contour from lower left corner
    b0 = (
        (-11, 4, 3, 0),
        (0, 1, 2, -7),
    )
    b1 = (
        (0, 3, 6, -3),
        (-4, 7, 4),
        (4, 5, -2),
        (-1, 2, 1, 0),
    )

    match2 = boundary_match(
        boundary0=b0, coordinates0=v0, boundary1=b1, coordinates1=v1, tolerance=1e-6
    )

    assert match2 == ((-1, 0, 0, 0), (0, 0, 0, -2))

    # domains
    d0 = qt.Domain(mesh=m0, boundaries=b0)
    d1 = qt.Domain(mesh=m1, boundaries=b1)

    d2 = domain_merge(domain0=d0, domain1=d1, tolerance=1e-6)

    m2 = d2.mesh
    b2 = d2.boundaries
    assert m2.coordinates == v0 + v1

    assert m2.connectivity == (
        (15, 10, 0, 14),  # 0
        (14, 0, 1, 13),  # 1
        (13, 1, 2, 12),  # 2
        (10, 8, 3, 0),  # 3
        (8, 7, 4, 3),  # 4
        (12, 2, 9, 11),  # 5
        (7, 6, 5, 4),  # 6
        (0, 3, 20, 1),  # 0 + 7 = 7
        (1, 20, 21, 2),  # 1 + 7 = 8
        (3, 4, 23, 20),  # 2 + 7 = 9
        (2, 21, 26, 9),  # 3 + 7 = 10
        (4, 5, 24, 23),  # 4 + 7 = 11
    )

    # assert b2 == ((20, 21, 26), (20, 23, 24))
    assert b2 == ((24, 23, 20), (20, 21, 26))


# @pytest.mark.skip("work in progress")
def test_domain_merge_key_0001_r0_p1_and_key_0001_r1_p0():
    """
        nnp0 = 24

        faces0 = ((0, 2, 3, 1), (0, 7, 4, 2), (2, 4, 5, 3), (3, 5, 6, 1), (4, 7, 8, 5),
                  (23, 19, 0, 22), (22, 0, 1, 21), (21, 1, 18, 20), (19, 16, 7, 0),
                  (1, 6, 17, 18), (16, 14, 13, 7), (7, 13, 12, 8))

                   -6->18         -7->17    -9->15
    -4->20 o---------o---------+----o         o    o -14->10    1.0
           |                   |    .
           |                   |    6         9    o -13->11    0.75
           |                   |    .
    -3->21 o         1         +----.    +         +            0.5
           |                *  |    .                             ^
           |              *    |    5. . . . .8. . o -12->12    0.25  |
           |            *    3 |         |         |                  |
           +---------*---------+---------*---------+            0.0   y-axis
           |            *    2 | 4     *           |
           |              *    |     *             |
           |                *  |  *                |
    -2->22 o         0         *         7         o -11->13   -0.5
           |                   |                   |
           |                   |                   |
           |                   |                   |
    -1->23 o---------o---------+---------o---------o        -1.0
                   -5->19              -8->16   -10->14

         -1.0      -0.5       0.0  0.25 0.5  0.75 1.0  --> x-axis

        bounds0 = ((23, 19, 16, 14), (14, 13, 12), (12, 8, 5), (5, 6, 17), (17, 18, 20),
                   (20, 21, 22, 23))

        nnp1 = 24

        faces1 = ((24, 26, 27, 25), (24, 31, 28, 26), (26, 28, 29, 27), (27, 29, 30, 25),
                  (28, 31, 32, 29), (29, 32, 33, 30), (25, 30, 41, 42), (30, 33, 39, 41),
                  (31, 37, 36, 32), (32, 36, 35, 33), (33, 35, 34, 39))

                    -6->42->17    -7->41    -9->39
    -4->44 o         o---------+----o----+----o----o -14->34    1.0
                     .         |         |         |
                     .         |    6->30|    9    o -13->35    0.75
                     .         |         |   ->33  |
    -3->45 o         1->25->6  +---------+---------+            0.5
                     .      *  |         |         |                  ^
                     .    *    |    5->29|    8    o -12->36    0.25  |
                     .  *    3 |         |   ->32  |                  |
           +         *------>27+---------*---------+            0.0   y-axis
                     .  *    2 | 4->28  *          |
                     .    *->26|     *             |
                     .      *  |  *                |
    -2->46 o         0. . . . .*. . . . .7. . . . .o -11       -0.5
                     ->24->5             ->31->8     ->37->12


    -1->47 o         o         +         o         o        -1.0
                    -5->43             -8->40    -10->38

         -1.0      -0.5       0.0  0.25 0.5  0.75 1.0  --> x-axis

        bounds1 = ((24, 31, 37), (37, 36, 35, 34), (34, 39, 41, 42), (42, 25, 24))
    """
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

    # boundaries, counterclockwise contour from lower left corner
    b0 = d0.boundaries
    b1 = d1.boundaries

    assert b0 == (
        (-1, -5, -8, -10),
        (-10, -11, -12),
        (-12, 8, 5),
        (5, 6, -7),
        (-7, -6, -4),
        (-4, -3, -2, -1),
    )

    assert b1 == (
        (0, 7, -11),
        (-11, -12, -13, -14),
        (-14, -9, -7, -6),
        (-6, 1, 0),
    )

    match2 = boundary_match(
        boundary0=b0,
        coordinates0=d0.mesh.coordinates,
        boundary1=b1,
        coordinates1=d1.mesh.coordinates,
        tolerance=1e-6,
    )

    assert match2 == (
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (-1, 0, 0, 0),
        (0, 0, 0, -2),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
    )

    d2 = domain_merge(domain0=d0, domain1=d1, tolerance=1e-6)

    m2 = d2.mesh
    b2 = d2.boundaries

    faces0 = (
        (0, 2, 3, 1),  # faces_dual
        (0, 7, 4, 2),
        (2, 4, 5, 3),
        (3, 5, 6, 1),
        (4, 7, 8, 5),
        (23, 19, 0, 22),  # faces_ports
        (22, 0, 1, 21),
        (21, 1, 18, 20),
        (19, 16, 7, 0),
        (1, 6, 17, 18),
        (16, 14, 13, 7),
        (7, 13, 12, 8),
    )

    faces1 = (
        (5, 26, 27, 6),  # faces_dual
        (5, 8, 28, 26),
        (26, 28, 29, 27),
        (27, 29, 30, 6),
        (28, 8, 32, 29),
        (29, 32, 33, 30),
        (6, 30, 41, 17),  # faces_ports
        (30, 33, 39, 41),
        (8, 12, 36, 32),
        (32, 36, 35, 33),
        (33, 35, 34, 39),
    )

    faces2 = faces0 + faces1

    assert m2.connectivity == faces2

    bounds0 = (
        (23, 19, 16, 14),
        (14, 13, 12),
        (12, 8, 5),
        (5, 6, 17),
        (17, 18, 20),
        (20, 21, 22, 23),
    )
    bounds1 = ((24, 31, 37), (37, 36, 35, 34), (34, 39, 41, 42), (42, 25, 24))

    bounds2 = bounds0[0:2] + bounds0[4:] + bounds1[1:3]

    assert bounds2 == b2


@pytest.mark.skip("work in progress")
def test_winding_number():
    """
    Reference:
    https://codegolf.stackexchange.com/questions/70600/compute-the-winding-number
    """

    # basic test
    input = ((1, 0), (1, 1), (-1, 1), (-1, -1), (1, -1), (1, 0))
    output = 1

    # repeated point test
    input = (
        (1, 0),
        (1, 0),
        (1, 1),
        (1, 1),
        (-1, 1),
        (-1, 1),
        (-1, -1),
        (-1, -1),
        (1, -1),
        (1, -1),
        (1, 0),
    )
    output = 1

    # clockwise test
    input = ((1, 0), (1, -1), (-1, -1), (-1, 1), (1, 1), (1, 0))
    output = -1

    # outside test
    input = ((1, 0), (1, 1), (2, 1), (1, 0))
    output = 0

    # mixed winding
    input = (
        (1, 0),
        (1, 1),
        (-1, 1),
        (-1, -1),
        (1, -1),
        (1, 0),
        (1, -1),
        (-1, -1),
        (-1, 1),
        (1, 1),
        (1, 0),
        (1, 1),
        (-1, 1),
        (-1, -1),
        (1, -1),
        (1, 0),
        (1, 1),
        (-1, 1),
        (-1, -1),
        (1, -1),
        (1, 0),
    )
    output = 2
