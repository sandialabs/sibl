"""This module tests the cp_solver (control point solver) implmentation.

To run
$ conda activate siblenv
$ cd ~/sibl
$ pytest /geo/tests/test_bspline_fit.py -v
"""

from pathlib import Path  # stop using os.path, use pathlib instead
from unittest import TestCase, main

import numpy as np

# import ptg.view_bspline as vbsp
import ptg.bspline_fit as bsf


class Test(TestCase):
    """Tests the creation of B-Spline view entities."""

    @classmethod
    def setUpClass(cls):
        cls.self_file = Path(__file__)
        cls.self_dir = cls.self_file.resolve().parent
        cls.data_dir = cls.self_dir.joinpath("../", "data", "bspline").resolve()
        cls.TOL = 1e-6  # tolerance
        cls.verbosity = True
        cls.sample_points = (
            (0.0, 0.0),
            (3.0, 4.0),
            (-1.0, 4.0),
            (-4.0, 0.0),
            (-4.0, 3.0),
        )  # Piegl Example 9.1, page 367
        cls.degree = 3  # Piegl ibid.

        return super().setUpClass()

    @classmethod
    def same(cls, a, b):
        same_to_tolerance = False
        l2norm_diff = np.linalg.norm(a - b)

        if cls.verbosity:
            print(f"array a = {a}")
            print(f"array b = {b}")
            print(f"l2norm_diff = {l2norm_diff}")

        if np.abs(l2norm_diff) < cls.TOL:
            same_to_tolerance = True

        return same_to_tolerance

    def test_001_sample_points_type_error(self):
        bad_sample_points = {
            "point1": [0.0, 0.0],
            "point2": [1.0, 1.0],
            "point3": [2.0, 4.0],
        }  # dict, which is the wrong type

        with self.assertRaises(TypeError):
            bsf.BSplineFit(bad_sample_points, self.degree)

    def test_002_degree_error(self):
        bad_degree = -1  # integer >= 0, so -1 is out of range for test

        with self.assertRaises(ValueError):
            bsf.BSplineFit(self.sample_points, bad_degree)


# def test_003_degree_too_small(self):
#     degree = -1  # integer >=0, so -1 is is out of range for test
#     B = bsf.BSplineFit(self.sample_points, degree)
#     a = 4

# def test_000_simple_least_squares(self):
#     # https://www.math.tamu.edu/~yvorobet/MATH304-503/Lect3-03web.pdf
#     # client data
#     # (sample_time t_s, x(t_s), y(t_s))
#     # or
#     # (sample_time t_s, x(t_s), y(t_s), z(t_s)))
#     samples = ((3.0, 1.0, 2.0), (5.0, 3.0, 2.0), (2.09, 1.0, 1))

#     # num_samples = 3
#     num_samples = len(samples)
#     num_space_dims = len(samples[0]) - 1  # 2D

#     num_control_points = 2

#     assert num_samples >= num_control_points
#     b = np.ones((num_samples, 1))  # samples, Ax = b
#     A = np.ones((num_samples, num_control_points))

#     A = np.array([[1.0, 2.0], [3.0, 2.0], [1.0, 1.0]])
#     b = np.array([3.0, 5.0, 2.09])
#     AtA = np.transpose(A) @ A
#     Atb = np.transpose(A) @ b
#     x = np.linalg.solve(AtA, Atb)

#     x_known = np.array([1.00, 1.01])
#     a = 4
#     self.assertTrue(self.same(x_known, x))


# retain main for debugging this file in VS code
if __name__ == "__main__":
    main()  # calls unittest.main()
