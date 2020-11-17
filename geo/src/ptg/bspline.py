from scipy.interpolate import BSpline as scipy_bspline


class BSpline:
    def __init__(
        self,
        knot_vector: list,
        coefficients: list,
        degree: int = 0,
        verbose: bool = False,
    ):
        """Creates a B-Spline curve or its derivatives.

        Args:
            knot_vector (float array): [t0, t1, t2, ... tK]
                len(knot_vector) = len(coef) + (degree + 1)
                (K+1) knots, K knot spans
                must have length of two or more
                must be a non-decreasing sequence
            coefficients (float array):
                spline coefficients [c0, c1, c2, ... cn]
            degree (int >= 0) : B-spline polynomial degree
            verbose (bool): prints extended error checking, default False
        """
        self.kv = knot_vector
        self.c = coefficients
        self.p = degree
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
        """Evaluate the BSpline at all points `t`."""

        # y = np.nan_to_num(self._bspline(t), nan=0.0)
        # y = self._bspline(t)
        # return y
        return self._bspline(t)
