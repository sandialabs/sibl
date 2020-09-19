# test_bspline_polynomial.py
"""
This module is a unit test of the bspline_polynomial implementation.

To run
$ conda load siblenv
$ cd ~/sibl

# default interaction
$ python -m unittest ptg/code/test_bspline_polynomial  

# verbose interaction
$ python -m unittest -v ptg/code/bspline_polynomial_test
"""
from unittest import TestCase, main

import numpy as np

import ptg.code.bspline_polynomial as bp


class TestBspline(TestCase):

    @classmethod
    def setUpClass(cls):
        cls._TOL = 1e-6  # tolerance
        cls._nti = 4  # number of time intervals
        # t, e.g., two intervals, three evaluation points
        cls._verbosity = True

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

    def test_000_p0(self):
        knot_vector = [0, 2, 3] # list
        degree = 0 # integer >= 0

        knot_index = 0 # integer >= 0
        calc = bp.bspline_polynomial(knot_vector, knot_index, degree, self._nti, self._verbosity)
        if self._verbosity:
            print(f"output = {calc}")
        
        known_t = [0, 0.5, 1, 1.5, 2, 2.25, 2.5, 2.75, 3]
        known_y = [1, 1, 1, 1, 0, 0, 0, 0, 0]

        self.assertTrue(self.same(known_t, calc[0]))
        self.assertTrue(self.same(known_y, calc[1]))

        knot_index = 1 # integer >= 0
        calc = bp.bspline_polynomial(knot_vector, knot_index, degree, self._nti, self._verbosity)
        if self._verbosity:
            print(f"output = {calc}")
        
        known_t = [0, 0.5, 1, 1.5, 2, 2.25, 2.5, 2.75, 3]
        known_y = [0, 0, 0, 0, 1, 1, 1, 1, 0]

        self.assertTrue(self.same(known_t, calc[0]))
        self.assertTrue(self.same(known_y, calc[1]))

        knot_index = 2 # integer >= 0
        calc = bp.bspline_polynomial(knot_vector, knot_index, degree, self._nti, self._verbosity)
        if self._verbosity:
            print(f"output = {calc}")
        
        known_t = [0, 0.5, 1, 1.5, 2, 2.25, 2.5, 2.75, 3]
        known_y = [0, 0, 0, 0, 0, 0, 0, 0, 1]

        self.assertTrue(self.same(known_t, calc[0]))
        self.assertTrue(self.same(known_y, calc[1]))