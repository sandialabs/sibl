"""This module is a unit test of the bspline implementation.

To run
$ conda activate sibl env
$ cd ~/sibl
$ pytest geo/tests/test_bspline.py -v
"""


from unittest import TestCase, main

import numpy as np

import ptg.bspline as bsp


class TestBSpline(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.TOL = 1e-6  # tolerance
        # cls.nti = 4  # number of time intervals per knot
        # t, e.g., nti=1 gives two sub-intervals, three evaluation points
        cls.verbosity = False
        cls.kv = [0, 2, 3]  # list, knot_vector
        cls.ki = 0  # non-negative integer, defaults to first index
        cls.degree = 0  # non-negative polynomial degree, defaults to 0 (constant)

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

    def test_000_initialization(self):
        knot_vector = [0, 1]
        coef = [1]
        degree = 0
        B = bsp.BSpline(knot_vector, coef, degree)
        self.assertIsInstance(B, bsp.BSpline)

    def test_001_knot_vector_minimum_length(self):
        knot_vector = [0]  # too short
        coef = [1]
        degree = 0
        B = bsp.BSpline(knot_vector, coef, degree)
        result = B.is_valid()
        self.assertIsInstance(result, AssertionError)
        self.assertTrue(result.args[0] == "Error: knot vector mininum length is two.")

    def test_002_degree_too_small_and_verbose(self):
        knot_vector = [0, 1]
        coef = [1]
        degree = -1  # integer >= 0, so -1 is out of range for test
        verbosity = True  # to test the verbose code lines
        B = bsp.BSpline(knot_vector, coef, degree, verbosity)
        result = B.is_valid()
        self.assertIsInstance(result, AssertionError)
        self.assertTrue(result.args[0] == "Error: degree must be non-negative.")

    def test_003_recover_bezier_linear(self):
        knot_vector = [0, 0, 1, 1]
        degree = 1  # linear

        coef_N00 = [1, 0]
        B01 = bsp.BSpline(knot_vector, coef_N00, degree)
        result = B01.is_valid()
        self.assertTrue(result)
        tmin, tmax, npts = 0, 1, 5
        t = np.linspace(tmin, tmax, npts, endpoint=True)
        y = B01.evaluate(t)
        y_known = [1.0, 0.75, 0.5, 0.25, 0.0]
        self.assertTrue(self.same(y_known, y))

        coef_N11 = [0, 1]
        B11 = bsp.BSpline(knot_vector, coef_N11, degree)
        result = B11.is_valid()
        self.assertTrue(result)
        tmin, tmax, npts = 0, 1, 5
        t = np.linspace(tmin, tmax, npts, endpoint=True)
        y = B11.evaluate(t)
        y_known = [0.0, 0.25, 0.5, 0.75, 1.0]
        self.assertTrue(self.same(y_known, y))

    def test_004_degree_zero_with_seven_knots(self):
        knot_vector = [0, 1, 2, 3, 4, 5, 6]
        degree = 0  # constant
        coef = [0, 1, 0, 0, 0, 0]
        B10 = bsp.BSpline(knot_vector, coef, degree)
        result = B10.is_valid()
        self.assertTrue(result)
        tmin, tmax, npts = knot_vector[0], knot_vector[-1], 13
        t = np.linspace(tmin, tmax, npts, endpoint=True)
        y = B10.evaluate(t)
        y_known = [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.assertTrue(self.same(y_known, y))
        a = 4

    def test_100_bspline_basis_quadratic_eight_knots(self):
        """Know example from NURBS Book, Piegl and Tiller, Ex2.2, Fig 2.6"""
        KV = [0, 0, 0, 1, 2, 3, 4, 4, 5, 5, 5]  # knot vector
        DEGREE = 2  # quadratic
        NBI = 3  # number of bisection intervals per knot span
        NCP = 8  # number of control points

        knots_lhs = KV[0:-1]  # left-hand-side knot values
        knots_rhs = KV[1:]  # right-hand-side knot values
        knot_spans = np.array(knots_rhs) - np.array(knots_lhs)
        dt = knot_spans / (2 ** NBI)
        assert all([dti >= 0 for dti in dt]), "Error: knot vector is decreasing."

        num_knots = len(KV)
        t = [
            knots_lhs[k] + j * dt[k]
            for k in np.arange(num_knots - 1)
            for j in np.arange(2 ** NBI)
        ]
        t.append(KV[-1])
        t = np.array(t)

        N_calc = []  # basis functions calculated by bsp.Bspline

        for i in np.arange(NCP):

            coef = np.zeros(NCP)
            coef[i] = 1.0

            B = bsp.BSpline(KV, coef, DEGREE)

            if B.is_valid():
                y = B.evaluate(t)
                N_calc.append(y)

        N_known = np.zeros((NCP, t.size), dtype=t.dtype)

        # Citation to give credit for Pythonic test implementation on knot intervals:
        # Roberto Agromayor (RoberAgro) Ph.D. candidate in turbomachinery design and
        # optimization at the Norwegian University of Science and Technology (NTNU)
        # https://github.com/RoberAgro/nurbspy/blob/master/tests/test_nurbs_basis_functions.py

        for j, t in enumerate(t):
            N02 = (1 - t) ** 2 * (0 <= t < 1)
            N12 = (2 * t - 3 / 2 * t ** 2) * (0 <= t < 1) + (1 / 2 * (2 - t) ** 2) * (
                1 <= t < 2
            )
            N22 = (
                (1 / 2 * t ** 2) * (0 <= t < 1)
                + (-3 / 2 + 3 * t - t ** 2) * (1 <= t < 2)
                + (1 / 2 * (3 - t) ** 2) * (2 <= t < 3)
            )
            N32 = (
                (1 / 2 * (t - 1) ** 2) * (1 <= t < 2)
                + (-11 / 2 + 5 * t - t ** 2) * (2 <= t < 3)
                + (1 / 2 * (4 - t) ** 2) * (3 <= t < 4)
            )
            N42 = (1 / 2 * (t - 2) ** 2) * (2 <= t < 3) + (
                -16 + 10 * t - 3 / 2 * t ** 2
            ) * (3 <= t < 4)
            N52 = (t - 3) ** 2 * (3 <= t < 4) + (5 - t) ** 2 * (4 <= t < 5)
            N62 = (2 * (t - 4) * (5 - t)) * (4 <= t < 5)
            N72 = (t - 4) ** 2 * (4 <= t <= 5)
            N_known[:, j] = np.asarray([N02, N12, N22, N32, N42, N52, N62, N72])

        for i in np.arange(NCP):
            self.assertTrue(self.same(N_known[i], N_calc[i]))


# retain main for debugging this file in VS code
if __name__ == "__main__":
    main()  # calls unittest.main()
