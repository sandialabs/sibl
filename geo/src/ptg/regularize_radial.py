"""This function returns the radial control point coordinates (P1x, P1y) for a
Bezier quadratic surface, given the bounding control points (P0x, P0y) and
(P2x, P2y) interpolating at a given radius and give theta_0 and theta_2, where
theta_1 is assumed as 1/2 (theta_0 + theta_2).
"""

from typing import Tuple

import numpy as np


def regularize_radial(
    *, radius: float, theta_0: float, theta_2: float
) -> Tuple[float, float]:
    """
    Arguments:

    radius (float): The radius interopolated by control points (P0x, P0y) and (P2x, P2y).
    theta_0 (float): The angle from *--> (+CCW) in radians of the first control point.
    theta_2 (float) The angle of the third control points.
    """
    theta_1 = 0.5 * (theta_0 + theta_2)
    P1x = (
        2.0
        * radius
        * (np.cos(theta_1) - 0.25 * np.cos(theta_0) - 0.25 * np.cos(theta_2))
    )

    P1y = (
        2.0
        * radius
        * (np.sin(theta_1) - 0.25 * np.sin(theta_0) - 0.25 * np.sin(theta_2))
    )

    return P1x, P1y
