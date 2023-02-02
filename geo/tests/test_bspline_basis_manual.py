# test_bspline_basis_manual.py
"""
This module is a unit test of the bspline_basis_manual implementation.

To run
$ conda load siblenv
$ cd ~/sibl
$ black --check geo/tests/test_bspline_basis_manual.py
$ pytest geo/tests/test_bspline_basis_manual.py -v
$ pytest geo/tests/test_bspline_basis_manual.py -v --cov=geo/src/ptg --cov-report term-missing
"""
from unittest import TestCase, main

import numpy as np
import pytest

import ptg.bspline_basis_manual as bp


class Test(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.TOL = 1e-6  # tolerance
        cls.nti = 4  # number of time intervals per knot
        # t, e.g., nti=1 gives two sub-intervals, three evaluation points
        cls.verbosity = False
        cls.kv = (0.0, 2.0, 3.0)  # knot_vector
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
        kv_too_short = (0.0,)
        calc = bp.bspline_basis_manual(kv_too_short)
        self.assertIsInstance(calc, AssertionError)
        self.assertTrue(
            calc.args[0] == "Error: knot vector length must be two or larger."
        )

    def test_002_knot_index_too_low(self):
        bad_knot_index = -1
        calc = bp.bspline_basis_manual(self.kv, bad_knot_index)
        self.assertIsInstance(calc, AssertionError)
        self.assertTrue(
            calc.args[0] == "Error: knot index knot_i must be non-negative."
        )

    def test_003_degree_too_small(self):
        degree = -1  # integer >= 0, so -1 is out of range for test
        calc = bp.bspline_basis_manual(self.kv, self.ki, degree)
        self.assertIsInstance(calc, AssertionError)
        self.assertTrue(
            calc.args[0] == "Error: polynomial degree p must be non-negative."
        )

    def test_004_degree_too_large(self):
        degree = 3  # integer >= 0, but cubic and higher not yet implemented
        calc = bp.bspline_basis_manual(self.kv, self.ki, degree)
        self.assertIsInstance(calc, AssertionError)
        self.assertTrue(
            calc.args[0] == "Error: polynomial degree p exceeds maximum of 2"
        )

    def test_005_number_of_time_intervals(self):
        bad_number_of_intervals = 0
        calc = bp.bspline_basis_manual(
            self.kv, self.ki, self.degree, bad_number_of_intervals
        )
        self.assertIsInstance(calc, AssertionError)
        self.assertTrue(
            calc.args[0] == "Error: number of time intervals nti must be 1 or greater."
        )

    def test_006_nti_out_of_range_and_verbose(self):
        bad_number_of_intervals = 0
        calc = bp.bspline_basis_manual(
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
        calc = bp.bspline_basis_manual(self.kv, bad_knot_index)
        self.assertIsInstance(calc, AssertionError)
        self.assertTrue(
            calc.args[0]
            == "Error: knot index knot_i exceeds knot vector length minus 1."
        )

    def test_007b_insufficient_knots_local_support(self):
        knot_vector = (0.0, 0.0, 1.0, 1.0)
        knot_i = 3  # the last knot
        degree = 2  # quadratic
        calc = bp.bspline_basis_manual(
            knot_vector_t=knot_vector, knot_i=knot_i, p=degree
        )
        self.assertIsInstance(calc, AssertionError)
        self.assertTrue(
            calc.args[0] == "Error: insufficient remaining knots for local support."
        )

    def test_008_decreasing_knots(self):
        # knot vector must be non-decreasing sequence, so test error
        # checking for a decreasing knot vector sequence
        bad_knot_vector = (0.0, 2.0, 1.0)
        with pytest.raises(ValueError) as error:
            _ = bp.bspline_basis_manual(bad_knot_vector)
        self.assertTrue(str(error.value) == "Error: knot vector is decreasing.")

    def test_N00_and_verbose(self):
        calc = bp.bspline_basis_manual(
            self.kv, self.ki, self.degree, self.nti, verbose=True
        )
        known_t = (0.0, 0.5, 1.0, 1.5, 2.0, 2.25, 2.5, 2.75, 3.0)  # nti = 2
        known_f_of_t = tuple(map(float, [1, 1, 1, 1, 0, 0, 0, 0, 0]))
        self.assertTrue(self.same(known_t, calc[0]))
        self.assertTrue(self.same(known_f_of_t, calc[1]))

    def test_N10(self):
        knot_index = 1  # integer >= 0
        calc = bp.bspline_basis_manual(self.kv, knot_index, self.degree, self.nti)
        known_t = (0.0, 0.5, 1.0, 1.5, 2.0, 2.25, 2.5, 2.75, 3.0)  # nti = 2
        known_f_of_t = tuple(map(float, [0, 0, 0, 0, 1, 1, 1, 1, 0]))
        self.assertTrue(self.same(known_t, calc[0]))
        self.assertTrue(self.same(known_f_of_t, calc[1]))

    def test_N20(self):
        knot_index = 2  # integer >= 0
        calc = bp.bspline_basis_manual(self.kv, knot_index, self.degree, self.nti)
        known_t = (0.0, 0.5, 1.0, 1.5, 2.0, 2.25, 2.5, 2.75, 3.0)  # nti = 2
        known_f_of_t = tuple(map(float, [0, 0, 0, 0, 0, 0, 0, 0, 1]))
        self.assertTrue(self.same(known_t, calc[0]))
        self.assertTrue(self.same(known_f_of_t, calc[1]))

    # def test_N30_insufficient_knots(self):
    #     knot_index = 3  # integer >= 0
    #     calc = bp.bspline_basis_manual(self.kv, knot_index, self.degree, self.nti)
    #     self.assertIsInstance(calc, AssertionError)
    #     self.assertTrue(
    #         calc.args[0] == "Error, insufficient remaining knots for local support."
    #     )

    def test_N01(self):
        knot_vector = tuple(map(float, [0, 1, 2]))
        degree = 1  # integer >= 0
        calc = bp.bspline_basis_manual(
            knot_vector, self.ki, degree, self.nti, verbose=True
        )
        known_t = (0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0)  # nti = 2
        known_f_of_t = (0.0, 0.25, 0.5, 0.75, 1.0, 0.75, 0.5, 0.25, 0.0)
        self.assertTrue(self.same(known_t, calc[0]))
        self.assertTrue(self.same(known_f_of_t, calc[1]))

    def test_N11(self):
        knot_vector = tuple(map(float, [0, 1, 2, 3]))
        knot_index = 1  # integer >= 0
        degree = 1  # integer >= 0
        calc = bp.bspline_basis_manual(
            knot_vector, knot_index, degree, self.nti, verbose=True
        )
        known_t = (
            0.0,
            0.25,
            0.5,
            0.75,
            1.0,
            1.25,
            1.5,
            1.75,
            2.0,
            2.25,
            2.5,
            2.75,
            3.0,
        )
        known_f_of_t = (
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.25,
            0.5,
            0.75,
            1.0,
            0.75,
            0.5,
            0.25,
            0.0,
        )
        self.assertTrue(self.same(known_t, calc[0]))
        self.assertTrue(self.same(known_f_of_t, calc[1]))

    def test_N02(self):
        knot_vector = tuple(map(float, [0, 1, 2, 3, 4]))
        degree = 2  # integer >= 0
        calc = bp.bspline_basis_manual(
            knot_vector, self.ki, degree, self.nti, verbose=True
        )
        # nti = 2
        known_t = (
            0.0,
            0.25,
            0.5,
            0.75,
            1.0,
            1.25,
            1.5,
            1.75,
            2.0,
            2.25,
            2.5,
            2.75,
            3.0,
            3.25,
            3.5,
            3.75,
            4.0,
        )
        known_f_of_t = (
            0.0,
            0.03125,
            0.125,
            0.28125,
            0.5,
            0.6875,
            0.75,
            0.6875,
            0.5,
            0.28125,
            0.125,
            0.03125,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        )
        self.assertTrue(self.same(known_t, calc[0]))
        self.assertTrue(self.same(known_f_of_t, calc[1]))

    def test_N12(self):
        knot_vector = tuple(map(float, [0, 1, 2, 3, 4]))
        knot_index = 1  # integer >= 0
        degree = 2  # integer >= 0
        calc = bp.bspline_basis_manual(
            knot_vector, knot_index, degree, self.nti, verbose=True
        )
        # nti = 2
        known_t = (
            0.0,
            0.25,
            0.5,
            0.75,
            1.0,
            1.25,
            1.5,
            1.75,
            2.0,
            2.25,
            2.5,
            2.75,
            3.0,
            3.25,
            3.5,
            3.75,
            4.0,
        )
        known_f_of_t = (
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.03125,
            0.125,
            0.28125,
            0.5,
            0.6875,
            0.75,
            0.6875,
            0.5,
            0.28125,
            0.125,
            0.03125,
            0.0,
        )
        self.assertTrue(self.same(known_t, calc[0]))
        self.assertTrue(self.same(known_f_of_t, calc[1]))

    def test_N03_not_yet_implemented(self):
        degree = 3  # integer >= 0
        calc = bp.bspline_basis_manual(self.kv, self.ki, degree)
        self.assertIsInstance(calc, AssertionError)
        self.assertTrue(
            calc.args[0] == "Error: polynomial degree p exceeds maximum of 2"
        )


# retain main for debugging this file in VS code
if __name__ == "__main__":
    main()  # calls unittest.main()


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
