"""This module tests the regularize_radial function."""

import numpy as np

import pytest

import ptg.regularize_radial as rr


def test_patch_1():
    deg2rad = np.pi / 180.0  # rad
    angle_0 = 0.0  # rad
    angle_2 = 45.0 * deg2rad  # rad
    r = 20.0  # length units
    P1x, P1y = rr.regularize_radial(radius=r, theta_0=angle_0, theta_2=angle_2)
    assert P1x == pytest.approx(19.884113488585996)
    assert P1y == pytest.approx(8.236269482738116)


def test_patch_2():
    deg2rad = np.pi / 180.0  # rad
    angle_0 = 45.0 * deg2rad  # rad
    angle_2 = 90.0 * deg2rad  # rad
    r = 20.0  # length units
    P1x, P1y = rr.regularize_radial(radius=r, theta_0=angle_0, theta_2=angle_2)
    assert P1x == pytest.approx(8.236269482738116)
    assert P1y == pytest.approx(19.884113488585996)


def test_patch_3():
    deg2rad = np.pi / 180.0  # rad
    angle_0 = 0.0  # rad
    angle_2 = 45.0 * deg2rad  # rad
    r = 30.0  # length units
    P1x, P1y = rr.regularize_radial(radius=r, theta_0=angle_0, theta_2=angle_2)
    assert P1x == pytest.approx(29.826170232878994)
    assert P1y == pytest.approx(12.354404224107174)
