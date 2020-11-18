"""
This module is a unit test of the bezier_surface implementation.

To run
$ conda load siblenv
$ cd ~/sibl
$ black --check geo/tests/test_bernstein_surface.py
$ pytest geo/tests/test_bernstein_surface.py -v
$ pytest geo/tests/test_bernstein_surface.py -v --cov=geo/src/ptg --cov-report term-missing
"""
# from unittest import TestCase, main
from unittest import TestCase

# from ptg.code.bezier_indices import bezindex
# import ptg.code.bezier_indices as bezindex
# import ptg.code.bezier_surface as bsurf
# import ptg.bezier_surface as bsurf
import ptg.view_bernstein_surface as bsurf


# class TestBezierSurface(TestCase):
class TestBernsteinSurface(TestCase):
    """Tests the creation of Bezier surface basis functions figures."""

    def test_000_bilinear(self):
        config = {
            "degree": 1,
            "number-time-interval-bisections": 1,
            "display": False,
            "camera-azimuth": 15,
            "camera-elevation": 15,
            "dots-per-inch": 100,
            "latex": True,
            "serialize": False,
            "verbose": True,
            "z-axis-label-inverted": True,
        }
        # bs = bsurf.BezierSurface(config=config)
        bs = bsurf.ViewBernsteinSurface(config=config)
        result = bs.INITIALIZED
        self.assertTrue(result)
