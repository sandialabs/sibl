import os
from unittest import TestCase

import numpy as np

# import xyfigure.client as client
import xyfigure.code.client as client


class MyTestCase(TestCase):
    """
    This is the unit test for differentiation of
    a quadratic function to produce a linear function.

    To run from command line:
    $ cd ~/sibl
    $ python -m unittest xyfigure/code/test/differentiation/test.py -v
    """

    @classmethod
    def setUpClass(cls):
        cls._path = os.path.join("xyfigure", "code", "test", "differentiation")
        cls._tol = 1e-6
        return super().setUpClass()

    def test_ddt1_quadratic(self):
        _jfile = os.path.join(self._path, "u-squared-ddt1.json")
        client.main([_jfile])

        _ofile = os.path.join(self._path, "u-squared-sig-proc-1.csv")

        _data = np.genfromtxt(_ofile, dtype="float", delimiter=",")
        _test = _data[:, 1]
        _ref = np.linspace(0, 10, 11)
        _diff = _test - _ref
        _diff_norm = np.linalg.norm(_diff)

        same_data = False
        same_data = np.abs(_diff_norm) < self._tol
        self.assertTrue(same_data)

    def test_ddt2_quadratic(self):
        _jfile = os.path.join(self._path, "u-squared-ddt2.json")
        client.main([_jfile])

        _ofile = os.path.join(self._path, "u-squared-sig-proc-2.csv")

        _data = np.genfromtxt(_ofile, dtype="float", delimiter=",")
        _test = _data[:, 1]
        _ref = np.ones(11)
        _diff = _test - _ref
        _diff_norm = np.linalg.norm(_diff)

        same_data = False
        same_data = np.abs(_diff_norm) < self._tol
        self.assertTrue(same_data)

    def test_ddt3_quadratic(self):
        _jfile = os.path.join(self._path, "u-squared-ddt3.json")
        client.main([_jfile])

        _ofile = os.path.join(self._path, "u-squared-sig-proc-3.csv")

        _data = np.genfromtxt(_ofile, dtype="float", delimiter=",")
        _test = _data[:, 1]
        _ref = np.zeros(11)
        _diff = _test - _ref
        _diff_norm = np.linalg.norm(_diff)

        same_data = False
        same_data = np.abs(_diff_norm) < self._tol
        self.assertTrue(same_data)

    def test_ddt1_sine(self):
        _jfile = os.path.join(self._path, "t-v-sines-ddt1.json")
        client.main([_jfile])

        _ofile = os.path.join(self._path, "t-v-sines-sig-proc-1.csv")

        _data = np.genfromtxt(_ofile, dtype="float", delimiter=",")
        _test = _data[:, 1]
        _t = np.linspace(0, 1, 101)
        _ref = 2 * np.pi * np.cos(2 * np.pi * _t)
        _diff = _test - _ref
        _diff_norm = np.linalg.norm(_diff)

        same_data = False
        # same_data = np.abs(_diff_norm) < self._tol
        # In manual testing, the L2norm was
        # diff_norm: 0.031201004731119160
        # because of how the np.gradient operator works on the edges of the
        # interval, so loosen the tolerance manually:
        _cosine_tolerance = 0.1
        # same_data = np.abs(_diff_norm) < 10000
        same_data = np.abs(_diff_norm) < _cosine_tolerance
        self.assertTrue(same_data)
