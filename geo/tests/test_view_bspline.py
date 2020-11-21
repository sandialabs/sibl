"""
This module is a unit test of the bezier_surface implementation.

To run
$ conda load siblenv
$ cd ~/sibl
$ black --check geo/tests/test_view_bspline.py
$ pytest geo/tests/test_view_bspline.py -v
$ pytest geo/tests/test_view_bspline.py -v --cov=geo/src/ptg --cov-report term-missing
"""
import os

from unittest import TestCase, main
import unittest

import ptg.view_bspline as vbsp


class Test(unittest.TestCase):
    """Tests the creation of B-Spline view entities."""

    @classmethod
    def setUpClass(cls):
        cls.data_path = os.path.join("geo", "data", "bspline")
        return super().setUpClass()

    @unittest.expectedFailure
    def test_000_json_file_does_not_exist(self):
        jfile = "no_such_file.json"  # file does not exist
        config_file = os.path.join(self.data_path, jfile)
        verbose = True

        item = vbsp.ViewBSplineFactory.create(config_file=config_file, verbose=verbose)
        self.assertIsInstance(item, vbsp.ViewBSplineBasis)
        a = 4

    def test_001_selftest_main_recover_bezier_linear(self):
        # config_file = "geo/data/bspline/recover_bezier_linear.json"
        jfile = "recover_bezier_linear.json"
        config_file = os.path.join(self.data_path, jfile)
        verbose = True

        item = vbsp.ViewBSplineFactory.create(config_file=config_file, verbose=verbose)
        self.assertIsInstance(item, vbsp.ViewBSplineBasis)
        a = 4

    def test_002_selftest_main_bspline_quadratic_expanded(self):
        # config_file = "geo/data/bspline/quadratic_expanded.json"
        jfile = "quadratic_expanded.json"
        config_file = os.path.join(self.data_path, jfile)
        verbose = True

        item = vbsp.ViewBSplineFactory.create(config_file=config_file, verbose=verbose)
        self.assertIsInstance(item, vbsp.ViewBSplineBasis)
        a = 4

    @unittest.expectedFailure
    def test_003_selftest_config_schema_incomplete(self):
        jfile = "test_config_schema_incomplete.json"
        config_file = os.path.join(self.data_path, jfile)
        item = vbsp.ViewBSplineFactory.create(config_file=config_file)
        a = 4


# retain main for debugging this file in VS code
if __name__ == "__main__":
    main()  # calls unittest.main()
