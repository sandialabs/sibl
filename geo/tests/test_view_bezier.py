"""
This module is a unit test of the bezier_surface implementation.

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

import ptg.view_bezier as vbz


class Test(unittest.TestCase):
    """Tests the creation of Bezier view entities."""

    @classmethod
    def setUpClass(cls):
        cls.self_file = Path(__file__)
        cls.self_dir = cls.self_file.resolve().parent
        cls.data_dir = cls.self_dir.joinpath("../", "data", "bezier").resolve()
        return super().setUpClass()

    @unittest.expectedFailure
    def test_000_no_config_file(self):
        config_file = "test-no-such-file.json"  # file does not exist
        config_path = Path.joinpath(self.data_dir, config_file)
        item = vbz.ViewBezier(config=config_path, verbose=True)

    def test_001_Georgia_e(self):
        config_file = "Georgia-e-config.json"
        config_path = Path.joinpath(self.data_dir, config_file)
        item = vbz.ViewBezier(config=config_path, verbose=True)

    @unittest.expectedFailure
    def test_003_incomplete_config_schema(self):
        config_file = "test-schema-incomplete.json"
        config_path = Path.joinpath(self.data_dir, config_file)
        item = vbz.ViewBezier(config=config_path)

    @unittest.expectedFailure
    def test_004_unknown_bezier_type(self):
        config_file = "test-unknown-bezier-type.json"
        config_path = Path.joinpath(self.data_dir, config_file)
        item = vbz.ViewBezier(config=config_path)

    @unittest.expectedFailure
    def test_005_bad_num_time_divisions(self):
        config_file = "test-bad-num-time-divisions.json"
        config_path = Path.joinpath(self.data_dir, config_file)
        item = vbz.ViewBezier(config=config_path)

    @unittest.expectedFailure
    def test_006_bad_data_path(self):
        config_file = "test-bad-data-path.json"
        config_path = Path.joinpath(self.data_dir, config_file)
        item = vbz.ViewBezier(config=config_path)

    @unittest.expectedFailure
    def test_007_no_control_points_file(self):
        config_file = "test-bad-control-points-file.json"
        config_path = Path.joinpath(self.data_dir, config_file)
        item = vbz.ViewBezier(config=config_path)

    @unittest.expectedFailure
    def test_008_no_control_nets_file(self):
        config_file = "test-bad-control-nets-file.json"
        config_path = Path.joinpath(self.data_dir, config_file)
        item = vbz.ViewBezier(config=config_path)

    def test_009_bilinear(self):
        config_file = "bilinear-config.json"
        config_path = Path.joinpath(self.data_dir, config_file)
        item = vbz.ViewBezier(config=config_path)

    def test_010_trilinear(self):
        config_file = "trilinear-config.json"
        config_path = Path.joinpath(self.data_dir, config_file)
        item = vbz.ViewBezier(config=config_path)

    def test_011_gehry_bilbao(self):
        config_file = "gehry-bilbao-config.json"
        config_path = Path.joinpath(self.data_dir, config_file)
        item = vbz.ViewBezier(config=config_path)


# retain main for debugging this file in VS code
if __name__ == "__main__":
    main()  # calls unittest.main()
