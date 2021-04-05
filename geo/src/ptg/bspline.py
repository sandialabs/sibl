from typing import Union

from scipy.interpolate import BSpline as scipy_bspline
import numpy as np


def evaluation_times(
    *, knot_vector: Union[list, tuple], degree: int = 0, n_bisections: int = 1,
) -> list:
    """Returns the parameter evaluation times for a parameter space, e.g.,
    parameter `t`, `u` or `v`.

    Keywork Arguments:
        knot_vector (float array): knot vector for curve parameterized by
            a pseudo-time variable `t`, `u`, or `v`.
            e.g., for `t` variable:
                len(knot_vector) = (I + 1)
                len(knot_vector) = len(coefficients) + (degree_t + 1)
                (I + 1) knots with (I) knot spans
            must have length of two or more
            must be a non-decreasing sequence
        degree (int): polynomial degree, e.g., p=0: constant,
            p=1: linear, p=2: quadratic, p=3: cubic, etc.
            Defaults to 1.
        n_bisections (int): number of time interval bisections
            e.g., for `t` in per-knot-span interval [t_i, t_{i+1}],
            likewise for `u` and `v` parameters.
            Defaults to 1.

    Returns:
        list: The pueudo-time parameter `t` (or `u` or `v`) evaluation times
            spanning the knot vector with `n_bisection` bisections.

    Raises:
        ValueError: If `len(knot_vector)` < 2.  Minimum `knot_vector` length is 2.
        ValueError: If `degree` < 0.  The `degree` must be non-negative.
        ValueError: If `n_bisections` < 1.  Minimum `n_bisections` is 1.
        ValueError: If the knot vector is decreasing.
    """
    if not len(knot_vector) >= 2:
        raise ValueError("Error: knot vector length must be two or greater.")

    if not degree >= 0:
        raise ValueError("Error: polynomial degree must be a non-negative integer.")

    if not n_bisections >= 1:
        raise ValueError(
            "Error: number of time interval bisections must be an integer >= 1."
        )

    knots_lhs = knot_vector[0:-1]  # left-hand-side knot values
    knots_rhs = knot_vector[1:]  # right-hand-side knot values
    knot_spans = np.array(knots_rhs) - np.array(knots_lhs)
    dt = knot_spans / (2.0 ** n_bisections)

    # assert all([dti >= 0 for dti in dt]), "Error: knot vector is decreasing."
    if not all([dti >= 0 for dti in dt]):
        raise ValueError("Error: knot vector is decreasing.")

    num_knots = len(knot_vector)
    _evaluation_times = [
        knots_lhs[k] + j * dt[k]
        for k in np.arange(num_knots - 1)
        for j in np.arange(2 ** n_bisections)
    ]

    # append the last knot
    _evaluation_times.append(knot_vector[-1])

    # recast as numpy array
    _evaluation_times = np.array(_evaluation_times)

    # retain only non-repeated evaluation points
    # at beginning and end
    i_repeat = 2 ** n_bisections * degree
    _evaluation_times = _evaluation_times[i_repeat:-i_repeat]
    return _evaluation_times


class Curve:
    """Creates a B-Spline curve.

    Args:
        knot_vector_t (float array): [t0, t1, t2, ... tI]
            len(knot_vector_t) = (I + 1)
            len(knot_vector_t) = len(coefficients) + (degree_t + 1)
            (I + 1) knots with (I) knot spans
            must have length of two or more
            must be a non-decreasing sequence
        coefficients (float array):
            coordinates (x, y, z), with `(x, y, z)_coefficient_n` as in
            spline coefficients [c0, c1, c2, ... cn]
            len(coefficients) = (n + 1)
        degree_t (int >= 0): B-spline polynomial degree.  Defaults to 0.
        verbose (bool): prints extended error checking, default False

    Example:
        # This example implements part of the unit test method
        # test_003_curve_basis_recover_bezier_linear in test_bspline.py unit test.
        #
        > cd ~/sibl
        > conda activate siblenv
        > python
        >>> import numpy as np
        >>> import ptg.bspline as bsp
        >>> kv = list(map(float, [0, 0, 1, 1]))
        >>> degree = 1
        >>> coef_N0_p1 = [1.0, 0.0]
        >>> N0_p1 = bsp.Curve(kv, coef_N0_p1, degree)
        >>> N0_p1.is_valid()
        True
        >>> tmin, tmax, npts = 0.0, 1.0, 5
        >>> t = np.linspace(tmin, tmax, npts, endpoint=True)
        >>> f_of_t = N0_p1.evaluate(t)
        >>> f_of_t
        array([1.  , 0.75, 0.5 , 0.25, 0.  ])
    """

    def __init__(
        self,
        knot_vector_t: Union[list, tuple],
        coefficients: Union[list, tuple],
        degree_t: int = 0,
        verbose: bool = False,
    ):
        self.kv = knot_vector_t
        self.c = coefficients
        self.p = degree_t
        self.verbose = verbose
        self.valid = False
        self._bspline = None
        # self.is_valid()  # not sure if I want to call or not, to be determined

    def is_valid(self):

        try:
            assert len(self.kv) >= 2, "Error: knot vector mininum length is two."
            assert self.p >= 0, "Error: degree must be non-negative."

            assert (
                len(self.kv) == len(self.c) + self.p + 1
            ), "Error: knot vector length is invalid."

            self.valid = True
            self._bspline = scipy_bspline(self.kv, self.c, self.p, extrapolate=False)
            return self.valid

        except AssertionError as error:
            if self.verbose:
                print(error)
            return error

    def evaluate(self, t):
        """Evaluate the BSpline curve at all points `t`."""

        # y = np.nan_to_num(self._bspline(t), nan=0.0)
        # y = self._bspline(t)
        # return y
        return self._bspline(t)


