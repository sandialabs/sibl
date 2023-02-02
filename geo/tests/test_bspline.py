"""This module is a unit test of the bspline implementation.

To run
$ conda activate siblenv
$ cd ~/sibl
$ pytest geo/tests/test_bspline.py -v
"""
from unittest import TestCase, main
import pytest
import numpy as np

import ptg.bspline as bsp


class TestBSpline(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tol = 1e-6  # tolerance
        # cls.nti = 4  # number of time intervals per knot
        # t, e.g., nti=1 gives two sub-intervals, three evaluation points
        cls.verbosity = False
        cls.kv = (0.0, 2.0, 3.0)  # tuple, default knot_vector
        cls.ki = 0  # non-negative integer, defaults to first index
        cls.degree = 0  # non-negative polynomial degree, defaults to 0 (constant)

    @classmethod
    def same(cls, a, b):
        same_to_tolerance = False
        l2norm_diff = np.linalg.norm(a - b)

        if cls.verbosity:
            print(f"array a = {a}")
            print(f"array b = {b}")
            print(f"l2norm_diff = {l2norm_diff}")

        if np.abs(l2norm_diff) < cls.tol:
            same_to_tolerance = True

        return same_to_tolerance

    def test_000_curve_initialization(self):
        knot_vector = (0.0, 1.0)
        coef = (1.0,)
        degree = 0
        C = bsp.Curve(knot_vector, coef, degree)
        self.assertIsInstance(C, bsp.Curve)

    def test_001_curve_knot_vector_too_short(self):
        knot_vector = (0.0,)  # too short
        coef = (1.0,)
        degree = 0
        C = bsp.Curve(knot_vector, coef, degree)
        result = C.is_valid()
        self.assertIsInstance(result, AssertionError)
        self.assertTrue(result.args[0] == "Error: knot vector mininum length is two.")

    def test_002_curve_degree_too_small_and_verbose(self):
        knot_vector = (0.0, 1.0)
        coef = (1.0,)
        degree = -1  # integer >= 0, so -1 is out of range for test
        verbosity = True  # to test the verbose code lines
        C = bsp.Curve(knot_vector, coef, degree, verbosity)
        result = C.is_valid()
        self.assertIsInstance(result, AssertionError)
        self.assertTrue(result.args[0] == "Error: degree must be non-negative.")

    def test_003_curve_basis_recover_bezier_linear(self):
        knot_vector = (0.0, 0.0, 1.0, 1.0)
        degree = 1  # linear

        coef_N0_p1 = (1.0, 0.0)
        N0_p1 = bsp.Curve(knot_vector, coef_N0_p1, degree)
        result = N0_p1.is_valid()
        self.assertTrue(result)
        tmin, tmax, npts = 0.0, 1.0, 5
        t = np.linspace(tmin, tmax, npts, endpoint=True)
        y = N0_p1.evaluate(t)
        y_known = (1.0, 0.75, 0.5, 0.25, 0.0)
        self.assertTrue(self.same(y_known, y))

        coef_N1_p1 = (0.0, 1.0)
        N1_p1 = bsp.Curve(knot_vector, coef_N1_p1, degree)
        result = N1_p1.is_valid()
        self.assertTrue(result)
        # tmin, tmax, npts = 0.0, 1.0, 5
        t = np.linspace(tmin, tmax, npts, endpoint=True)
        y = N1_p1.evaluate(t)
        y_known = (0.0, 0.25, 0.5, 0.75, 1.0)
        self.assertTrue(self.same(y_known, y))

    def test_004_curve_basis_degree_zero_seven_knots(self):
        knot_vector = (0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0)
        degree = 0  # constant
        coef = (0.0, 1.0, 0.0, 0.0, 0.0, 0.0)
        N1_p0 = bsp.Curve(knot_vector, coef, degree)
        result = N1_p0.is_valid()
        self.assertTrue(result)
        tmin, tmax, npts = knot_vector[0], knot_vector[-1], 13
        t = np.linspace(tmin, tmax, npts, endpoint=True)
        y = N1_p0.evaluate(t)
        y_known = (0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        self.assertTrue(self.same(y_known, y))

    def test_100_curve_basis_quadratic_eight_knots(self):
        """Known example from NURBS Book, Piegl and Tiller, Ex2.2, Fig 2.6 page 55."""
        KV = tuple(map(float, [0, 0, 0, 1, 2, 3, 4, 4, 5, 5, 5]))  # knot vector
        DEGREE = 2  # quadratic
        NBI = 3  # number of bisection intervals per knot span
        NCP = 8  # number of control points

        knots_lhs = KV[0:-1]  # left-hand-side knot values
        knots_rhs = KV[1:]  # right-hand-side knot values
        knot_spans = np.array(knots_rhs) - np.array(knots_lhs)
        dt = knot_spans / (2**NBI)
        assert all([dti >= 0 for dti in dt]), "Error: knot vector is decreasing."

        num_knots = len(KV)
        t = [
            knots_lhs[k] + j * dt[k]
            for k in np.arange(num_knots - 1)
            for j in np.arange(2**NBI)
        ]
        t.append(KV[-1])
        t = np.array(t)

        N_calc = []  # basis functions calculated by bsp.Curve

        for i in np.arange(NCP):

            coef = np.zeros(NCP)
            coef[i] = 1.0

            C = bsp.Curve(KV, coef, DEGREE)

            if C.is_valid():
                y = C.evaluate(t)
                N_calc.append(y)

        N_known = np.zeros((NCP, t.size), dtype=t.dtype)

        # Citation to give credit for Pythonic test implementation on knot intervals:
        # Roberto Agromayor (RoberAgro) Ph.D. candidate in turbomachinery design and
        # optimization at the Norwegian University of Science and Technology (NTNU)
        # https://github.com/RoberAgro/nurbspy/blob/master/tests/test_nurbs_basis_functions.py

        for j, t in enumerate(t):
            N0_p2 = (1 - t) ** 2 * (0 <= t < 1)
            N1_p2 = (2 * t - 3 / 2 * t**2) * (0 <= t < 1) + (1 / 2 * (2 - t) ** 2) * (
                1 <= t < 2
            )
            N2_p2 = (
                (1 / 2 * t**2) * (0 <= t < 1)
                + (-3 / 2 + 3 * t - t**2) * (1 <= t < 2)
                + (1 / 2 * (3 - t) ** 2) * (2 <= t < 3)
            )
            N3_p2 = (
                (1 / 2 * (t - 1) ** 2) * (1 <= t < 2)
                + (-11 / 2 + 5 * t - t**2) * (2 <= t < 3)
                + (1 / 2 * (4 - t) ** 2) * (3 <= t < 4)
            )
            N4_p2 = (1 / 2 * (t - 2) ** 2) * (2 <= t < 3) + (
                -16 + 10 * t - 3 / 2 * t**2
            ) * (3 <= t < 4)
            N5_p2 = (t - 3) ** 2 * (3 <= t < 4) + (5 - t) ** 2 * (4 <= t < 5)
            N6_p2 = (2 * (t - 4) * (5 - t)) * (4 <= t < 5)
            N7_p2 = (t - 4) ** 2 * (4 <= t <= 5)
            N_known[:, j] = np.asarray(
                [N0_p2, N1_p2, N2_p2, N3_p2, N4_p2, N5_p2, N6_p2, N7_p2]
            )

    def test_101_Bingol_2D_curve(self):
        """See
        https://nurbs-python.readthedocs.io/en/latest/visualization.html#curves
        """

        # knot vector
        KV = (0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0, 1.0, 1.0, 1.0)
        DEGREE = 4  # quadratic
        NBI = 1  # number of bisection intervals per knot span
        # NCP = 9  # number of control points

        knots_lhs = KV[0:-1]  # left-hand-side knot values
        knots_rhs = KV[1:]  # right-hand-side knot values
        knot_spans = np.array(knots_rhs) - np.array(knots_lhs)
        dt = knot_spans / (2**NBI)
        assert all([dti >= 0 for dti in dt]), "Error: knot vector is decreasing."

        num_knots = len(KV)
        t = [
            knots_lhs[k] + j * dt[k]
            for k in np.arange(num_knots - 1)
            for j in np.arange(2**NBI)
        ]
        t.append(KV[-1])
        t = np.array(t)

        COEF = (
            (5.0, 10.0),
            (15.0, 25.0),
            (30.0, 30.0),
            (45.0, 5.0),
            (55.0, 5.0),
            (70.0, 40.0),
            (60.0, 60.0),
            (35.0, 60.0),
            (20.0, 40.0),
        )
        NSD = len(COEF[0])  # number of space dimensions

        C = bsp.Curve(KV, COEF, DEGREE)
        result = C.is_valid()
        self.assertTrue(result)
        y = C.evaluate(t)
        # retain only non-repeated points at begnning and end
        # (which drops redundant points and beginning and end)
        y = y[2**NBI * DEGREE : -(2**NBI * DEGREE)]

        P_known = (
            (5.0, 10.0),
            (21.809895833333336, 24.60503472222222),
            (33.95833333333333, 20.347222222222218),
            (42.94270833333333, 11.692708333333336),
            (49.79166666666665, 7.84722222222222),
            (55.9157986111111, 12.174479166666664),
            (61.527777777777786, 23.61111111111111),
            (64.11458333333333, 38.29427083333332),
            (59.8611111111111, 51.31944444444444),
            (45.4079861111111, 57.37413194444444),
            (20.0, 40.0),
        )  # from geomdl at curve.delta = 1./11., thus 11 evaluation points
        # The 11 evaluation points bisects the five elements plus the endpoint
        # will correspond to NBI=1 (number of bisection intervals) used here.

        for i in np.arange(NSD):
            P_known_e = [e[i] for e in P_known]  # e is evaluation point
            self.assertTrue(self.same(P_known_e, y[:, i]))

    def test_200_evaluation_times_knot_vector_too_short(self):
        kv = (0.0,)  # knot vector too short
        deg = 0  # constant
        n_bis = 2
        with pytest.raises(ValueError) as error:
            _ = bsp.evaluation_times(knot_vector=kv, degree=deg, n_bisections=n_bis)
        self.assertTrue(
            str(error.value) == "Error: knot vector length must be two or greater."
        )

    def test_200_evaluation_times_bad_degree(self):
        kv = (0.0, 2.0, 3.0)  # knot vector
        deg = -1  # bad value
        n_bis = 2
        with pytest.raises(ValueError) as error:
            _ = bsp.evaluation_times(knot_vector=kv, degree=deg, n_bisections=n_bis)
        self.assertTrue(
            str(error.value)
            == "Error: polynomial degree must be a non-negative integer."
        )

    def test_200_evaluation_times_bad_number_of_bisections(self):
        kv = (0.0, 2.0, 3.0)  # knot vector
        deg = 0  # constant
        n_bis = 0  # bad value
        with pytest.raises(ValueError) as error:
            _ = bsp.evaluation_times(knot_vector=kv, degree=deg, n_bisections=n_bis)
        self.assertTrue(
            str(error.value)
            == "Error: number of time interval bisections must be an integer >= 1."
        )

    def test_200_evaluation_times_decreasing_knot_vector(self):
        kv = (0.0, 3.0, 2.0)  # bad knot vector
        deg = 0  # constant
        n_bis = 2
        with pytest.raises(ValueError) as error:
            _ = bsp.evaluation_times(knot_vector=kv, degree=deg, n_bisections=n_bis)
        self.assertTrue(str(error.value) == "Error: knot vector is decreasing.")

    def test_200_evaluation_times_non_uniform_knot_vector(self):
        kv = (0.0, 0.0, 2.0, 3.0, 3.0)
        deg = 1  # constant
        n_bis = 2
        calc_t = bsp.evaluation_times(knot_vector=kv, degree=deg, n_bisections=n_bis)
        known_t = (0.0, 0.5, 1.0, 1.5, 2.0, 2.25, 2.5, 2.75, 3.0)  # nti = 2
        self.assertTrue(self.same(calc_t, known_t))

    def test_201_recover_bezier_bilinear_B00_p1_surface(self):
        kv_t = (0.0, 0.0, 1.0, 1.0)  # knot vector for t parameter
        kv_u = (0.0, 0.0, 1.0, 1.0)  # knot vector for u parameter
        # control_points = [
        #     [[-15.0, -10.0, 1.0], [-15.0, 10.0, 1.0]],
        #     [[15.0, -10.0, 1.0], [15.0, 10.0, 1.0]],
        # ]
        control_points = (
            ((0.0, 0.0, 1.0), (0.0, 1.0, 0.0)),
            ((1.0, 0.0, 0.0), (1.0, 1.0, 0.0)),
        )
        degree_t = 1  # linear
        degree_u = 1  # linear
        nbi = 1  # number of bisections per knot interval

        S = bsp.Surface(
            kv_t,
            kv_u,
            control_points,
            degree_t,
            degree_u,
            n_bisections=nbi,
            verbose=True,
        )

        (
            calc_surface_evaluations_x,
            calc_surface_evaluations_y,
            calc_surface_evaluations_z,
        ) = S.evaluations

        known_surface_evaluations_x = np.array(
            ((0.0, 0.0, 0.0), (0.5, 0.5, 0.5), (1.0, 1.0, 1.0))
        )

        known_surface_evaluations_y = np.array(
            ((0.0, 0.5, 1.0), (0.0, 0.5, 1.0), (0.0, 0.5, 1.0))
        )

        known_surface_evaluations_z = np.array(
            ((1.0, 0.5, 0.0), (0.5, 0.25, 0.0), (0.0, 0.0, 0.0))
        )

        difference_matrix_x = calc_surface_evaluations_x - known_surface_evaluations_x
        difference_matrix_y = calc_surface_evaluations_y - known_surface_evaluations_y
        difference_matrix_z = calc_surface_evaluations_z - known_surface_evaluations_z

        Frobenius_norm_x = np.linalg.norm(difference_matrix_x, ord="fro")
        Frobenius_norm_y = np.linalg.norm(difference_matrix_y, ord="fro")
        Frobenius_norm_z = np.linalg.norm(difference_matrix_z, ord="fro")

        self.assertTrue(Frobenius_norm_x < self.tol)
        self.assertTrue(Frobenius_norm_y < self.tol)
        self.assertTrue(Frobenius_norm_z < self.tol)

        known_evaluation_times_t = (0.0, 0.5, 1.0)
        known_evaluation_times_u = (0.0, 0.5, 1.0)

        calc_evaluation_times_t = S.evaluation_times_t
        calc_evaluation_times_u = S.evaluation_times_u

        self.assertTrue(self.same(known_evaluation_times_t, calc_evaluation_times_t))
        self.assertTrue(self.same(known_evaluation_times_u, calc_evaluation_times_u))

    def test_202_Bingol_3D_surface(self):
        """Tests creation and plotting of BSpline surface, compared to
        GitHub repository orbingol
        https://github.com/orbingol/NURBS-Python/blob/5.x/geomdl/BSpline.py

        Example usage:

        $ conda activate nurbspyenv
        $ cd nurbspy/
        $ python
        > from geomdl import BSpline
        > from geomdl.visualization import VisMPL as vis
        >
        > surf = BSpline.Surface()
        > surf.degree_u = 3
        > surf.degree_v = 2
        > control_points = [
            [0, 0, 0], [0, 4, 0], [0, 8, -3],
            [2, 0, 6], [2, 4, 0], [2, 8, 0],
            [4, 0, 0], [4, 4, 0], [4, 8, 3],
            [6, 0, 0], [6, 4, -3], [6, 8, 0]
        ]
        > surf.set_ctrlpts(control_points, 4, 3)
        > surf.knotvector_u = [0, 0, 0, 0, 1, 1, 1, 1]
        > surf.knotvector_v = [0, 0, 0, 1, 1, 1]
        > surf.delta = 0.20  # 0.20 for testing, was originally 0.05 for smoothness
        > surf.vis = vis.VisSurface()
        # or alternatively, for a transparent surface, set the alpha to non-unity
        > surf.vis = vis.VisSurface(vis.VisConfig(alpha=0.8))
        >
        > surface_points = surf.evalpts
        > surf.render()
        # 0.20, with 1.0 / 0.20 = 5.0,
        # gives a matrix of [5x5] evalution (x, y, z) points found by
        > surf.evalpts
        """
        kv_t = tuple(map(float, [0, 0, 0, 0, 1, 1, 1, 1]))  # cubic
        kv_u = tuple(map(float, [0, 0, 0, 1, 1, 1]))  # quadratic
        control_points = (
            ((0, 0, 0), (0, 4, 0), (0, 8, -3)),
            ((2, 0, 6), (2, 4, 0), (2, 8, 0)),
            ((4, 0, 0), (4, 4, 0), (4, 8, 3)),
            ((6, 0, 0), (6, 4, -3), (6, 8, 0)),
        )
        degree_t = 3  # cubic
        degree_u = 2  # quadratic
        nbi = 2  # number of bisections per knot interval

        S = bsp.Surface(
            kv_t,
            kv_u,
            control_points,
            degree_t,
            degree_u,
            n_bisections=nbi,
            verbose=True,
        )

        (
            calc_surface_evaluations_x,
            calc_surface_evaluations_y,
            calc_surface_evaluations_z,
        ) = S.evaluations

        known_surface_evaluation_points = np.array(
            [
                [
                    [0.0, 0.0, 0.0],
                    [0.0, 2.0, -0.1875],
                    [0.0, 4.0, -0.75],
                    [0.0, 6.0, -1.6875],
                    [0.0, 8.0, -3.0],
                ],
                [
                    [1.5, 0.0, 2.53125],
                    [1.5, 2.0, 1.353515625],
                    [1.5, 4.0, 0.3984375],
                    [1.5, 6.0, -0.333984375],
                    [1.5, 8.0, -0.84375],
                ],
                [
                    [3.0, 0.0, 2.25],
                    [3.0, 2.0, 1.171875],
                    [3.0, 4.0, 0.5625],
                    [3.0, 6.0, 0.421875],
                    [3.0, 8.0, 0.75],
                ],
                [
                    [4.5, 0.0, 0.84375],
                    [4.5, 2.0, 0.076171875],
                    [4.5, 4.0, -0.1171875],
                    [4.5, 6.0, 0.263671875],
                    [4.5, 8.0, 1.21875],
                ],
                [
                    [6.0, 0.0, 0.0],
                    [6.0, 2.0, -1.125],
                    [6.0, 4.0, -1.5],
                    [6.0, 6.0, -1.125],
                    [6.0, 8.0, 0.0],
                ],
            ]
        )

        ix, iy, iz = 0, 1, 2  # index for x, y, z

        known_surface_evaluation_points_x = known_surface_evaluation_points[
            :, :, ix
        ].flatten()

        known_surface_evaluation_points_y = known_surface_evaluation_points[
            :, :, iy
        ].flatten()

        known_surface_evaluation_points_z = known_surface_evaluation_points[
            :, :, iz
        ].flatten()

        self.assertTrue(
            self.same(
                known_surface_evaluation_points_x, calc_surface_evaluations_x.flatten()
            )
        )
        self.assertTrue(
            self.same(
                known_surface_evaluation_points_y, calc_surface_evaluations_y.flatten()
            )
        )
        self.assertTrue(
            self.same(
                known_surface_evaluation_points_z, calc_surface_evaluations_z.flatten()
            )
        )

    def test_203_Bingol_3D_surface(self):
        """Tests creation and plotting of BSpline surface, compared to
        GitHub repository orbingol
        https://nurbs-python.readthedocs.io/en/5.x/visualization-3.py

        Example usage:

        $ conda activate nurbspyenv
        $ cd nurbspy/
        $ python
        > from geomdl import BSpline
        > from geomdl.visualization import VisMPL as vis
        >
        > surf = BSpline.Surface()
        >
        > surf.degree_u = 3
        > surf.degree_v = 3
        >
        > control_points = [
            [
                [-25.0, -25.0, -10.0],
                [-25.0, -15.0, -5.0],
                [-25.0, -5.0, 0.0],
                [-25.0, 5.0, 0.0],
                [-25.0, 15.0, -5.0],
                [-25.0, 25.0, -10.0]
            ],
            [
                [-15.0, -25.0, -8.0],
                [-15.0, -15.0, -4.0],
                [-15.0, -5.0, -4.0],
                [-15.0, 5.0, -4.0],
                [-15.0, 15.0, -4.0],
                [-15.0, 25.0, -8.0]
            ],
            [
                [-5.0, -25.0, -5.0],
                [-5.0, -15.0, -3.0],
                [-5.0, -5.0, -8.0],
                [-5.0, 5.0, -8.0],
                [-5.0, 15.0, -3.0],
                [-5.0, 25.0, -5.0]
            ],
            [
                [5.0, -25.0, -3.0],
                [5.0, -15.0, -2.0],
                [5.0, -5.0, -8.0],
                [5.0, 5.0, -8.0],
                [5.0, 15.0, -2.0],
                [5.0, 25.0, -3.0]
            ],
            [
                [15.0, -25.0, -8.0],
                [15.0, -15.0, -4.0],
                [15.0, -5.0, -4.0],
                [15.0, 5.0, -4.0],
                [15.0, 15.0, -4.0],
                [15.0, 25.0, -8.0]
            ],
            [
                [25.0, -25.0, -10.0],
                [25.0, -15.0, -5.0],
                [25.0, -5.0, 2.0],
                [25.0, 5.0, 2.0],
                [25.0, 15.0, -5.0],
                [25.0, 25.0, -10.0]
            ]
        ]
        > surf.ctrlpts2d = control_points
        > surf.knotvector_u = [0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0]
        > surf.knotvector_v = [0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0]
        > surf.delta = 1.0/7.0  # seven intervals for testing, originally 0.025 for smoothness
        > surf.evaluate()

        > surf.vis = vis.VisSurface(vis.VisConfig(alpha=0.8))
        >
        > surface_points = surf.evalpts
        > surf.render()
        # delta of 1.0 / 7.0
        # gives a matrix of [7x7] evalution (x, y, z) points found by
        > surf.evalpts
        > len(surf.evalpts)  # is 49, a 7x7 grid
        """
        kv_t = tuple(map(float, [0, 0, 0, 0, 1, 2, 3, 3, 3, 3]))  # cubic
        kv_u = tuple(map(float, [0, 0, 0, 0, 1, 2, 3, 3, 3, 3]))  # cubic
        control_points = (
            (
                (-25.0, -25.0, -10.0),
                (-25.0, -15.0, -5.0),
                (-25.0, -5.0, 0.0),
                (-25.0, 5.0, 0.0),
                (-25.0, 15.0, -5.0),
                (-25.0, 25.0, -10.0),
            ),
            (
                (-15.0, -25.0, -8.0),
                (-15.0, -15.0, -4.0),
                (-15.0, -5.0, -4.0),
                (-15.0, 5.0, -4.0),
                (-15.0, 15.0, -4.0),
                (-15.0, 25.0, -8.0),
            ),
            (
                (-5.0, -25.0, -5.0),
                (-5.0, -15.0, -3.0),
                (-5.0, -5.0, -8.0),
                (-5.0, 5.0, -8.0),
                (-5.0, 15.0, -3.0),
                (-5.0, 25.0, -5.0),
            ),
            (
                (5.0, -25.0, -3.0),
                (5.0, -15.0, -2.0),
                (5.0, -5.0, -8.0),
                (5.0, 5.0, -8.0),
                (5.0, 15.0, -2.0),
                (5.0, 25.0, -3.0),
            ),
            (
                (15.0, -25.0, -8.0),
                (15.0, -15.0, -4.0),
                (15.0, -5.0, -4.0),
                (15.0, 5.0, -4.0),
                (15.0, 15.0, -4.0),
                (15.0, 25.0, -8.0),
            ),
            (
                (25.0, -25.0, -10.0),
                (25.0, -15.0, -5.0),
                (25.0, -5.0, 2.0),
                (25.0, 5.0, 2.0),
                (25.0, 15.0, -5.0),
                (25.0, 25.0, -10.0),
            ),
        )
        degree_t = 3  # cubic
        degree_u = 3  # cubic
        nbi = 1  # number of bisections per knot interval

        S = bsp.Surface(
            kv_t,
            kv_u,
            control_points,
            degree_t,
            degree_u,
            n_bisections=nbi,
            verbose=True,
        )

        (
            calc_surface_evaluations_x,
            calc_surface_evaluations_y,
            calc_surface_evaluations_z,
        ) = S.evaluations

        known_surface_evaluation_points = np.array(
            [
                [-25.0, -25.0, -10.0],
                [-25.0, -13.229166666666668, -4.21875],
                [-25.0, -5.833333333333334, -1.25],
                [-24.999999999999993, 4.440892098500626e-16, -0.3124999999999999],
                [-25.0, 5.833333333333331, -1.2499999999999996],
                [-25.0, 13.22916666666667, -4.218750000000002],
                [-25.0, 25.0, -10.0],
                [-13.229166666666668, -25.0, -7.364583333333334],
                [-13.229166666666668, -13.229166666666668, -4.4912109375],
                [-13.229166666666668, -5.833333333333334, -4.424479166666667],
                [-13.229166666666664, 4.440892098500626e-16, -4.574869791666666],
                [-13.229166666666666, 5.833333333333331, -4.424479166666667],
                [-13.229166666666668, 13.22916666666667, -4.491210937500001],
                [-13.229166666666668, 25.0, -7.364583333333334],
                [-5.833333333333334, -25.0, -5.416666666666667],
                [-5.833333333333334, -13.229166666666668, -4.476562500000001],
                [-5.833333333333334, -5.833333333333334, -6.020833333333333],
                [-5.833333333333333, 4.440892098500626e-16, -6.755208333333332],
                [-5.833333333333333, 5.833333333333332, -6.020833333333333],
                [-5.833333333333334, 13.229166666666671, -4.4765625],
                [-5.833333333333334, 25.0, -5.416666666666667],
                [4.440892098500626e-16, -24.999999999999993, -4.249999999999999],
                [4.440892098500626e-16, -13.229166666666666, -4.2509765625],
                [4.440892098500626e-16, -5.833333333333333, -6.460937499999998],
                [3.3306690738754696e-16, 4.440892098500625e-16, -7.4277343749999964],
                [3.3306690738754696e-16, 5.83333333333333, -6.460937499999998],
                [4.440892098500626e-16, 13.229166666666668, -4.250976562499999],
                [4.440892098500626e-16, 24.999999999999993, -4.249999999999999],
                [5.833333333333331, -25.0, -4.583333333333332],
                [5.833333333333332, -13.229166666666666, -4.125],
                [5.833333333333331, -5.833333333333333, -5.916666666666666],
                [5.83333333333333, 4.4408920985006257e-16, -6.729166666666664],
                [5.83333333333333, 5.83333333333333, -5.916666666666666],
                [5.833333333333331, 13.229166666666668, -4.124999999999999],
                [5.833333333333331, 25.0, -4.583333333333332],
                [13.22916666666667, -25.0, -6.885416666666668],
                [13.22916666666667, -13.229166666666668, -4.21875],
                [13.22916666666667, -5.833333333333334, -4.177083333333332],
                [13.229166666666668, 4.440892098500626e-16, -4.325520833333332],
                [13.229166666666668, 5.833333333333331, -4.177083333333332],
                [13.22916666666667, 13.22916666666667, -4.218750000000001],
                [13.22916666666667, 25.0, -6.885416666666668],
                [25.0, -25.0, -10.0],
                [25.0, -13.229166666666668, -3.65625],
                [25.0, -5.833333333333334, 0.25000000000000006],
                [24.999999999999993, 4.440892098500626e-16, 1.5624999999999998],
                [25.0, 5.833333333333331, 0.25000000000000044],
                [25.0, 13.22916666666667, -3.6562500000000013],
                [25.0, 25.0, -10.0],
            ]
        )

        ix, iy, iz = 0, 1, 2  # index for x, y, z

        self.assertTrue(
            self.same(
                known_surface_evaluation_points[:, ix],
                calc_surface_evaluations_x.flatten(),
            )
        )

        self.assertTrue(
            self.same(
                known_surface_evaluation_points[:, iy],
                calc_surface_evaluations_y.flatten(),
            )
        )

        self.assertTrue(
            self.same(
                known_surface_evaluation_points[:, iz],
                calc_surface_evaluations_z.flatten(),
            )
        )

    def test_300_control_lattice_3D_volume(self):
        control_points = (
            (
                ((0.0, 0.0, 0.0), (0.0, 0.0, 30.0)),
                ((0.0, 20.0, 0.0), (0.0, 20.0, 30.0)),
            ),
            (
                ((10.0, 0.0, 0.0), (10.0, 0.0, 30.0)),
                ((10.0, 20.0, 0.0), (10.0, 20.0, 30.0)),
            ),
        )

        kv_t = (0, 0, 1, 1)
        kv_u = (0, 0, 1, 1)
        kv_v = (0, 0, 1, 1)
        deg_t = 1
        deg_u = 1
        deg_v = 1

        V = bsp.Volume(
            knot_vector_t=kv_t,
            knot_vector_u=kv_u,
            knot_vector_v=kv_v,
            coefficients=control_points,
            degree_t=deg_t,
            degree_u=deg_u,
            degree_v=deg_v,
        )

        known_evaluation_times = (0.0, 0.5, 1.0)  # in this example, same in t, u, v
        calc_evaluation_times_t = V.evaluation_times_t
        calc_evaluation_times_u = V.evaluation_times_u
        calc_evaluation_times_v = V.evaluation_times_v

        self.assertTrue(self.same(known_evaluation_times, calc_evaluation_times_t))
        self.assertTrue(self.same(known_evaluation_times, calc_evaluation_times_u))
        self.assertTrue(self.same(known_evaluation_times, calc_evaluation_times_v))

        known_volume_evaluations_x = (
            ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
            ((5.0, 5.0, 5.0), (5.0, 5.0, 5.0), (5.0, 5.0, 5.0)),
            ((10.0, 10.0, 10.0), (10.0, 10.0, 10.0), (10.0, 10.0, 10.0)),
        )

        known_volume_evaluations_y = (
            ((0.0, 0.0, 0.0), (10.0, 10.0, 10.0), (20.0, 20.0, 20.0)),
            ((0.0, 0.0, 0.0), (10.0, 10.0, 10.0), (20.0, 20.0, 20.0)),
            ((0.0, 0.0, 0.0), (10.0, 10.0, 10.0), (20.0, 20.0, 20.0)),
        )

        known_volume_evaluations_z = (
            ((0.0, 15.0, 30.0), (0.0, 15.0, 30.0), (0.0, 15.0, 30.0)),
            ((0.0, 15.0, 30.0), (0.0, 15.0, 30.0), (0.0, 15.0, 30.0)),
            ((0.0, 15.0, 30.0), (0.0, 15.0, 30.0), (0.0, 15.0, 30.0)),
        )

        ix, iy, iz = 0, 1, 2  # coordinate index for x, y, and z

        self.assertTrue(
            self.same(
                np.array(known_volume_evaluations_x).flatten(),
                V.evaluations[ix].flatten(),
            )
        )

        self.assertTrue(
            self.same(
                np.array(known_volume_evaluations_y).flatten(),
                V.evaluations[iy].flatten(),
            )
        )

        self.assertTrue(
            self.same(
                np.array(known_volume_evaluations_z).flatten(),
                V.evaluations[iz].flatten(),
            )
        )

    # @pytest.mark.skip(reason="work in progress")
    def test_301_Bingol_3D_volume(self):
        """Tests creation and plotting of BSpline surface, compared to
        GitHub repository orbingol
        https://github.com/orbingol/NURBS-Python/blob/5.x/geomdl/BSpline.py

        Example usage:

        $ conda activate nurbspyenv
        $ cd nurbspy/
        $ python
        > from geomdl import BSpline
        > from geomdl.visualization import VisMPL as vis
        >
        > vol = BSpline.Volume()
        >
        > vol.degree_u = 1
        > vol.degree_v = 1
        > vol.degree_w = 1
        >
        > vol.ctrlpts_size_u = 2
        > vol.ctrlpts_size_v = 2
        > vol.ctrlpts_size_w = 2
        >
        x  # Not with 3D structure, use flat list instead.
        x  > control_points = [
        x      [
        x          [
        x              [0.0, 0.0, 0.0],
        x              [0.0, 0.0, 30.0]
        x          ],
        x          [
        x              [0.0, 20.0, 0.0],
        x              [0.0, 20.0, 30.0]
        x          ]
        x      ],
        x      [
        x          [
        x              [10.0, 0.0, 0.0],
        x              [10.0, 0.0, 30.0]
        x          ],
        x          [
        x              [10.0, 20.0, 0.0],
        x              [10.0, 20.0, 30.0]
        x          ]
        x      ]
        x  ]
        > control_points = [
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 30.0],
            [0.0, 20.0, 0.0],
            [0.0, 20.0, 30.0],
            [10.0, 0.0, 0.0],
            [10.0, 0.0, 30.0],
            [10.0, 20.0, 0.0],
            [10.0, 20.0, 30.0]
        ]
        > vol.ctrlpts = control_points
        >
        > vol.knotvector_u = [0, 0, 1, 1]
        > vol.knotvector_v = [0, 0, 1, 1]
        > vol.knotvector_w = [0, 0, 1, 1]
        >
        > vol.delta = 0.5  # two intervals for testing
        > vol.evaluate()
        >
        > vol.vis = vis.VisVolume()
        > vol.render()
        > vol_points = vol.evalpts
        > vol_points  # displays list of eight 3D-points
        [[0.0, 0.0, 0.0], [10.0, 0.0, 0.0], [0.0, 0.0, 30.0], [10.0, 0.0, 30.0], [0.0, 20.0, 0.0], [10.0, 20.0, 0.0], [0.0, 20.0, 30.0], [10.0, 20.0, 30.0]]
        > len(vol_points)
        8
        #
        # -----------------
        # refinement 1 of 2
        # -----------------
        > vol.delta = 1.0 / 3.0
        > vol.evaluate()
        > vol.vis = vis.VisVolume()
        > vol.render()
        > vol_points = vol.evalpts
        > vol_points
        [[0.0, 0.0, 0.0], [5.0, 0.0, 0.0], [10.0, 0.0, 0.0], [0.0, 0.0, 15.0], [5.0, 0.0, 15.0], [10.0, 0.0, 15.0], [0.0, 0.0, 30.0], [5.0, 0.0, 30.0], [10.0, 0.0, 30.0], [0.0, 10.0, 0.0], [5.0, 10.0, 0.0], [10.0, 10.0, 0.0], [0.0, 10.0, 15.0], [5.0, 10.0, 15.0], [10.0, 10.0, 15.0], [0.0, 10.0, 30.0], [5.0, 10.0, 30.0], [10.0, 10.0, 30.0], [0.0, 20.0, 0.0], [5.0, 20.0, 0.0], [10.0, 20.0, 0.0], [0.0, 20.0, 15.0], [5.0, 20.0, 15.0], [10.0, 20.0, 15.0], [0.0, 20.0, 30.0], [5.0, 20.0, 30.0], [10.0, 20.0, 30.0]]
        > len(vol_points)
        27
        """
        control_points = (
            (
                ((0.0, 0.0, 0.0), (0.0, 0.0, 30.0)),
                ((0.0, 20.0, 0.0), (0.0, 20.0, 30.0)),
            ),
            (
                ((10.0, 0.0, 0.0), (10.0, 0.0, 30.0)),
                ((10.0, 20.0, 0.0), (10.0, 20.0, 30.0)),
            ),
        )

        kv_t = (0, 0, 1, 1)
        kv_u = (0, 0, 1, 1)
        kv_v = (0, 0, 1, 1)
        deg_t = 1
        deg_u = 1
        deg_v = 1

        V = bsp.Volume(
            knot_vector_t=kv_t,
            knot_vector_u=kv_u,
            knot_vector_v=kv_v,
            coefficients=control_points,
            degree_t=deg_t,
            degree_u=deg_u,
            degree_v=deg_v,
        )

        known_points = [
            [0.0, 0.0, 0.0],
            [5.0, 0.0, 0.0],
            [10.0, 0.0, 0.0],
            [0.0, 0.0, 15.0],
            [5.0, 0.0, 15.0],
            [10.0, 0.0, 15.0],
            [0.0, 0.0, 30.0],
            [5.0, 0.0, 30.0],
            [10.0, 0.0, 30.0],
            [0.0, 10.0, 0.0],
            [5.0, 10.0, 0.0],
            [10.0, 10.0, 0.0],
            [0.0, 10.0, 15.0],
            [5.0, 10.0, 15.0],
            [10.0, 10.0, 15.0],
            [0.0, 10.0, 30.0],
            [5.0, 10.0, 30.0],
            [10.0, 10.0, 30.0],
            [0.0, 20.0, 0.0],
            [5.0, 20.0, 0.0],
            [10.0, 20.0, 0.0],
            [0.0, 20.0, 15.0],
            [5.0, 20.0, 15.0],
            [10.0, 20.0, 15.0],
            [0.0, 20.0, 30.0],
            [5.0, 20.0, 30.0],
            [10.0, 20.0, 30.0],
        ]

        ix, iy, iz = 0, 1, 2  # coordinate index for x, y, and z

        calc_points_x = V.evaluations[ix].flatten()
        calc_points_y = V.evaluations[iy].flatten()
        calc_points_z = V.evaluations[iz].flatten()

        calc_points = np.transpose([calc_points_x, calc_points_y, calc_points_z])
        assert len(calc_points) == 27
        assert len(known_points) == len(calc_points)

        # pluck calculated points from matched known points, check known_points is an
        # empty list thereafter
        for i in calc_points:
            known_points.remove(i.tolist())
        assert len(known_points) == 0

        """
        # -----------------
        # refinement 2 of 2
        # -----------------
        > vol.delta = 1.0 / 5.0
        > vol.evaluate()
        > vol.vis = vis.VisVolume()
        > vol.render()
        > vol_points = vol.evalpts
        > vol_points
        [[0.0, 0.0, 0.0], [2.5, 0.0, 0.0], [5.0, 0.0, 0.0], [7.5, 0.0, 0.0], [10.0, 0.0, 0.0], [0.0, 0.0, 7.5], [2.5, 0.0, 7.5], [5.0, 0.0, 7.5], [7.5, 0.0, 7.5], [10.0, 0.0, 7.5], [0.0, 0.0, 15.0], [2.5, 0.0, 15.0], [5.0, 0.0, 15.0], [7.5, 0.0, 15.0], [10.0, 0.0, 15.0], [0.0, 0.0, 22.5], [2.5, 0.0, 22.5], [5.0, 0.0, 22.5], [7.5, 0.0, 22.5], [10.0, 0.0, 22.5], [0.0, 0.0, 30.0], [2.5, 0.0, 30.0], [5.0, 0.0, 30.0], [7.5, 0.0, 30.0], [10.0, 0.0, 30.0], [0.0, 5.0, 0.0], [2.5, 5.0, 0.0], [5.0, 5.0, 0.0], [7.5, 5.0, 0.0], [10.0, 5.0, 0.0], [0.0, 5.0, 7.5], [2.5, 5.0, 7.5], [5.0, 5.0, 7.5], [7.5, 5.0, 7.5], [10.0, 5.0, 7.5], [0.0, 5.0, 15.0], [2.5, 5.0, 15.0], [5.0, 5.0, 15.0], [7.5, 5.0, 15.0], [10.0, 5.0, 15.0], [0.0, 5.0, 22.5], [2.5, 5.0, 22.5], [5.0, 5.0, 22.5], [7.5, 5.0, 22.5], [10.0, 5.0, 22.5], [0.0, 5.0, 30.0], [2.5, 5.0, 30.0], [5.0, 5.0, 30.0], [7.5, 5.0, 30.0], [10.0, 5.0, 30.0], [0.0, 10.0, 0.0], [2.5, 10.0, 0.0], [5.0, 10.0, 0.0], [7.5, 10.0, 0.0], [10.0, 10.0, 0.0], [0.0, 10.0, 7.5], [2.5, 10.0, 7.5], [5.0, 10.0, 7.5], [7.5, 10.0, 7.5], [10.0, 10.0, 7.5], [0.0, 10.0, 15.0], [2.5, 10.0, 15.0], [5.0, 10.0, 15.0], [7.5, 10.0, 15.0], [10.0, 10.0, 15.0], [0.0, 10.0, 22.5], [2.5, 10.0, 22.5], [5.0, 10.0, 22.5], [7.5, 10.0, 22.5], [10.0, 10.0, 22.5], [0.0, 10.0, 30.0], [2.5, 10.0, 30.0], [5.0, 10.0, 30.0], [7.5, 10.0, 30.0], [10.0, 10.0, 30.0], [0.0, 15.0, 0.0], [2.5, 15.0, 0.0], [5.0, 15.0, 0.0], [7.5, 15.0, 0.0], [10.0, 15.0, 0.0], [0.0, 15.0, 7.5], [2.5, 15.0, 7.5], [5.0, 15.0, 7.5], [7.5, 15.0, 7.5], [10.0, 15.0, 7.5], [0.0, 15.0, 15.0], [2.5, 15.0, 15.0], [5.0, 15.0, 15.0], [7.5, 15.0, 15.0], [10.0, 15.0, 15.0], [0.0, 15.0, 22.5], [2.5, 15.0, 22.5], [5.0, 15.0, 22.5], [7.5, 15.0, 22.5], [10.0, 15.0, 22.5], [0.0, 15.0, 30.0], [2.5, 15.0, 30.0], [5.0, 15.0, 30.0], [7.5, 15.0, 30.0], [10.0, 15.0, 30.0], [0.0, 20.0, 0.0], [2.5, 20.0, 0.0], [5.0, 20.0, 0.0], [7.5, 20.0, 0.0], [10.0, 20.0, 0.0], [0.0, 20.0, 7.5], [2.5, 20.0, 7.5], [5.0, 20.0, 7.5], [7.5, 20.0, 7.5], [10.0, 20.0, 7.5], [0.0, 20.0, 15.0], [2.5, 20.0, 15.0], [5.0, 20.0, 15.0], [7.5, 20.0, 15.0], [10.0, 20.0, 15.0], [0.0, 20.0, 22.5], [2.5, 20.0, 22.5], [5.0, 20.0, 22.5], [7.5, 20.0, 22.5], [10.0, 20.0, 22.5], [0.0, 20.0, 30.0], [2.5, 20.0, 30.0], [5.0, 20.0, 30.0], [7.5, 20.0, 30.0], [10.0, 20.0, 30.0]]
        > len(vol_points)
        125
        """
        V2 = bsp.Volume(
            knot_vector_t=kv_t,
            knot_vector_u=kv_u,
            knot_vector_v=kv_v,
            coefficients=control_points,
            degree_t=deg_t,
            degree_u=deg_u,
            degree_v=deg_v,
            n_bisections=2,
        )

        known_points = [
            [0.0, 0.0, 0.0],
            [2.5, 0.0, 0.0],
            [5.0, 0.0, 0.0],
            [7.5, 0.0, 0.0],
            [10.0, 0.0, 0.0],
            [0.0, 0.0, 7.5],
            [2.5, 0.0, 7.5],
            [5.0, 0.0, 7.5],
            [7.5, 0.0, 7.5],
            [10.0, 0.0, 7.5],
            [0.0, 0.0, 15.0],
            [2.5, 0.0, 15.0],
            [5.0, 0.0, 15.0],
            [7.5, 0.0, 15.0],
            [10.0, 0.0, 15.0],
            [0.0, 0.0, 22.5],
            [2.5, 0.0, 22.5],
            [5.0, 0.0, 22.5],
            [7.5, 0.0, 22.5],
            [10.0, 0.0, 22.5],
            [0.0, 0.0, 30.0],
            [2.5, 0.0, 30.0],
            [5.0, 0.0, 30.0],
            [7.5, 0.0, 30.0],
            [10.0, 0.0, 30.0],
            [0.0, 5.0, 0.0],
            [2.5, 5.0, 0.0],
            [5.0, 5.0, 0.0],
            [7.5, 5.0, 0.0],
            [10.0, 5.0, 0.0],
            [0.0, 5.0, 7.5],
            [2.5, 5.0, 7.5],
            [5.0, 5.0, 7.5],
            [7.5, 5.0, 7.5],
            [10.0, 5.0, 7.5],
            [0.0, 5.0, 15.0],
            [2.5, 5.0, 15.0],
            [5.0, 5.0, 15.0],
            [7.5, 5.0, 15.0],
            [10.0, 5.0, 15.0],
            [0.0, 5.0, 22.5],
            [2.5, 5.0, 22.5],
            [5.0, 5.0, 22.5],
            [7.5, 5.0, 22.5],
            [10.0, 5.0, 22.5],
            [0.0, 5.0, 30.0],
            [2.5, 5.0, 30.0],
            [5.0, 5.0, 30.0],
            [7.5, 5.0, 30.0],
            [10.0, 5.0, 30.0],
            [0.0, 10.0, 0.0],
            [2.5, 10.0, 0.0],
            [5.0, 10.0, 0.0],
            [7.5, 10.0, 0.0],
            [10.0, 10.0, 0.0],
            [0.0, 10.0, 7.5],
            [2.5, 10.0, 7.5],
            [5.0, 10.0, 7.5],
            [7.5, 10.0, 7.5],
            [10.0, 10.0, 7.5],
            [0.0, 10.0, 15.0],
            [2.5, 10.0, 15.0],
            [5.0, 10.0, 15.0],
            [7.5, 10.0, 15.0],
            [10.0, 10.0, 15.0],
            [0.0, 10.0, 22.5],
            [2.5, 10.0, 22.5],
            [5.0, 10.0, 22.5],
            [7.5, 10.0, 22.5],
            [10.0, 10.0, 22.5],
            [0.0, 10.0, 30.0],
            [2.5, 10.0, 30.0],
            [5.0, 10.0, 30.0],
            [7.5, 10.0, 30.0],
            [10.0, 10.0, 30.0],
            [0.0, 15.0, 0.0],
            [2.5, 15.0, 0.0],
            [5.0, 15.0, 0.0],
            [7.5, 15.0, 0.0],
            [10.0, 15.0, 0.0],
            [0.0, 15.0, 7.5],
            [2.5, 15.0, 7.5],
            [5.0, 15.0, 7.5],
            [7.5, 15.0, 7.5],
            [10.0, 15.0, 7.5],
            [0.0, 15.0, 15.0],
            [2.5, 15.0, 15.0],
            [5.0, 15.0, 15.0],
            [7.5, 15.0, 15.0],
            [10.0, 15.0, 15.0],
            [0.0, 15.0, 22.5],
            [2.5, 15.0, 22.5],
            [5.0, 15.0, 22.5],
            [7.5, 15.0, 22.5],
            [10.0, 15.0, 22.5],
            [0.0, 15.0, 30.0],
            [2.5, 15.0, 30.0],
            [5.0, 15.0, 30.0],
            [7.5, 15.0, 30.0],
            [10.0, 15.0, 30.0],
            [0.0, 20.0, 0.0],
            [2.5, 20.0, 0.0],
            [5.0, 20.0, 0.0],
            [7.5, 20.0, 0.0],
            [10.0, 20.0, 0.0],
            [0.0, 20.0, 7.5],
            [2.5, 20.0, 7.5],
            [5.0, 20.0, 7.5],
            [7.5, 20.0, 7.5],
            [10.0, 20.0, 7.5],
            [0.0, 20.0, 15.0],
            [2.5, 20.0, 15.0],
            [5.0, 20.0, 15.0],
            [7.5, 20.0, 15.0],
            [10.0, 20.0, 15.0],
            [0.0, 20.0, 22.5],
            [2.5, 20.0, 22.5],
            [5.0, 20.0, 22.5],
            [7.5, 20.0, 22.5],
            [10.0, 20.0, 22.5],
            [0.0, 20.0, 30.0],
            [2.5, 20.0, 30.0],
            [5.0, 20.0, 30.0],
            [7.5, 20.0, 30.0],
            [10.0, 20.0, 30.0],
        ]

        calc_points_x = V2.evaluations[ix].flatten()
        calc_points_y = V2.evaluations[iy].flatten()
        calc_points_z = V2.evaluations[iz].flatten()

        calc_points = np.transpose([calc_points_x, calc_points_y, calc_points_z])
        assert len(calc_points) == 125
        assert len(known_points) == len(calc_points)

        # pluck calculated points from matched known points, check known_points is an
        # empty list thereafter
        for i in calc_points:
            known_points.remove(i.tolist())
        assert len(known_points) == 0


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
