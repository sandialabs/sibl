import numpy as np

import pytest

from ptg.shape import PixelSphere as ps

# References:
# https://code.visualstudio.com/docs/python/testing#_enable-a-test-framework

# > pytest --collect-only


def test_construction_and_defaults():
    s = ps()
    assert s  # tests constructor

    # tests defautls of radius = 1 len, pixels_per_len = 2
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

    calc_mask = s.mask
    calc_mask_vector = np.ndarray.flatten(calc_mask)
    tolerance = 1e-6  # very small value
    abs_error = np.abs(np.linalg.norm(known_mask_vector - calc_mask_vector))
    assert abs_error < tolerance


def test_non_positive_radius():
    bad_radius = 0  # radius should be 1 or greater
    with pytest.raises(ValueError):
        ps(bad_radius)


def test_non_positive_pixels_per_len():
    good_radius = 4  # some positive number is good
    bad_pixels_per_len = 0  # should be 1 or greater
    with pytest.raises(ValueError):
        ps(good_radius, bad_pixels_per_len)


@pytest.mark.skip(reason="test not yet completed")
def test_one_len_radius_high_resolution():
    radius = 1  # len units
    pixels_per_len = 10  # pixels per len unit
    s = ps(radius, pixels_per_len)
    m = s.mask
    pass