class Surface:
    def __init__(
        self,
        knot_vector_t: Union[list, tuple],
        knot_vector_u: Union[list, tuple],
        coefficients: Union[list, tuple],
        degree_t: int = 0,
        degree_u: int = 0,
        n_bisections: int = 1,
        verbose: bool = False,
    ):
        """Creates a B-Spline surface.

        Args:
            knot_vector_t (float array): knot vector for curve parameterized by `t`.
                len(knot_vector_t) = (I + 1)
                len(knot_vector_t) = len(coefficients) + (degree_t + 1)
                (I + 1) knots with (I) knot spans
                must have length of two or more
                must be a non-decreasing sequence
            knot_vector_u (float array): knot vector for curve parameterized by `u`.
                len(knot_vector_u) = (J + 1)
                len(knot_vector_u) = len(coefficients[0]) + (degree_u + 1)
                (J + 1) knots with (J) knot spans
                must have length of two or more
                must be a non-decreasing sequence
            coefficients (float array): control net/grid of points with
                coordinates (x, y, z), with `(x, y, z)_coefficient_nm` as in
                [
                    [[x, y, z]_c00, [x, y, z]_c01, ... [x, y, z]_c0m],
                    [[x, y, z]_cn0, [x, y, z]_cn1, ... [x, y, z]_cnm]
                ]
            degree_t: (int >=0): B-spline polynomial degree for spline in `t`.
                Defaults to 0.
            degree_u: (int >=0): B-spline polynomial degree for spline in `u`.
                Defaults to 0.
            n_bisections (int): Number of bisections per knot span for both `t` and `u`.
                Defaults to 1.
            verbose (bool): prints extended error checking, default False

        Example:
            To come.
        """
        # ncp_t: number of control points for the t parameter
        # ncp_u: number of control points for the u parameter
        # nsd: number of space dimensions, typically 2 or 3
        self.valid = False
        self.verbose = verbose
        self.ncp_t, self.ncp_u, self.nsd = np.array(coefficients).shape

        # knots_t_lhs = knot_vector_t[0:-1]  # left-hand-side knot values for t
        # knots_t_rhs = knot_vector_t[1:]  # right-hand-side knot values for t
        # knot_t_spans = np.array(knots_t_rhs) - np.array(knots_t_lhs)
        # dt = knot_t_spans / (2.0 ** n_bisections)
        # assert all([dti >= 0 for dti in dt]), "Error: knot vector T is decreasing."
        # num_knots_t = len(knot_vector_t)
        # self.t = [
        #     knots_t_lhs[k] + j * dt[k]
        #     for k in np.arange(num_knots_t - 1)
        #     for j in np.arange(2 ** n_bisections)
        # ]
        # self.t.append(knot_vector_t[-1])
        # self.t = np.array(self.t)
        # # retain only non-repeated evaluation points at beginning and end
        # t_repeated_index = 2 ** n_bisections * degree_t
        # self.t = self.t[t_repeated_index:-t_repeated_index]

        # knots_u_lhs = knot_vector_u[0:-1]  # left-hand-side knot values for u
        # knots_u_rhs = knot_vector_u[1:]  # right-hand-side knot values for u
        # knot_u_spans = np.array(knots_u_rhs) - np.array(knots_u_lhs)
        # du = knot_u_spans / (2.0 ** n_bisections)
        # assert all([duj >= 0 for duj in du]), "Error: knot vector U is decreasing."
        # num_knots_u = len(knot_vector_u)
        # self.u = [
        #     knots_u_lhs[k] + j * du[k]
        #     for k in np.arange(num_knots_u - 1)
        #     for j in np.arange(2 ** n_bisections)
        # ]
        # self.u.append(knot_vector_u[-1])
        # self.u = np.array(self.u)
        # # retain only non-repeated evaluation points at beginning and end
        # u_repeated_index = 2 ** n_bisections * degree_u
        # self.u = self.u[u_repeated_index:-u_repeated_index]

        # self._t_new = evaluation_times(
        #     knot_vector=knot_vector_t, degree=degree_t, n_bisections=n_bisections
        # )
        # self._u_new = evaluation_times(
        #     knot_vector=knot_vector_u, degree=degree_u, n_bisections=n_bisections
        # )

        # assert np.norm(self._t_new - self.t < 0.00001)
        # assert np.norm(self._u_new - self.u > 0.00001)

        self.t = evaluation_times(
            knot_vector=knot_vector_t, degree=degree_t, n_bisections=n_bisections
        )
        self.u = evaluation_times(
            knot_vector=knot_vector_u, degree=degree_u, n_bisections=n_bisections
        )

        self.x_of_t_u = np.zeros((len(self.t), len(self.u)), dtype=float)
        self.y_of_t_u = np.zeros((len(self.t), len(self.u)), dtype=float)
        self.z_of_t_u = np.zeros((len(self.t), len(self.u)), dtype=float)

        ix = 0  # x-coordinate index
        iy = 1  # y-coordinate index
        iz = 2  # z-coordinate index

        for i in np.arange(self.ncp_t):
            for j in np.arange(self.ncp_u):

                N_coef_t = np.zeros(self.ncp_t)
                N_coef_u = np.zeros(self.ncp_u)

                N_coef_t[i] = 1.0
                N_coef_u[j] = 1.0

                Ni = Curve(knot_vector_t, N_coef_t, degree_t)
                Nj = Curve(knot_vector_u, N_coef_u, degree_u)

                if Ni.is_valid() and Nj.is_valid():
                    Ni_of_t = Ni.evaluate(self.t)
                    Nj_of_u = Nj.evaluate(self.u)
                    Nij = np.outer(Ni_of_t, Nj_of_u)

                    coef_x = coefficients[i][j][ix]
                    coef_y = coefficients[i][j][iy]
                    coef_z = coefficients[i][j][iz]

                    self.x_of_t_u += Nij * coef_x
                    self.y_of_t_u += Nij * coef_y
                    self.z_of_t_u += Nij * coef_z

        self.valid = True

    @property
    def evaluations(self):
        """Returns the BSpline surface at all parameter evaluation points `t` and `u`."""

        """
            Returns:
                A tuple of (x, y, z) values, evaluated over all parameterization
                points `t` and `u`.

            Raises:
                AssertionError if the BSpline surface has not been properly defined.
        """
        try:
            assert self.valid
            return (self.x_of_t_u, self.y_of_t_u, self.z_of_t_u)

        except AssertionError as error:
            if self.verbose:
                print(error)
            # return error
            return (None, None, None)

    @property
    def evaluation_times_t(self):
        """Returns the BSpline surface evaluation time parameters in the `t` direction."""
        return self.t

    @property
    def evaluation_times_u(self):
        """Returns the BSpline surface evaluation time parameters in the `u` direction."""
        return self.u


