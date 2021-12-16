from typing import List, Tuple, Union

import numpy as np
from numpy import ndarray

# from numpy import linalg

import ptg.bspline as bsp


class BSplineFit:
    def __init__(
        self,
        sample_points: Union[List[float], Tuple[float], ndarray],
        degree: int = 0,
        verbose: bool = False,
        sample_time_method: str = "chord",
        knot_method: str = "average",
    ):
        """Creates a B-Spline curve based on fits to sample_points on curve.
        Sample points are either interpolated (default) or approximated (to come).

        Args:
            sample_points (ArrayLike[float]): [[a0, a1, a2, ... am], [b0, b1, b2, ... bm],
                [c0, c1, c2, ... cm]] composed of (m+1) samples points on the curve
                used to generate a fitted B-sline curve.  Coordinate measurements
                (a, b, c) are made in the (x, y, z) directions.
            degree (int >= 0): B-spline polynomial degree
            verbose (bool): prints additional information, default False
            sample_time_method:
                "chord": default, standard method to determine sample times
                "centripetal": (optional), suited for data with sharp turns
            knot_method:
                "average": default, recommended method for placing knots
                "equal": (optional), not recommended, can lead to a singular matrix,
                implemented herein for unit tests and testing purposes only.
        """
        if not isinstance(sample_points, (list, tuple, ndarray)):
            raise TypeError("Error: sample points must be a list, tuple, or ndarray.")

        if degree < 0:
            raise ValueError("Error: degree must be non-negative.")

        if sample_time_method not in ("chord", "centripetal"):
            raise ValueError(
                "Error: sample_time_method must be 'chord' or 'centripetal'"
            )

        if knot_method not in ("average", "equal"):
            raise ValueError("Error: knot_method must be 'average' or 'equal'")

        self.samples = np.asarray(sample_points)
        self.n_samples = len(self.samples)  # (m + 1)
        self._m = self.n_samples - 1  # m index
        self.n_control_points = (
            self.n_samples
        )  # special case n = m, number of control points

        # self.verbose = verbose
        self.valid = False
        self._bspline = None

        # Piegl 1997 page 364-365, chord length method or centripetal method
        chord_lengths = np.zeros(self.n_samples)

        for k in range(1, self.n_samples):
            chord_length = np.linalg.norm(self.samples[k] - self.samples[k - 1])
            if sample_time_method == "chord":
                chord_lengths[k] = chord_length  # norm from Eq. (9.5) Piegl 1997
            else:  # "centripetal"
                chord_lengths[k] = np.sqrt(chord_length)  # sqrt norm Eq. (9.6)

        total_chord_length = sum(chord_lengths)

        self._sample_times = np.zeros(self.n_samples)
        for k in range(1, self.n_samples):
            self._sample_times[k] = (
                self._sample_times[k - 1] + chord_lengths[k] / total_chord_length
            )  # Eq. (9.5) or (9.6) Piegl 1997

        # averaging knots from sample times, Piegl 1997, page 365, Eq. (9.8)
        self._n_knots = degree + 1 + self.n_samples  # (kappa + 1)
        self._kappa = self._n_knots - 1
        self._knot_vector = np.zeros(self._n_knots)
        if knot_method == "average":
            # averaging knots from sample times
            for j in range(1, self._m - degree + 1):  # +1 for Python 0-index
                # _phi_high = degree - 1 + j
                _phi_high = degree + j  # add +1 back in to account for Python 0-index
                _knot_subspan_average = (1 / degree) * sum(
                    self._sample_times[j:_phi_high]
                )
                self._knot_vector[degree + j] = _knot_subspan_average
        else:
            # knot_method is "equal"
            for j in range(1, self._m - degree + 1):  # +1 for Python 0-index
                self._knot_vector[degree + j] = j / (self._m - degree + 1)
        # append end of knot vector with 1.0 repeated (degree + 1) times
        _kappa_minus_p = self._kappa - degree
        self._knot_vector[_kappa_minus_p : self._kappa + 1] = 1.0  # Python 0-index

        # matrix A u = f -> (notation) N u = f
        self._sample_basis_matrix = []  # (m x 1) by (n x 1) coefficient matrix
        for column in range(self.n_control_points):
            coef = np.zeros(self.n_control_points)
            coef[column] = 1.0

            # build the B-spline basis functions column-by-column
            _bspline_basis_function = bsp.Curve(self.knot_vector, coef, degree)

            if _bspline_basis_function.is_valid():
                _y = _bspline_basis_function.evaluate(self.sample_times)
                self._sample_basis_matrix.append(_y)

        # now transpose the N matrix, since we filled column-wise
        self._sample_basis_matrix = np.transpose(self._sample_basis_matrix)

        # self.control_points = np.linalg.solve(self._N, sample_points)
        self._control_points = np.linalg.solve(self._sample_basis_matrix, self.samples)

        self.valid = True  # if we come to the end of __init__, all is valid

    @property
    def control_points(self):
        """Returns the B-spline control points that fit the sample point data."""
        return self._control_points

    @property
    def knot_vector(self):
        """Returns the knot vector generated from the averaging method of the sample
        point times."""
        return self._knot_vector

    @property
    def sample_basis_matrix(self):
        """Returns the matrix of B-spline basis functions equaluated at sample point
        times."""
        return self._sample_basis_matrix

    @property
    def sample_times(self):
        """Returns the sample times for each sample point based on the 'chord' or
        'centripetal' method."""
        return self._sample_times
