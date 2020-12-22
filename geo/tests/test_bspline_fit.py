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
            (-4.0, -3.0),
        )  # Piegl Example 9.1, page 367
        cls.degree = 3  # Piegl ibid.
        # cls.kwargs = {"sample_time_method": "chord"}
        cls.sample_time_method = "chord"

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

    def test_003_bad_sample_time_method(self):
        bad_sample_time_method = "bad_method"

        with self.assertRaises(ValueError):
            bsf.BSplineFit(
                self.sample_points, self.degree, self.verbosity, bad_sample_time_method
            )

    def test_004_Piegl_example_9p1(self):
        b = bsf.BSplineFit(
            self.sample_points, self.degree, self.verbosity, self.sample_time_method
        )
        calc_sample_times = b.sample_times

        # Piegl, page 367, known sample times are 0, 5/17, 9/17, 14/17, 1.
        known_sample_times = (
            0.0,
            0.29411764705882354,
            0.5294117647058824,
            0.8235294117647058,
            1.0,
        )

        self.assertTrue(self.same(calc_sample_times, known_sample_times))

        calc_knot_vector = b.knot_vector
        # Piegl, page 368, known knot vector is [0, 0, 0, 0, 28/51, 1, 1, 1, 1]
        known_knot_vector = (0.0, 0.0, 0.0, 0.0, 0.549019607843137, 1.0, 1.0, 1.0, 1.0)
        self.assertTrue(self.same(calc_knot_vector, known_knot_vector))

        calc_control_points = b.control_points
        known_control_points = np.array(
            [
                [0.0, 0.0],
                [7.3169635171119936, 3.6867775257587367],
                [-2.958130565851424, 6.678276528176592],
                [-4.494953466891109, -0.6736915062424752],
                [-4.0, -3.0],
            ]
        )  # evaluated 2020-12-21 reference:
        #  https://github.com/orbingol/geomdl-examples/blob/master/fitting/interpolation/global_curve2d.py

        difference_matrix = calc_control_points - known_control_points
        Frobenius_norm = np.linalg.norm(difference_matrix, ord="fro")
        self.assertTrue(Frobenius_norm < self.TOL)

    def test_005_Piegl_example_9p1_Bingol_centripetal(self):
        centripetal_sample_method = "centripetal"

        b = bsf.BSplineFit(
            self.sample_points, self.degree, self.verbosity, centripetal_sample_method
        )
        calc_sample_times = b.sample_times

        # evaluated 2020-12-21 reference:
        #  https://github.com/orbingol/geomdl-examples/blob/master/fitting/interpolation/global_curve2d.py
        DEN = np.sqrt(5) + np.sqrt(4) + np.sqrt(5) + np.sqrt(3)
        known_sample_times = (
            0.0,
            np.sqrt(5) / DEN,
            (np.sqrt(5) + np.sqrt(4)) / DEN,
            (np.sqrt(5) + np.sqrt(4) + np.sqrt(5)) / DEN,
            1.0,
        )

        self.assertTrue(self.same(calc_sample_times, known_sample_times))

        calc_knot_vector = b.knot_vector
        #   # Piegl, page 368, known knot vector is [0, 0, 0, 0, 28/51, 1, 1, 1, 1]
        #   # known_knot_vector = (0.0, 0.0, 0.0, 0.0, 0.549019607843137, 1.0, 1.0, 1.0, 1.0)
        # evaluated 2020-12-21 reference:
        #  https://github.com/orbingol/geomdl-examples/blob/master/fitting/interpolation/global_curve2d.py
        known_knot_vector = (0.0, 0.0, 0.0, 0.0, 0.525921389676195, 1.0, 1.0, 1.0, 1.0)
        self.assertTrue(self.same(calc_knot_vector, known_knot_vector))

        calc_control_points = b.control_points
        known_control_points = np.array(
            [
                [0.0, 0.0],
                [6.844809006430229, 3.6830706809273708],
                [-2.780244455052183, 7.09266371886821],
                [-4.75497856997568, -1.614237702476598],
                [-4.0, -3.0],
            ]
        )  # evaluated 2020-12-21 reference:
        #  https://github.com/orbingol/geomdl-examples/blob/master/fitting/interpolation/global_curve2d.py

        difference_matrix = calc_control_points - known_control_points
        Frobenius_norm = np.linalg.norm(difference_matrix, ord="fro")
        self.assertTrue(Frobenius_norm < self.TOL)

    def test_006_bad_knot_method(self):
        bad_knot_method = "bad_method"

        with self.assertRaises(ValueError):
            bsf.BSplineFit(
                self.sample_points,
                self.degree,
                self.verbosity,
                self.sample_time_method,
                bad_knot_method,
            )

    def test_007_Rogers_example_3p9(self):
        # Rogers, Example 3.9, page 92.
        points = ((0.0, 0.0), (1.5, 2.0), (3.0, 2.5), (4.5, 2.0), (6.0, 0.0))
        p = 2  # quadratic degree, (which is third order)
        speak_to_me = True
        method_samples = "chord"
        method_knots = "equal"

        b = bsf.BSplineFit(
            sample_points=points,
            degree=p,
            verbose=speak_to_me,
            sample_time_method=method_samples,
            knot_method=method_knots,
        )

        calc_sample_times = b.sample_times
        D21 = 5 / 2
        D32 = np.sqrt((3 / 2) ** 2 + (1 / 2) ** 2)
        D43 = np.sqrt((3 / 2) ** 2 + (-1 / 2) ** 2)
        D54 = 5 / 2
        DEN = D21 + D32 + D43 + D54
        known_sample_times = (
            0.0,
            D21 / DEN,
            (D21 + D32) / DEN,
            (D21 + D32 + D43) / DEN,
            1.0,
        )
        self.assertTrue(self.same(calc_sample_times, known_sample_times))

        calc_knot_vector = b.knot_vector
        # known_knot_vector = (0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0)
        # normalize, becaus the BSplineFit algorithm normalizes the knot vector:
        known_knot_vector = (0.0, 0.0, 0.0, 1 / 3, 2 / 3, 1.0, 1.0, 1.0)
        self.assertTrue(self.same(calc_knot_vector, known_knot_vector))

        calc_basis_matrix = b.basis_matrix
        known_basis_matrix = np.array(
            [
                [1.0, 0.0, 0.0, 0.0, 0.0],
                [0.007, 0.571, 0.422, 0.0, 0.0],
                [0.0, 0.125, 0.75, 0.125, 0.0],
                [0.0, 0.0, 0.422, 0.571, 0.007],
                [0.0, 0.0, 0.0, 0.0, 1.0],
            ]
        )  # Rogers, page 93, second equation
        difference_matrix = calc_basis_matrix - known_basis_matrix
        Frobenius_norm = np.linalg.norm(difference_matrix, ord="fro")
        TOL_MATRIX = 0.0008  # some small number larger than self.TOL, book 3 sig fig
        self.assertTrue(Frobenius_norm < TOL_MATRIX)

        calc_control_points = b.control_points
        known_control_points = np.array(
            [[0.0, 0.0], [0.409, 1.378], [3.0, 2.874], [5.591, 1.377], [6.0, 0.0]]
        )  # Rogers, page 93, fifth equation
        difference_matrix = calc_control_points - known_control_points
        Frobenius_norm = np.linalg.norm(difference_matrix, ord="fro")
        TOL_MATRIX = 0.0012  # some small number larger than self.TOL, book 3 sig fig
        self.assertTrue(Frobenius_norm < TOL_MATRIX)


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