class Volume:
    def __init__(
        self,
        *,
        knot_vector_t: Union[list, tuple],
        knot_vector_u: Union[list, tuple],
        knot_vector_v: Union[list, tuple],
        coefficients: Union[list, tuple],
        degree_t: int = 0,
        degree_u: int = 0,
        degree_v: int = 0,
        n_bisections: int = 1,
        verbose: bool = False,
    ):
        """Creates a B-Spline volume.

        Args:
            knot_vector_t (float array): knot vector for curve parameterized by `t`.
                len(knot_vector_t) = (I + 1)
                len(knot_vector_t) = len(coefficients) + (degree_t + 1)
                (I + 1) knots with (I) knot spans
                must have length of two or more
                must be a non-decreasing sequence
            knot_vector_u (float array): knot vector for curve parameterized by `u`.
                len(knot_vector_u) = (J + 1)
                len(knot_vector_u) = len(coefficients[0]) + (degree_u + 1)
                (J + 1) knots with (J) knot spans
                must have length of two or more
                must be a non-decreasing sequence
            knot_vector_v (float array): knot vector for curve parameterized by `v`.
                len(knot_vector_v) = (K + 1)
                len(knot_vector_v) = len(coefficients[0][0]) + (degree_v + 1)
                (K + 1) knots with (K) knot spans
                must have length of two or more
                must be a non-decreasing sequence
            coefficients (float array): control lattice of points with
                coordinates (x, y, z), with `(x, y, z)_coefficient_nml` as in
                [
                    [ # layer 0
                        [[x, y, z]_c000, [x, y, z]_c001, ... [x, y, z]_c00l],
                        [[x, y, z]_c0m0, [x, y, z]_c0m1, ... [x, y, z]_c0ml]
                    ],
                    [ # layer n
                        [[x, y, z]_cn00, [x, y, z]_cn01, ... [x, y, z]_cn0l],
                        [[x, y, z]_cnm0, [x, y, z]_cnm1, ... [x, y, z]_cnml]
                    ]
                ]
                (n+1 layers) x (m+1 rows) x (l+1 columns)
            degree_t: (int >=0): B-spline polynomial degree for spline in `t`.
                Defaults to 0.
            degree_u: (int >=0): B-spline polynomial degree for spline in `u`.
                Defaults to 0.
            degree_v: (int >=0): B-spline polynomial degree for spline in `v`.
                Defaults to 0.
            n_bisections (int): Number of bisections per knot span for each of the
                `t`, `u`, and `v` parameters.
                Defaults to 1.
            verbose (bool): prints extended error checking, default False

        Example:
            To come.
        """
        self.valid = False
        self.verbose = verbose
        # self.ncp_t, self.ncp_u, self.nsd = np.array(coefficients).shape
        self.ncp_t, self.ncp_u, self.ncp_v, self.nsd = np.array(coefficients).shape

        self.t = evaluation_times(
            knot_vector=knot_vector_t, degree=degree_t, n_bisections=n_bisections
        )
        self.u = evaluation_times(
            knot_vector=knot_vector_u, degree=degree_u, n_bisections=n_bisections
        )
        self.v = evaluation_times(
            knot_vector=knot_vector_v, degree=degree_v, n_bisections=n_bisections
        )

        self.x_of_t_u_v = np.zeros((len(self.t), len(self.u), len(self.v)), dtype=float)
        self.y_of_t_u_v = np.zeros((len(self.t), len(self.u), len(self.v)), dtype=float)
        self.z_of_t_u_v = np.zeros((len(self.t), len(self.u), len(self.v)), dtype=float)

        ix = 0  # x-coordinate index
        iy = 1  # y-coordinate index
        iz = 2  # z-coordinate index

        for i in np.arange(self.ncp_t):
            for j in np.arange(self.ncp_u):
                for k in np.arange(self.ncp_v):

                    N_coef_t = np.zeros(self.ncp_t)
                    N_coef_u = np.zeros(self.ncp_u)
                    N_coef_v = np.zeros(self.ncp_v)

                    N_coef_t[i] = 1.0
                    N_coef_u[j] = 1.0
                    N_coef_v[k] = 1.0

                    # walk the curves and make three outer products
                    Ni = Curve(knot_vector_t, N_coef_t, degree_t)
                    Nj = Curve(knot_vector_u, N_coef_u, degree_u)
                    Nk = Curve(knot_vector_v, N_coef_v, degree_v)

                    if Ni.is_valid() and Nj.is_valid() and Nk.is_valid():
                        Ni_of_t = Ni.evaluate(self.t)
                        Nj_of_u = Nj.evaluate(self.u)
                        Nk_of_v = Nk.evaluate(self.v)

                        # Nij = np.outer(Ni_of_t, Nj_of_u)
                        # Nijk = np.outer(Ni_of_t, np.outer(Nj_of_u, Nk_of_v))
                        Nijk = np.array(
                            [_ * np.outer(Nj_of_u, Nk_of_v) for _ in Ni_of_t]
                        )

                        coef_x = coefficients[i][j][k][ix]
                        coef_y = coefficients[i][j][k][iy]
                        coef_z = coefficients[i][j][k][iz]

                        # self.x_of_t_u += Nij * coef_x
                        # self.y_of_t_u += Nij * coef_y
                        # self.z_of_t_u += Nij * coef_z
                        self.x_of_t_u_v += Nijk * coef_x
                        self.y_of_t_u_v += Nijk * coef_y
                        self.z_of_t_u_v += Nijk * coef_z

        self.valid = True

    @property
    def evaluations(self):
        """Returns the BSpline volume at all parameter evaluation points
        `t`, `u`, and `v`."""

        """
            Returns:
                A tuple of (x, y, z) values, evaluated over all parameterization
                points `t`, `u`, and `v`.

            Raises:
                AssertionError if the BSpline volume has not been properly defined.
        """
        try:
            assert self.valid
            return (self.x_of_t_u_v, self.y_of_t_u_v, self.z_of_t_u_v)

        except AssertionError as error:
            if self.verbose:
                print(error)
            # return error
            return (None, None, None)

    @property
    def evaluation_times_t(self):
        """Returns the BSpline volume evaluation time parameters in the `t` direction."""
        return self.t

    @property
    def evaluation_times_u(self):
        """Returns the BSpline volume evaluation time parameters in the `u` direction."""
        return self.u

    @property
    def evaluation_times_v(self):
        """Returns the BSpline volume evaluation time parameters in the `v` direction."""
        return self.v
