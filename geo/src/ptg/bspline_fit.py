# from numpy.typing import ArrayLike
from typing import Union, List, Tuple
from numpy import ndarray


class BSplineFit:
    def __init__(
        self,
        sample_points: Union[List[float], Tuple[float], ndarray],
        degree: int = 0,
        verbose: bool = False,
        **kwargs
    ):
        """Creates a B-Spline curve based on fits to sample_points on curve.

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
        """
        if not isinstance(sample_points, (list, tuple, ndarray)):
            raise TypeError("Error: sample points must be a list, tuple, or ndarray.")
        self.samples = sample_points

        # assert degree >= 0, "Error: degree must be non-negative."
        if degree < 0:
            raise ValueError("Error: degree must be non-negative.")
        self.p = degree

        self.verbose = verbose
        self.valid = False
        self._bspline = None
        self._sample_time_method = kwargs.get("sample_time_method", "chord")
        assert self._sample_time_method in ("chord", "centripetal")

    @property
    def knot_vector(self):
        """Gets the knot vector used to create the BSpline fit to sample points."""
        pass

    def sample_times(self):
        """Creates the sample times for each sample point based on the 'chord' or
        'centripetal' method."""
        pass
