# test_bspline_polynomial.py
"""
This module is a unit test of the bspline_polynomial implementation.

To run
$ conda load siblenv
$ cd ~/sibl
$ black --check geo/tests/test_bspline_polynomial.py
$ pytest geo/tests/test_bspline_polynomial.py -v
$ pytest geo/tests/test_bspline_polynomial.py -v --cov=geo/src/ptg --cov-report term-missing
"""
# from unittest import TestCase
from unittest import TestCase, main

import numpy as np

# import ptg.code.bspline_polynomial as bp
# import ptg.bspline_polynomial as bp
import ptg.bspline_manual as bp


class TestBSplinePoly(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.TOL = 1e-6  # tolerance
        cls.nti = 4  # number of time intervals per knot
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

    def test_001_knot_vector_minimum_length(self):
        kv_too_short = [0]
        calc = bp.bspline_polynomial(kv_too_short)
        self.assertIsInstance(calc, AssertionError)
        self.assertTrue(
            calc.args[0] == "Error: knot vector length must be two or larger."
        )

    def test_002_knot_index_too_low(self):
        bad_knot_index = -1
        calc = bp.bspline_polynomial(self.kv, bad_knot_index)
        self.assertIsInstance(calc, AssertionError)
        self.assertTrue(
            calc.args[0] == "Error: knot index knot_i must be non-negative."
        )

    def test_003_degree_too_small(self):
        degree = -1  # integer >= 0, so -1 is out of range for test
        calc = bp.bspline_polynomial(self.kv, self.ki, degree)
        self.assertIsInstance(calc, AssertionError)
        self.assertTrue(
            calc.args[0] == "Error: polynomial degree p must be non-negative."
        )

    def test_004_degree_too_large(self):
        degree = 2  # integer >= 0, but quadratic and higher not yet implemented
        calc = bp.bspline_polynomial(self.kv, self.ki, degree)
        self.assertIsInstance(calc, AssertionError)
        self.assertTrue(
            calc.args[0] == "Error: polynomial degree p exceeds maximum of 1"
        )

    def test_005_number_of_time_intervals(self):
        bad_number_of_intervals = 0
        calc = bp.bspline_polynomial(
            self.kv, self.ki, self.degree, bad_number_of_intervals
        )
        self.assertIsInstance(calc, AssertionError)
        self.assertTrue(
            calc.args[0] == "Error: number of time intervals nti must be 1 or greater."
        )

    def test_006_nti_out_of_range_and_verbose(self):
        bad_number_of_intervals = 0
        calc = bp.bspline_polynomial(
            self.kv, self.ki, self.degree, bad_number_of_intervals, verbose=True
        )
        self.assertIsInstance(calc, AssertionError)
        self.assertTrue(
            calc.args[0] == "Error: number of time intervals nti must be 1 or greater."
        )

    def test_007_knot_index_too_high(self):
        # Python's zero-based index makes the integer length of the knot_vector
        # be the first index to be out of range, thus test this
        bad_knot_index = len(self.kv)
        calc = bp.bspline_polynomial(self.kv, bad_knot_index)
        self.assertIsInstance(calc, AssertionError)
        self.assertTrue(
            calc.args[0]
            == "Error: knot index knot_i exceeds knot vector length minus 1."
        )

    def test_008_decreasing_knots(self):
        # knot vector must be non-decreasing sequence, so test error
        # checking for a decreasing knot vector sequence
        bad_knot_vector = [0, 2, 1]
        calc = bp.bspline_polynomial(bad_knot_vector)
        self.assertIsInstance(calc, AssertionError)
        self.assertTrue(calc.args[0] == "Error: knot vector is decreasing.")

    def test_N00_and_verbose(self):
        calc = bp.bspline_polynomial(
            self.kv, self.ki, self.degree, self.nti, verbose=True
        )
        known_t = [0, 0.5, 1, 1.5, 2, 2.25, 2.5, 2.75, 3]  # nti = 2
        known_y = [1, 1, 1, 1, 0, 0, 0, 0, 0]
        self.assertTrue(self.same(known_t, calc[0]))
        self.assertTrue(self.same(known_y, calc[1]))

    def test_N10(self):
        knot_index = 1  # integer >= 0
        calc = bp.bspline_polynomial(self.kv, knot_index, self.degree, self.nti)
        known_t = [0, 0.5, 1, 1.5, 2, 2.25, 2.5, 2.75, 3]  # nti = 2
        known_y = [0, 0, 0, 0, 1, 1, 1, 1, 0]
        self.assertTrue(self.same(known_t, calc[0]))
        self.assertTrue(self.same(known_y, calc[1]))

    def test_N20(self):
        knot_index = 2  # integer >= 0
        calc = bp.bspline_polynomial(self.kv, knot_index, self.degree, self.nti)
        known_t = [0, 0.5, 1, 1.5, 2, 2.25, 2.5, 2.75, 3]  # nti = 2
        known_y = [0, 0, 0, 0, 0, 0, 0, 0, 1]
        self.assertTrue(self.same(known_t, calc[0]))
        self.assertTrue(self.same(known_y, calc[1]))

    # def test_N30_insufficient_knots(self):
    #     knot_index = 3  # integer >= 0
    #     calc = bp.bspline_polynomial(self.kv, knot_index, self.degree, self.nti)
    #     self.assertIsInstance(calc, AssertionError)
    #     self.assertTrue(
    #         calc.args[0] == "Error, insufficient remaining knots for local support."
    #     )

    # def test_N01_not_yet_implemented(self):
    #     degree = 1  # integer >= 0
    #     calc = bp.bspline_polynomial(self.kv, self.ki, degree)
    #     self.assertIsInstance(calc, AssertionError)
    #     self.assertTrue(
    #         calc.args[0] == "Error: polynomial degree p exceeds maximum of 0"
    #     )


# retain main for debugging this file in VS code
if __name__ == "__main__":
    main()  # calls unittest.main()
