import os
import unittest

import numpy as np

# import xyfigure.client as client
# import xyfigure.code.client as client
import xyfigure.code.client as client


class MyTestCase(unittest.TestCase):
    """
    This is the unit test for differentiation of
    a quadratic function to produce a linear function.

    To run
    $ conda load siblenv
    $ cd ~/sibl
    $ pytest xyfigure/tests/differentiation/test_differentiation.py -v
    formerly
    $ python -m unittest xyfigure/tests/differentiation/test_differentiation.py -v
    """

    @classmethod
    def setUpClass(cls):
        cls.path = os.path.join("xyfigure", "tests", "differentiation")
        cls.tol = 1e-6
        return super().setUpClass()

    def test_ddt1_quadratic(self):
        jfile = os.path.join(self.path, "u-squared-ddt1.json")
        client.main([jfile])

        ofile = os.path.join(self.path, "u-squared-sig-proc-1.csv")

        data = np.genfromtxt(ofile, dtype="float", delimiter=",")
        test = data[:, 1]
        ref = np.linspace(0, 10, 11)
        diff = test - ref
        diff_norm = np.linalg.norm(diff)

        same_data = False
        same_data = np.abs(diff_norm) < self.tol
        self.assertTrue(same_data)

    def test_ddt2_quadratic(self):
        jfile = os.path.join(self.path, "u-squared-ddt2.json")
        client.main([jfile])

        ofile = os.path.join(self.path, "u-squared-sig-proc-2.csv")

        data = np.genfromtxt(ofile, dtype="float", delimiter=",")
        test = data[:, 1]
        ref = np.ones(11)
        diff = test - ref
        diff_norm = np.linalg.norm(diff)

        same_data = False
        same_data = np.abs(diff_norm) < self.tol
        self.assertTrue(same_data)

    def test_ddt3_quadratic(self):
        jfile = os.path.join(self.path, "u-squared-ddt3.json")
        client.main([jfile])

        ofile = os.path.join(self.path, "u-squared-sig-proc-3.csv")

        data = np.genfromtxt(ofile, dtype="float", delimiter=",")
        test = data[:, 1]
        ref = np.zeros(11)
        diff = test - ref
        diff_norm = np.linalg.norm(diff)

        same_data = False
        same_data = np.abs(diff_norm) < self.tol
        self.assertTrue(same_data)

    def test_ddt1_sine(self):
        jfile = os.path.join(self.path, "t-v-sines-ddt1.json")
        client.main([jfile])

        ofile = os.path.join(self.path, "t-v-sines-sig-proc-1.csv")

        data = np.genfromtxt(ofile, dtype="float", delimiter=",")
        test = data[:, 1]
        _t = np.linspace(0, 1, 101)
        ref = 2 * np.pi * np.cos(2 * np.pi * _t)
        diff = test - ref
        diff_norm = np.linalg.norm(diff)

        same_data = False
        # same_data = np.abs(diff_norm) < self.tol
        # In manual testing, the L2norm was
        # diff_norm: 0.031201004731119160
        # because of how the np.gradient operator works on the edges of the
        # interval, so loosen the tolerance manually:
        _cosine_tolerance = 0.1
        # same_data = np.abs(diff_norm) < 10000
        same_data = np.abs(diff_norm) < _cosine_tolerance
        self.assertTrue(same_data)
