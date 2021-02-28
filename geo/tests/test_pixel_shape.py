import numpy as np

import pytest

from ptg.pixel_shape import PixelCube as pixel_cube
from ptg.pixel_shape import PixelCylinder as pixel_cylinder
from ptg.pixel_shape import PixelSphere as pixel_sphere
from ptg.pixel_shape import PixelQuarterCylinder as pixel_quarter_cylinder

# References:
# https://code.visualstudio.com/docs/python/testing#_enable-a-test-framework

# > pytest --collect-only

# Sphere and cylinder (stacked disc) verified against scikit-image 2021-01-03.
# Generate Structuring Elements
# https://scikit-image.org/docs/stable/auto_examples/numpy_operations/plot_structuring_elements.html#sphx-glr-auto-examples-numpy-operations-plot-structuring-elements-py


def test_cube_construction_and_verbose():
    cube = pixel_cube(pixels_per_len=3, verbose=True)
    assert cube  # tests constructor

    # tests defaults of width = 1 len, pixels_per_len = 2
    known_mask = np.array(
        [
            [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
            [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
            [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        ]
    )
    known_mask_vector = np.ndarray.flatten(known_mask)

    calc_mask = cube.mask
    calc_mask_vector = np.ndarray.flatten(calc_mask)
    tolerance = 1e-6  # very small value
    abs_error = np.abs(np.linalg.norm(known_mask_vector - calc_mask_vector))
    assert abs_error < tolerance

    bb = cube.bounding_box
    assert bb.dx == 3
    assert bb.dy == 3
    assert bb.dz == 3


def test_cube_anchor_and_bounding_box():
    cube = pixel_cube(
        anchor_x=1.0, anchor_y=2.0, anchor_z=3.0, dx=1.0, pixels_per_len=2
    )
    _anchor = cube.anchor
    assert _anchor.x == 2  # pixels
    assert _anchor.y == 4
    assert _anchor.z == 6

    _pbb = cube.bounding_box
    assert _pbb.dx == 2  # pixels
    assert _pbb.dy == 2
    assert _pbb.dz == 2


def test_cube_non_zero_anchor():
    x, y, z = 2.0, 3.0, 4.0  # cm offset from origin
    pc = pixel_cube(anchor_x=x, anchor_y=y, anchor_z=z)
    calc_anchor = pc.anchor  # pixel (int)
    assert calc_anchor.x == 2  # pixel (int)
    assert calc_anchor.y == 3
    assert calc_anchor.z == 4


def test_cube_non_default_non_zero_anchor():
    x, y, z = 2.0, 3.0, 4.0  # cm offset from origin
    pc = pixel_cube(anchor_x=x, anchor_y=y, anchor_z=z, pixels_per_len=5)
    calc_anchor = pc.anchor  # pixel (int)
    assert calc_anchor.x == 10  # pixel (int)
    assert calc_anchor.y == 15
    assert calc_anchor.z == 20


def test_cylinder_construction_od4():
    cylinder = pixel_cylinder(
        height=1.0, diameter_inner=0.0, diameter_outer=4.0, pixels_per_len=1
    )
    assert cylinder  # tests constructor

    known_mask = np.array(
        [
            [
                [0, 1, 1, 0],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [0, 1, 1, 0],
            ]
        ]
    )
    known_mask_vector = np.ndarray.flatten(known_mask)

    calc_mask = cylinder.mask
    calc_mask_vector = np.ndarray.flatten(calc_mask)
    tolerance = 1e-6  # very small value
    abs_error = np.abs(np.linalg.norm(known_mask_vector - calc_mask_vector))
    assert abs_error < tolerance

    bb = cylinder.bounding_box
    assert bb.dx == 1
    assert bb.dy == 4
    assert bb.dz == 4


def test_cylinder_construction_od5():
    cylinder = pixel_cylinder(
        height=3.0, diameter_inner=0.0, diameter_outer=5.0, pixels_per_len=1
    )
    assert cylinder  # tests constructor

    known_mask = np.array(
        [
            [
                [0, 0, 1, 0, 0],
                [0, 1, 1, 1, 0],
                [1, 1, 1, 1, 1],
                [0, 1, 1, 1, 0],
                [0, 0, 1, 0, 0],
            ],
            [
                [0, 0, 1, 0, 0],
                [0, 1, 1, 1, 0],
                [1, 1, 1, 1, 1],
                [0, 1, 1, 1, 0],
                [0, 0, 1, 0, 0],
            ],
            [
                [0, 0, 1, 0, 0],
                [0, 1, 1, 1, 0],
                [1, 1, 1, 1, 1],
                [0, 1, 1, 1, 0],
                [0, 0, 1, 0, 0],
            ],
        ]
    )
    known_mask_vector = np.ndarray.flatten(known_mask)

    calc_mask = cylinder.mask
    calc_mask_vector = np.ndarray.flatten(calc_mask)
    tolerance = 1e-6  # very small value
    abs_error = np.abs(np.linalg.norm(known_mask_vector - calc_mask_vector))
    assert abs_error < tolerance

    bb = cylinder.bounding_box
    assert bb.dx == 3
    assert bb.dy == 5
    assert bb.dz == 5


def test_cylinder_hallow_construction():
    cylinder = pixel_cylinder(
        height=1.0, diameter_inner=6.0, diameter_outer=12.0, pixels_per_len=1
    )
    assert cylinder  # tests constructor

    known_mask = np.array(
        [
            [
                [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0],
                [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
                [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
                [0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
            ]
        ]
    )
    known_mask_vector = np.ndarray.flatten(known_mask)

    calc_mask = cylinder.mask
    calc_mask_vector = np.ndarray.flatten(calc_mask)
    tolerance = 1e-6  # very small value
    abs_error = np.abs(np.linalg.norm(known_mask_vector - calc_mask_vector))
    assert abs_error < tolerance

    bb = cylinder.bounding_box
    assert bb.dx == 1
    assert bb.dy == 12
    assert bb.dz == 12


def test_cylinder_non_positive_pixels_per_len():
    good_diameter = 4  # len, some positive number is good
    good_height = 2 * good_diameter  # len, a very squat cylinder
    bad_pixels_per_len = 0  # should be 1 or greater
    with pytest.raises(ValueError):
        pixel_cylinder(
            diameter_outer=good_diameter,
            height=good_height,
            pixels_per_len=bad_pixels_per_len,
        )


def test_cylinder_non_positive_diameter():
    bad_value = 0  # diamter should be 1 or greater
    with pytest.raises(ValueError):
        pixel_cylinder(diameter_outer=bad_value)


def test_cylinder_non_positive_height():
    good_diameter = 10
    bad_height = 0  # height should be 1 or greater
    with pytest.raises(ValueError):
        pixel_cylinder(diameter_outer=good_diameter, height=bad_height)


def test_cylinder_diameter_inner_exceeds_diameter_outer():
    ID = 10  # inner diameter
    OD = 5  # outer diameter
    with pytest.raises(ValueError):
        pixel_cylinder(diameter_inner=ID, diameter_outer=OD)


def test_quarter_cylinder_construction():
    qtr_cylinder = pixel_quarter_cylinder(
        height=2, radius_inner=3.0, radius_outer=6.0, pixels_per_len=1
    )
    assert qtr_cylinder  # tests constructor

    known_mask = np.array(
        [
            [
                [0, 0, 0, 1, 1, 1],
                [0, 0, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 0],
                [1, 1, 1, 1, 0, 0],
                [1, 1, 1, 0, 0, 0],
                [1, 0, 0, 0, 0, 0],
            ],
            [
                [0, 0, 0, 1, 1, 1],
                [0, 0, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 0],
                [1, 1, 1, 1, 0, 0],
                [1, 1, 1, 0, 0, 0],
                [1, 0, 0, 0, 0, 0],
            ],
        ]
    )
    known_mask_vector = np.ndarray.flatten(known_mask)

    calc_mask = qtr_cylinder.mask
    calc_mask_vector = np.ndarray.flatten(calc_mask)
    tolerance = 1e-6  # very small value
    abs_error = np.abs(np.linalg.norm(known_mask_vector - calc_mask_vector))
    assert abs_error < tolerance

    bb = qtr_cylinder.bounding_box
    assert bb.dx == 2
    assert bb.dy == 6
    assert bb.dz == 6


def test_quarter_cylinder_negative_inner_radius():
    bad_inner_radius = -1.0  # bad, must be >= 0.0
    with pytest.raises(ValueError):
        pixel_quarter_cylinder(radius_inner=bad_inner_radius)


def test_quarter_cylinder_radius_inner_exceeds_radius_outer():
    IR = 10  # inner radius
    OR = 5  # outer radius
    with pytest.raises(ValueError):
        pixel_quarter_cylinder(radius_inner=IR, radius_outer=OR)


def test_sphere_construction():
    sphere = pixel_sphere(diameter=5.0, pixels_per_len=1)
    assert sphere  # tests constructor

    # tests of radius = 2.5 len -> diameter = 5.0
    # pixels_per_len = 1
    known_mask = np.array(
        [
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ],
            [
                [0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 1, 1, 1, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0],
            ],
            [
                [0, 0, 1, 0, 0],
                [0, 1, 1, 1, 0],
                [1, 1, 1, 1, 1],
                [0, 1, 1, 1, 0],
                [0, 0, 1, 0, 0],
            ],
            [
                [0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 1, 1, 1, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0],
            ],
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ],
        ]
    )
    known_mask_vector = np.ndarray.flatten(known_mask)

    calc_mask = sphere.mask
    calc_mask_vector = np.ndarray.flatten(calc_mask)
    tolerance = 1e-6  # very small value
    abs_error = np.abs(np.linalg.norm(known_mask_vector - calc_mask_vector))
    assert abs_error < tolerance

    bb = sphere.bounding_box
    assert bb.dx == 5
    assert bb.dy == 5
    assert bb.dz == 5


def test_sphere_non_positive_diameter():
    bad_value = 0  # diamter should be 1 or greater
    with pytest.raises(ValueError):
        pixel_sphere(diameter=bad_value)


def test_sphere_non_positive_pixels_per_len():
    good_diameter = 4  # len, some positive number is good
    bad_pixels_per_len = 0  # should be 1 or greater
    with pytest.raises(ValueError):
        pixel_sphere(diameter=good_diameter, pixels_per_len=bad_pixels_per_len)


@pytest.mark.skip(reason="test not yet completed")
def test_sphere_one_len_radius_high_resolution():
    sphere = pixel_sphere(diameter=1, pixels_per_len=5)
    _mask = sphere.mask
    pass


@pytest.mark.skip(reason="test not yet completed")
def test_small_mesh_1x_1y_2z():

    #            Two-element finite element mesh
    #
    #             Node (x, y, z) positions       Node Numbers
    #
    #             y-axis    x-axis
    #               ^      /
    #               |     /
    #       /       | *---*---* 3                10--11--12
    #      /        |/|  /|  /| 2                /|  /|  /|
    #     /       3 *---*---* | 1               4---5---6 |
    #    1        2 | *-|-*-|-* 0               | 7 | 8 | 9
    #   x         1 |/  |/  |/                  |/  |/  |/
    #  0 -------  0 *---*---*------> z-axis     1---2---3
    # /             012345678
    #
    # To match the Exodus II format for a hexahedral finite elment (see reference:
    # https://prod-ng.sandia.gov/techlib-noauth/access-control.cgi/1992/922137.pdf)
    # page 10, the first face proceeeds with counter-clockwise node enumeration with
    # normal vector pointing into hex element; the second face, parallel to the first,
    # proceeds with counter-clockwise node enumeration with normal vector pointing
    # out of the hex element.
    #
    #              8 *-----* 7
    #               /|    /|
    #              / |   / |
    #           5 *-----*6 |         assumed as z for now for Exodus II
    #             | 4*--|--* 3        ^
    #             | /   | /           | / assumed as y for now for Exodus II
    #             |/    |/            |/
    #           1 *-----* 2           +--> assumed as x for now for Exodus II
    #
    # See also for splines: https://gsjaardema.github.io/seacas-docs/gen3d-updates.pdf
    #

    expected_node_list = [
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 4.0],
        [0.0, 0.0, 8.0],
        [0.0, 3.0, 0.0],
        [0.0, 3.0, 4.0],
        [0.0, 3.0, 8.0],
        [1.0, 0.0, 0.0],
        [1.0, 0.0, 4.0],
        [1.0, 0.0, 8.0],
        [1.0, 3.0, 0.0],
        [1.0, 3.0, 4.0],
        [1.0, 3.0, 8.0],
    ]

    expected_element_list = [
        [1, 7, 10, 4, 2, 8, 11, 5],
        [2, 8, 11, 5, 3, 9, 12, 6],
    ]
