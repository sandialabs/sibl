# test_bernstein_polynomial.py
"""
This module is a unit test of the bernstein_polynomial implementation.

To run
$ conda load siblenv
$ cd ~/sibl
$ black --check ptg/tests/test_bernstein_polynomial.py
$ pytest ptg/tests/test_bernstein_polynomial.py -v
$ pytest ptg/tests/test_bernstein_polynomial.py -v --cov=ptg/code --cov-report term-missing
"""
# from unittest import TestCase, main
from unittest import TestCase

import numpy as np

import ptg.code.bernstein_polynomial as bp


class TestBernstein(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._TOL = 1e-6  # tolerance
        cls._nti = 4  # number of time intervals
        # t, e.g., four intervals, five evaluation points
        cls._t = np.linspace(0, 1, cls._nti + 1)
        cls._verbosity = False

    @classmethod
    def same(cls, a, b):
        same_to_tolerance = False
        l2norm_diff = np.linalg.norm(a - b)

        if cls._verbosity:
            print(f"array a = {a}")
            print(f"array b = {b}")
            print(f"l2norm_diff = {l2norm_diff}")

        if np.abs(l2norm_diff) < cls._TOL:
            same_to_tolerance = True

        return same_to_tolerance

    def test_b00_input_out_of_range_and_verbose(self):
        i, p = 0, 0
        verbose = True
        calc = bp.bernstein_polynomial(i, p, self._nti, verbose=verbose)
        self.assertIsNone(calc)

    def test_b01(self):
        known = 1 - self._t
        i, p = 0, 1
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))

    def test_b11(self):
        known = self._t
        i, p = 1, 1
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))

    def test_b02(self):
        known = (1 - self._t) ** 2
        i, p = 0, 2
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))

    def test_b12(self):
        known = 2 * self._t * (1 - self._t)
        i, p = 1, 2
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))

    def test_b22(self):
        known = (self._t) ** 2
        i, p = 2, 2
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))

    def test_b03(self):
        known = (1 - self._t) ** 3
        i, p = 0, 3
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))

    def test_b13(self):
        known = 3 * self._t * (1 - self._t) ** 2
        i, p = 1, 3
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))

    def test_b23(self):
        known = 3 * (self._t) ** 2 * (1 - self._t)
        i, p = 2, 3
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))

    def test_b33(self):
        known = (self._t) ** 3
        i, p = 3, 3
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))

    def test_b04(self):
        known = (1 - self._t) ** 4
        i, p = 0, 4
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))

    def test_b14(self):
        known = 4 * self._t * (1 - self._t) ** 3
        i, p = 1, 4
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))

    def test_b24(self):
        known = 6 * (self._t) ** 2 * (1 - self._t) ** 2
        i, p = 2, 4
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))

    def test_b34(self):
        known = 4 * (self._t) ** 3 * (1 - self._t)
        i, p = 3, 4
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))

    def test_b44(self):
        known = (self._t) ** 4
        i, p = 4, 4
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))


# if __name__ == "__main__":
#     main()  # calls unittest.main()
