"""
This module is a unit test of the bezier_surface implementation.

To run
$ conda load siblenv
$ cd ~/sibl
$ black --check geo/tests/test_bernstein_surface.py
$ pytest geo/tests/test_view_bernstein_surface.py -v
$ pytest geo/tests/test_view_bernstein_surface.py -v --cov=geo/src/ptg --cov-report term-missing
"""

from unittest import TestCase, main

import ptg.view_bernstein_surface as bsurf


class Test(TestCase):
    """Tests the creation of Bezier surface basis (Bernstein) functions figures."""

    def test_000_bilinear(self):
        config = {
            "degree": 1,
            "number-time-interval-bisections": 1,
            "display": False,
            "camera-azimuth": 15,
            "camera-elevation": 15,
            "dots-per-inch": 100,
            "latex": False,
            "serialize": False,
            "verbose": True,
            "z-axis-label-inverted": True,
        }
        # bs = bsurf.BezierSurface(config=config)
        bs = bsurf.ViewBernsteinSurface(config=config)
        result = bs.INITIALIZED
        self.assertTrue(result)

    def test_001_selftest_main(self):
        result = bsurf.main(None)
        self.assertTrue(result)


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
