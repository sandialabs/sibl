"""
This module is a unit test of the view_bspline implementation.

To run
$ conda load siblenv
$ cd ~/sibl
$ black --check geo/tests/test_view_bspline.py
$ pytest geo/tests/test_view_bspline.py -v
$ pytest geo/tests/test_view_bspline.py -v --cov=geo/src/ptg --cov-report term-missing
"""
# import runpy
# import sys
from pathlib import Path  # stop using os.path, use pathlib instead
from unittest import TestCase, main
import unittest

import ptg.view_bspline as vbsp


class Test(TestCase):
    """Tests the creation of B-Spline view entities."""

    @classmethod
    def setUpClass(cls):
        cls.self_file = Path(__file__)
        cls.self_dir = cls.self_file.resolve().parent
        cls.data_dir = cls.self_dir.joinpath("../", "data", "bspline").resolve()
        return super().setUpClass()

    @unittest.expectedFailure
    def test_000_json_file_does_not_exist(self):
        config_file = "no_such_file.json"  # file does not exist
        config_path = Path.joinpath(self.data_dir, config_file)
        item = vbsp.ViewBSplineFactory.create(config=config_path, verbose=True)
        self.assertIsInstance(item, vbsp.ViewBSplineBasis)

    def test_001_selftest_main_recover_bezier_linear(self):
        config_file = "recover_bezier_linear.json"
        config_path = Path.joinpath(self.data_dir, config_file)
        item = vbsp.ViewBSplineFactory.create(config=config_path, verbose=True)
        self.assertIsInstance(item, vbsp.ViewBSplineBasis)

    def test_002_selftest_main_bspline_quadratic_expanded(self):
        config_file = "quadratic_expanded.json"
        config_path = Path.joinpath(self.data_dir, config_file)
        item = vbsp.ViewBSplineFactory.create(config=config_path, verbose=True)
        self.assertIsInstance(item, vbsp.ViewBSplineBasis)

    @unittest.expectedFailure
    def test_003_selftest_config_schema_incomplete(self):
        config_file = "schema_incomplete.json"
        config_path = Path.joinpath(self.data_dir, config_file)
        item = vbsp.ViewBSplineFactory.create(config=config_path)

    @unittest.expectedFailure
    def test_004_selftest_config_class_type_not_exist(self):
        config_file = "class_request_not_exist.json"
        config_path = Path.joinpath(self.data_dir, config_file)
        item = vbsp.ViewBSplineFactory.create(config=config_path)

    def test_005_selftest_main_bspline_Piegl_Fig3p1(self):
        config_file = "Piegl_Fig3p1.json"
        config_path = Path.joinpath(self.data_dir, config_file)
        item = vbsp.ViewBSplineFactory.create(config=config_path)
        self.assertIsInstance(item, vbsp.ViewBSplineCurve)

    def test_006_selftest_main_bspline_Piegl_Fig9p1(self):
        config_file = "Piegl_Ex9p1.json"
        config_path = Path.joinpath(self.data_dir, config_file)
        item = vbsp.ViewBSplineFactory.create(config=config_path)
        self.assertIsInstance(item, vbsp.ViewBSplineCurveFit)

    def test_201_recover_bezier_bilinear(self):
        config_file = "recover_bezier_bilinear.json"
        config_path = Path.joinpath(self.data_dir, config_file)
        item = vbsp.ViewBSplineFactory.create(config=config_path)
        self.assertIsInstance(item, vbsp.ViewBSplineSurface)
        a = 4

    # Ask Anirudh
    # def test_006_selftest_main(self):
    #     config_file = "Piegl_Fig3p1.json"
    #     config_path = Path.joinpath(self.data_dir, config_file)
    #     source_file = self.self_dir.joinpath(
    #         "../", "src", "ptg", "view_bspline.py"
    #     ).resolve()

    #     argv_orig = sys.argv  # store previous state
    #     # sys.argv = [str(source_file), str(config_path)]  # temporary override
    #     # sys.argv = [str(source_file)]  # temporary override
    #     # sys.argv = vbsp
    #     # runpy = imp.load_source("__main__", str(source_file), a
    #     # result = runpy.run_module(str(source_file), run_name="__main__",)
    #     # result = runpy.run_module(str(source_file), run_name="__main__", alter_sys=True)
    #     result = runpy.run_module(str(source_file), run_name="main", alter_sys=True)
    #     # result = runpy.run_module(sys.argv, run_name="__main__", alter_sys=True)
    #     # result = runpy.run_module(sys.argv)
    #     # result = runpy.run_module(str(source_file))
    #     # result = runpy.run_module(vbsp, run_name="__main__", alter_sys=True)
    #     # result = vbsp.main(config_path)
    #     a = 4
    #     # result = bs_main = bsurf.main(None)
    #     sys.argv = argv_orig  # reinstate
    #     self.assertTrue(result)


# retain main for debugging this file in VS code
if __name__ == "__main__":
    main()  # calls unittest.main()
