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


"""
Copyright 2023 Sandia National Laboratories

Notice: This computer software was prepared by National Technology and Engineering Solutions of
Sandia, LLC, hereinafter the Contractor, under Contract DE-NA0003525 with the Department of Energy
(DOE). All rights in the computer software are reserved by DOE on behalf of the United States
Government and the Contractor as provided in the Contract. You are authorized to use this computer
software for Governmental purposes but it is not to be released or distributed to the public.
NEITHER THE U.S. GOVERNMENT NOR THE CONTRACTOR MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR ASSUMES
ANY LIABILITY FOR THE USE OF THIS SOFTWARE. This notice including this sentence must appear on any
copies of this computer software. Export of this data may require a license from the United States
Government.
"""
