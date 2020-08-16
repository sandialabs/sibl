#!/usr/bin/env python3
# bernstein_polynomial_test.py
"""
This module is a unit test of the bernstein_polynomial implementation.

To run
$ python bernstein_polynomial_test.py              # terse interaction
$ python -m unittest bernstein_polynomial_test     # default interaction
$ python -m unittest -v bernstein_polynomial_test  # verbose interaction
"""
# standard library imports
# import sys
#
import numpy as np
from unittest import TestCase, main
#
import bernstein_polynomial as bp


class TestBernstein(TestCase):

    @classmethod
    def setUpClass(cls):
        cls._TOL = 1e-6  # tolerance
        cls._nti = 4  # number of time intervals
        # t, e.g., four intervals, five evaluation points
        cls._t = np.linspace(0, 1, cls._nti+1)
        cls._verbosity = 0

    @classmethod
    def same(cls, a, b):
        same_to_tolerance = False
        l2norm_diff = np.linalg.norm(a - b)

        if cls._verbosity > 0:
            print(f'array a = {a}')
            print(f'array b = {b}')
            print(f'l2norm_diff = {l2norm_diff}')

        if np.abs(l2norm_diff) < cls._TOL:
            same_to_tolerance = True

        return same_to_tolerance

    def test_000_b01(self):
        known = 1 - self._t
        i, p = 0, 1
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))

    def test_001_b11(self):
        known = self._t
        i, p = 1, 1
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))

    def test_003_b02(self):
        known = (1 - self._t)**2
        i, p = 0, 2
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))

    def test_004_b12(self):
        known = 2 * self._t * (1 - self._t)
        i, p = 1, 2
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))

    def test_005_b22(self):
        known = (self._t)**2
        i, p = 2, 2
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))

    def test_006_b03(self):
        known = (1 - self._t)**3
        i, p = 0, 3
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))

    def test_007_b13(self):
        known = 3 * self._t * (1 - self._t)**2
        i, p = 1, 3
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))

    def test_008_b23(self):
        known = 3 * (self._t)**2 * (1 - self._t)
        i, p = 2, 3
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))

    def test_009_b33(self):
        known = (self._t)**3
        i, p = 3, 3
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))

    def test_010_b04(self):
        known = (1 - self._t)**4
        i, p = 0, 4
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))

    def test_011_b14(self):
        known = 4 * self._t * (1 - self._t)**3
        i, p = 1, 4
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))

    def test_012_b24(self):
        known = 6 * (self._t)**2 * (1 - self._t)**2
        i, p = 2, 4
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))

    def test_013_b34(self):
        known = 4 * (self._t)**3 * (1 - self._t)
        i, p = 3, 4
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))

    def test_014_b44(self):
        known = (self._t)**4
        i, p = 4, 4
        calc = bp.bernstein_polynomial(i, p, self._nti)
        self.assertTrue(self.same(known, calc))


if __name__ == '__main__':
    main()  # calls unittest.main()
