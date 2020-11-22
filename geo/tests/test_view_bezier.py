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
    def test_000_json_file_does_not_exist(self):
        config_file = "no_such_file.json"  # file does not exist
        config_path = Path.joinpath(self.data_dir, config_file)
        item = vbz.ViewBezier(config=config_path, verbose=True)

    def test_001_Georgia_e(self):
        config_file = "Georgia-e-config.json"
        config_path = Path.joinpath(self.data_dir, config_file)
        item = vbz.ViewBezier(config=config_path, verbose=False)


# retain main for debugging this file in VS code
if __name__ == "__main__":
    main()  # calls unittest.main()
