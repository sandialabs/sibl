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

import numpy as np

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
        config_path = str(Path.joinpath(self.data_dir, config_file))
        item = vbsp.ViewBSplineFactory.create(config=config_path, verbose=True)
        self.assertIsInstance(item, vbsp.ViewBSplineBasis)

    def test_001_selftest_main_recover_bezier_linear(self):
        config_file = "recover_bezier_linear.json"
        config_path = str(Path.joinpath(self.data_dir, config_file))
        item = vbsp.ViewBSplineFactory.create(config=config_path, verbose=True)
        self.assertIsInstance(item, vbsp.ViewBSplineBasis)

    def test_002_selftest_main_bspline_quadratic_expanded(self):
        config_file = "quadratic_expanded.json"
        config_path = str(Path.joinpath(self.data_dir, config_file))
        item = vbsp.ViewBSplineFactory.create(config=config_path, verbose=True)
        self.assertIsInstance(item, vbsp.ViewBSplineBasis)

    @unittest.expectedFailure
    def test_003_selftest_config_schema_incomplete(self):
        config_file = "schema_incomplete.json"
        config_path = str(Path.joinpath(self.data_dir, config_file))
        _ = vbsp.ViewBSplineFactory.create(config=config_path)

    @unittest.expectedFailure
    def test_004_selftest_config_class_type_not_exist(self):
        config_file = "class_request_not_exist.json"
        config_path = str(Path.joinpath(self.data_dir, config_file))
        _ = vbsp.ViewBSplineFactory.create(config=config_path)

    def test_005_selftest_main_bspline_Piegl_Fig3p1(self):
        config_file = "Piegl_Fig3p1.json"
        config_path = str(Path.joinpath(self.data_dir, config_file))
        item = vbsp.ViewBSplineFactory.create(config=config_path)
        self.assertIsInstance(item, vbsp.ViewBSplineCurve)

    def test_006_selftest_main_bspline_Piegl_Fig9p1(self):
        config_file = "Piegl_Ex9p1.json"
        config_path = str(Path.joinpath(self.data_dir, config_file))
        item = vbsp.ViewBSplineFactory.create(config=config_path)
        self.assertIsInstance(item, vbsp.ViewBSplineCurveFit)

    def test_201_recover_bezier_bilinear_B00_p1(self):
        config_file = "recover_bezier_bilinear_B00_p1.json"
        config_path = str(Path.joinpath(self.data_dir, config_file))
        item = vbsp.ViewBSplineFactory.create(config=config_path)
        self.assertIsInstance(item, vbsp.ViewBSplineSurface)

    def test_control_net_rows_columns(self):
        exemplar_control_points_net = [
            [[0.0, 0.0, 0.0], [0.0, 2.0, 1.0], [0.0, 4.0, 2.0]],
            [[5.1, 0.2, 0.3], [5.2, 2.2, 1.3], [5.3, 4.2, 2.3]],
        ]

        known_rows = np.array(
            [
                [[0.0, 0.0, 0.0], [0.0, 2.0, 1.0], [0.0, 4.0, 2.0]],
                [[5.1, 0.2, 0.3], [5.2, 2.2, 1.3], [5.3, 4.2, 2.3]],
            ]
        )

        known_cols = np.array(
            [
                [[0.0, 0.0, 0.0], [5.1, 0.2, 0.3]],
                [[0.0, 2.0, 1.0], [5.2, 2.2, 1.3]],
                [[0.0, 4.0, 2.0], [5.3, 4.2, 2.3]],
            ]
        )

        cn = vbsp.ControlNet(exemplar_control_points_net)

        TOL = 1e-6  # tolerance

        difference_rows = known_rows - cn.rows
        norm_rows = np.linalg.norm(difference_rows.flatten())
        self.assertTrue(norm_rows < TOL)

        difference_cols = known_cols - cn.columns
        norm_cols = np.linalg.norm(difference_cols.flatten())
        self.assertTrue(norm_cols < TOL)

    # Ask Anirudh
    # def test_006_selftest_main(self):
    #     config_file = "Piegl_Fig3p1.json"
    #     config_path = str(Path.joinpath(self.data_dir, config_file))
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
