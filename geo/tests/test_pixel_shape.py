import numpy as np

import pytest

from ptg.pixel_shape import PixelSphere as pixel_sphere
from ptg.pixel_shape import PixelCylinder as pixel_cylinder

# References:
# https://code.visualstudio.com/docs/python/testing#_enable-a-test-framework

# > pytest --collect-only


def test_sphere_construction_and_defaults():
    sphere = pixel_sphere()
    assert sphere  # tests constructor

    # tests defaults of radius = 1 len, pixels_per_len = 2
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


def test_cylinder_construction():
    # tests defaults of radius = 1 len, pixels_per_len = 2
    good_radius = 1  # len, some positive number is good
    good_height = good_radius  # half-cubic bounding box, squat z size
    cylinder = pixel_cylinder(good_radius, good_height)
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


def test_sphere_non_positive_radius():
    bad_radius = 0  # radius should be 1 or greater
    with pytest.raises(ValueError):
        pixel_sphere(bad_radius)


def test_cylinder_non_positive_radius():
    bad_radius = 0  # radius should be 1 or greater
    with pytest.raises(ValueError):
        pixel_cylinder(bad_radius)


def test_cylinder_non_positive_height():
    good_radius = 10
    bad_height = 0  # radius should be 1 or greater
    with pytest.raises(ValueError):
        pixel_cylinder(good_radius, bad_height)


def test_sphere_non_positive_pixels_per_len():
    good_radius = 4  # len, some positive number is good
    bad_pixels_per_len = 0  # should be 1 or greater
    with pytest.raises(ValueError):
        pixel_sphere(good_radius, bad_pixels_per_len)


def test_cylinder_non_positive_pixels_per_len():
    good_radius = 4  # len, some positive number is good
    good_height = 2 * good_radius  # len, a very squat cylinder
    bad_pixels_per_len = 0  # should be 1 or greater
    with pytest.raises(ValueError):
        pixel_cylinder(good_radius, good_height, bad_pixels_per_len)


def test_cylinder_non_positive_pixels_per_len():
    good_radius = 4  # len, some positive number is good
    good_height = 2 * good_radius  # len, a very squat cylinder
    bad_pixels_per_len = 0  # should be 1 or greater
    with pytest.raises(ValueError):
        pixel_cylinder(good_radius, good_height, bad_pixels_per_len)


@pytest.mark.skip(reason="test not yet completed")
def test_sphere_one_len_radius_high_resolution():
    radius = 1  # len
    pixels_per_len = 10  # pixels per len unit
    sphere = pixel_sphere(radius, pixels_per_len)
    _ = sphere.mask
    pass
