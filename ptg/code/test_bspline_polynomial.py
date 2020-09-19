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

    def test_000(self):
        knot_vector = [0, 1, 5]
        knot = 0
        degree = 0
        calc = bp.bspline_polynomial(knot, knot_vector, degree, self._nti, self._verbosity)
