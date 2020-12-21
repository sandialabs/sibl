# from numpy.typing import ArrayLike
from typing import Union, List, Tuple
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
                "centripetal": (optional), better suited for data with sharp turns
            knot_method:
                "average": default, recommended method for placing knots
                "equal": (optional), not recommended, can lead to a singular matrix,
                implemented for unit tests and testing purposes only.
        """
        if not isinstance(sample_points, (list, tuple, ndarray)):
            raise TypeError("Error: sample points must be a list, tuple, or ndarray.")
        # self.samples = sample_points
        self.samples = np.asarray(sample_points)
        self.n_samples = len(self.samples)  # (m + 1)
        self._m = self.n_samples - 1
        self.NCP = self.n_samples  # special case n = m, number of control points

        # assert degree >= 0, "Error: degree must be non-negative."
        if degree < 0:
            raise ValueError("Error: degree must be non-negative.")
        self.DEGREE = degree

        self.verbose = verbose
        self.valid = False
        self._bspline = None
        # self._sample_time_method = kwargs.get("sample_time_method", "chord")
        self._sample_time_method = sample_time_method

        # assert self._sample_time_method in ("chord", "centripetal")
        if self._sample_time_method not in ("chord", "centripetal"):
            raise ValueError(
                "Error: sample_time_method must be 'chord' or 'centripetal'"
            )

        self._knot_method = knot_method

        if self._knot_method not in ("average", "equal"):
            raise ValueError("Error: knot_method must be 'average' or 'equal'")

        # Piegl 1997 page 364-365, chord length method or centripetal method
        chord_lengths = np.zeros(self.n_samples)

        for k in range(1, self.n_samples):
            chord_length = np.linalg.norm(self.samples[k] - self.samples[k - 1])
            if self._sample_time_method == "chord":
                chord_lengths[k] = chord_length  # norm from Eq. (9.5) Piegl 1997
            else:  # "centripetal"
                chord_lengths[k] = np.sqrt(chord_length)  # sqrt norm Eq. (9.6)

        total_chord_length = sum(chord_lengths)

        # self._sample_times = [0.0 for _ in range(self.n_samples)]
        self._sample_times = np.zeros(self.n_samples)
        for k in range(1, self.n_samples):
            self._sample_times[k] = (
                self._sample_times[k - 1] + chord_lengths[k] / total_chord_length
            )  # Eq. (9.5) or (9.6) Piegl 1997

        # averaging knots from sample times, Piegl 1997, page 365, Eq. (9.8)
        self._n_knots = degree + 1 + self.n_samples  # (kappa + 1)
        self._kappa = self._n_knots - 1
        self._knot_vector = np.zeros(self._n_knots)
        if self._knot_method == "average":
            # averaging knots from sample times
            # for j in range(1, self.n_samples - degree + 1):
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
        self._N = []  # (m x 1) by (n x 1) coefficient matrix
        for column in range(self.NCP):
            print(f"column = {column}")
            coef = np.zeros(self.NCP)
            coef[column] = 1.0

            # build the B-spline basis functions column-by-column
            _B = bsp.BSpline(self.knot_vector, coef, self.DEGREE)

            if _B.is_valid():
                _y = _B.evaluate(self.sample_times)
                self._N.append(_y)

        # now transpose the N matrix, since we filled column-wise
        self._N = np.transpose(self._N)

        # self.control_points = np.linalg.solve(self._N, sample_points)
        self._control_points = np.linalg.solve(self._N, self.samples)

        self.valid = True  # if we come to the end of __init__, all is valid

    @property
    def sample_times(self):
        """Returns the sample times for each sample point based on the 'chord' or
        'centripetal' method."""
        return self._sample_times

    @property
    def knot_vector(self):
        """Returns the knot vector generated from the averaging method of the sample
        point times."""
        return self._knot_vector

    @property
    def basis_matrix(self):
        """Returns the matrix of B-spline basis functions equaluated at sample point
        times."""
        return self._N

    @property
    def control_points(self):
        """Returns the B-spline control points that fit the sample point data."""
        return self._control_points
