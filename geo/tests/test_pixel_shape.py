import numpy as np

import pytest

from ptg.pixel_shape import PixelCube as pixel_cube
from ptg.pixel_shape import PixelCylinder as pixel_cylinder
from ptg.pixel_shape import PixelSphere as pixel_sphere

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
    assert bb.width == 3
    assert bb.depth == 3
    assert bb.height == 3


def test_sphere_construction():
    sphere = pixel_sphere(radius=2.5, pixels_per_len=1)
    assert sphere  # tests constructor

    # tests of radius = 2.5 len,
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
    assert bb.width == 5
    assert bb.depth == 5
    assert bb.height == 5


def test_cylinder_construction():
    cylinder = pixel_cylinder(radius=2.5, height=3.0, pixels_per_len=1)
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
    assert bb.width == 5
    assert bb.depth == 5
    assert bb.height == 3


def test_sphere_non_positive_radius():
    bad_radius = 0  # radius should be 1 or greater
    with pytest.raises(ValueError):
        pixel_sphere(radius=bad_radius)


def test_cylinder_non_positive_radius():
    bad_radius = 0  # radius should be 1 or greater
    with pytest.raises(ValueError):
        pixel_cylinder(radius=bad_radius)


def test_cylinder_non_positive_height():
    good_radius = 10
    bad_height = 0  # radius should be 1 or greater
    with pytest.raises(ValueError):
        pixel_cylinder(radius=good_radius, height=bad_height)


def test_sphere_non_positive_pixels_per_len():
    good_radius = 4  # len, some positive number is good
    bad_pixels_per_len = 0  # should be 1 or greater
    with pytest.raises(ValueError):
        pixel_sphere(radius=good_radius, pixels_per_len=bad_pixels_per_len)


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


# def test_add_shape():
#    pc1 = pixel_cube()


def test_cylinder_non_positive_pixels_per_len():
    good_radius = 4  # len, some positive number is good
    good_height = 2 * good_radius  # len, a very squat cylinder
    bad_pixels_per_len = 0  # should be 1 or greater
    with pytest.raises(ValueError):
        pixel_cylinder(
            radius=good_radius, height=good_height, pixels_per_len=bad_pixels_per_len
        )


@pytest.mark.skip(reason="test not yet completed")
def test_sphere_one_len_radius_high_resolution():
    radius = 1  # len
    pixels_per_len = 10  # pixels per len unit
    sphere = pixel_sphere(radius=radius, pixels_per_len=pixels_per_len)
    _ = sphere.mask
    pass
