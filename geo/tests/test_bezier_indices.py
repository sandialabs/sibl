# test_bezier_indices.py
"""
This module is a unit test of the bezier_indices implementation.

To run
$ conda load siblenv
$ cd ~/sibl
$ black --check geo/tests/test_bezier_indices.py
$ pytest geo/tests/test_bezier_indices.py -v
$ pytest geo/tests/test_bezier_indices.py -v --cov=geo/src/ptg --cov-report term-missing
"""
# from unittest import TestCase, main
from unittest import TestCase

# from ptg.code.bezier_indices import bezindex
# import ptg.code.bezier_indices as bezindex
import ptg.bezier_indices as bezindex


class TestBezierIndices(TestCase):
    """Tests the canonical index order of knots in control nets
    for Bezier curves (1D), surfaces (2D), and volumes (3D),
    for the following polynomial degree, p, cases:
        p = 1 (linear, bilinear, trilinear)
        p = 2 (quadratic, biquadratic, triquadratic)
        p = 3 (cubic, bicubic, tricubic)

    To test from the command line:
    (siblenv) $ [~/sibl] python -m unittest ptg/code/test_bezier_indices.py -v
    """

    def test_000_input_out_of_range(self):
        p, dim = (4, 1)
        indices = bezindex.knot_indices(degree=p, dimension=dim)
        self.assertIsNone(indices)

    def test_001_linear_1D(self):
        p, dim = (1, 1)
        indices = bezindex.knot_indices(degree=p, dimension=dim)
        self.assertTupleEqual(indices, (0, 1))

    def test_002_linear_2D(self):
        p, dim = (1, 2)
        indices = bezindex.knot_indices(degree=p, dimension=dim)
        self.assertTupleEqual(indices, ((0, 0), (0, 1), (1, 0), (1, 1)))

    def test_003_linear_3D(self):
        p, dim = (1, 3)
        indices = bezindex.knot_indices(degree=p, dimension=dim)
        self.assertTupleEqual(
            indices,
            (
                (0, 0, 0),
                (0, 0, 1),
                (0, 1, 0),
                (0, 1, 1),
                (1, 0, 0),
                (1, 0, 1),
                (1, 1, 0),
                (1, 1, 1),
            ),
        )

    def test_004_quadratic_1D(self):
        p, dim = (2, 1)
        indices = bezindex.knot_indices(degree=p, dimension=dim)
        self.assertTupleEqual(indices, (0, 1, 2))

    def test_005_quadratic_2D(self):
        p, dim = (2, 2)
        indices = bezindex.knot_indices(degree=p, dimension=dim)
        self.assertTupleEqual(
            indices,
            ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)),
        )

    def test_006_quadratic_3D(self):
        p, dim = (2, 3)
        indices = bezindex.knot_indices(degree=p, dimension=dim)
        self.assertTupleEqual(
            indices,
            (
                (0, 0, 0),
                (0, 0, 1),
                (0, 0, 2),
                (0, 1, 0),
                (0, 1, 1),
                (0, 1, 2),
                (0, 2, 0),
                (0, 2, 1),
                (0, 2, 2),
                (1, 0, 0),
                (1, 0, 1),
                (1, 0, 2),
                (1, 1, 0),
                (1, 1, 1),
                (1, 1, 2),
                (1, 2, 0),
                (1, 2, 1),
                (1, 2, 2),
                (2, 0, 0),
                (2, 0, 1),
                (2, 0, 2),
                (2, 1, 0),
                (2, 1, 1),
                (2, 1, 2),
                (2, 2, 0),
                (2, 2, 1),
                (2, 2, 2),
            ),
        )

    def test_007_cubic_1D(self):
        p, dim = (3, 1)
        indices = bezindex.knot_indices(degree=p, dimension=dim)
        self.assertTupleEqual(indices, (0, 1, 2, 3))

    def test_008_cubic_2D(self):
        p, dim = (3, 2)
        indices = bezindex.knot_indices(degree=p, dimension=dim)
        self.assertTupleEqual(
            indices,
            (
                (0, 0),
                (0, 1),
                (0, 2),
                (0, 3),
                (1, 0),
                (1, 1),
                (1, 2),
                (1, 3),
                (2, 0),
                (2, 1),
                (2, 2),
                (2, 3),
                (3, 0),
                (3, 1),
                (3, 2),
                (3, 3),
            ),
        )

    def test_009_cubic_3D(self):
        p, dim = (3, 3)
        indices = bezindex.knot_indices(degree=p, dimension=dim)
        self.assertTupleEqual(
            indices,
            (
                (
                    (0, 0, 0),
                    (0, 0, 1),
                    (0, 0, 2),
                    (0, 0, 3),
                    (0, 1, 0),
                    (0, 1, 1),
                    (0, 1, 2),
                    (0, 1, 3),
                    (0, 2, 0),
                    (0, 2, 1),
                    (0, 2, 2),
                    (0, 2, 3),
                    (0, 3, 0),
                    (0, 3, 1),
                    (0, 3, 2),
                    (0, 3, 3),
                    (1, 0, 0),
                    (1, 0, 1),
                    (1, 0, 2),
                    (1, 0, 3),
                    (1, 1, 0),
                    (1, 1, 1),
                    (1, 1, 2),
                    (1, 1, 3),
                    (1, 2, 0),
                    (1, 2, 1),
                    (1, 2, 2),
                    (1, 2, 3),
                    (1, 3, 0),
                    (1, 3, 1),
                    (1, 3, 2),
                    (1, 3, 3),
                    (2, 0, 0),
                    (2, 0, 1),
                    (2, 0, 2),
                    (2, 0, 3),
                    (2, 1, 0),
                    (2, 1, 1),
                    (2, 1, 2),
                    (2, 1, 3),
                    (2, 2, 0),
                    (2, 2, 1),
                    (2, 2, 2),
                    (2, 2, 3),
                    (2, 3, 0),
                    (2, 3, 1),
                    (2, 3, 2),
                    (2, 3, 3),
                    (3, 0, 0),
                    (3, 0, 1),
                    (3, 0, 2),
                    (3, 0, 3),
                    (3, 1, 0),
                    (3, 1, 1),
                    (3, 1, 2),
                    (3, 1, 3),
                    (3, 2, 0),
                    (3, 2, 1),
                    (3, 2, 2),
                    (3, 2, 3),
                    (3, 3, 0),
                    (3, 3, 1),
                    (3, 3, 2),
                    (3, 3, 3),
                )
            ),
        )


# if __name__ == "__main__":
#     main()  # calls unittest.main()


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
