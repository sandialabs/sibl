from unittest import TestCase, main

import ptg.code.bezier_indices as bezindex


class TestBezierIndices(TestCase):
    def test_000_1D_linear(self):
        p, dim = (1, 1)
        indices = bezindex.knot_indices(degree=p, dimension=dim)
        self.assertTupleEqual(indices, (0, 1))

    def test_001_2D_linear(self):
        p, dim = (1, 2)
        indices = bezindex.knot_indices(degree=p, dimension=dim)
        self.assertTupleEqual(indices, ((0, 0), (0, 1), (1, 0), (1, 1)))

    def test_002_3D_linear(self):
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

    def test_003_1D_quadratic(self):
        p, dim = (2, 1)
        indices = bezindex.knot_indices(degree=p, dimension=dim)
        self.assertTupleEqual(indices, (0, 1, 2))

    def test_004_2D_quadratic(self):
        p, dim = (2, 2)
        indices = bezindex.knot_indices(degree=p, dimension=dim)
        self.assertTupleEqual(
            indices,
            ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)),
        )

    def test_005_3D_quadratic(self):
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

    def test_006_1D_cubic(self):
        p, dim = (3, 1)
        indices = bezindex.knot_indices(degree=p, dimension=dim)
        self.assertTupleEqual(indices, (0, 1, 2, 3))

    def test_007_2D_cubic(self):
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

    def test_008_3D_cubic(self):
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


if __name__ == "__main__":
    main()  # calls unittest.main()
