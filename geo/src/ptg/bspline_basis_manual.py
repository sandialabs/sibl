# bspline_polynomial.py
import numpy as np


def bspline_basis_manual(
    kv: list, knot_i: int = 0, p: int = 0, nti: int = 1, verbose: bool = False
):
    """Computes the B-spline polynomial basis

    Args:
        kv (float array): knot vector [t0, t1, t2, ... tK]
            of length (K+1), and K knot spans
            must have length of 2 or more
            must be a non-decreasing sequence
        knot_i (int): index in the list of possible knot_index values = [0, 1, 2, ... K]
        p (int): polynomial degree (p=0: constant, p=1: linear, p=2: quadratic, p=3: cubic, etc.)
            currently limited to p = [0, 1, 2].
        nti (int): number of time intervals for t in per knot span [t_k, t_{k+1}], nti = 1 is default
        verbose (bool): prints polynomial or error checking

    Returns:
        tuple: arrays of (t, f(t)) as time t and polynomial evaluated at t; or,
        AssertionError: if input is out of range
    """

    num_knots = len(kv)
    MAX_DEGREE = 2

    try:
        assert len(kv) >= 2, "Error: knot vector length must be two or larger."
        assert knot_i >= 0, "Error: knot index knot_i must be non-negative."
        assert p >= 0, "Error: polynomial degree p must be non-negative."
        assert (
            p <= MAX_DEGREE
        ), f"Error: polynomial degree p exceeds maximum of {MAX_DEGREE}"
        assert nti >= 1, "Error: number of time intervals nti must be 1 or greater."
        assert knot_i <= (
            num_knots - 1
        ), "Error: knot index knot_i exceeds knot vector length minus 1."

        num_knots_k_to_end = len(kv[knot_i:])
        assert (
            num_knots_k_to_end >= p + 1
        ), "Error, insufficient remaining knots for local support."

        knots_lhs = kv[0:-1]  # left-hand-side knot values
        knots_rhs = kv[1:]  # right-hand-side knot values
        knot_spans = np.array(knots_rhs) - np.array(knots_lhs)
        dt = knot_spans / nti
        assert all([dti >= 0 for dti in dt]), "Error: knot vector is decreasing."

        # improve index notation
        # t = [knots_lhs[i] + k * dt[i] for i in np.arange(num_knots-1) for k in np.arange(nti)]
        t = [
            knots_lhs[k] + j * dt[k]
            for k in np.arange(num_knots - 1)
            for j in np.arange(nti)
        ]
        t.append(kv[-1])
        t = np.array(t)

        # y = np.zeros((num_knots - 1) * nti + 1)
        y = np.zeros(len(t))

        if verbose:
            print(f"Knot vector: {kv}")
            print(f"Number of knots = {num_knots}")
            print(f"Knot index: {knot_i}")
            print(f"Left-hand-side knot vector values: {knots_lhs}")
            print(f"Right-hand-side knot vector values: {knots_rhs}")
            print(f"Knot spans: {knot_spans}")
            print(f"Number of time intervals per knot span: {nti}")
            print(f"Knot span deltas: {dt}")

        if p == 0:
            y[knot_i * nti : knot_i * nti + nti] = 1.0
            if verbose:
                print(f"t = {t}")
                print(f"y = {y}")

        if p == 1:
            for (eix, te) in enumerate(t):  # e for evaluations, ix for index
                if te >= kv[knot_i] and te < kv[knot_i + 1]:
                    y[eix] = (te - kv[knot_i]) / (kv[knot_i + 1] - kv[knot_i])
                elif te >= kv[knot_i + 1] and te < kv[knot_i + 2]:
                    y[eix] = (kv[knot_i + 2] - te) / (kv[knot_i + 2] - kv[knot_i + 1])

        if p == 2:
            for (eix, te) in enumerate(t):  # e for evaluations, ix for index
                if te >= kv[knot_i] and te < kv[knot_i + 1]:

                    a_1 = (te - kv[knot_i]) / (kv[knot_i + 2] - kv[knot_i])
                    a_2 = (te - kv[knot_i]) / (kv[knot_i + 1] - kv[knot_i])
                    y[eix] = a_1 * a_2

                elif te >= kv[knot_i + 1] and te < kv[knot_i + 2]:

                    b_1 = (te - kv[knot_i]) / (kv[knot_i + 2] - kv[knot_i])
                    b_2 = (kv[knot_i + 2] - te) / (kv[knot_i + 2] - kv[knot_i + 1])
                    b_3 = (kv[knot_i + 3] - te) / (kv[knot_i + 3] - kv[knot_i + 1])
                    b_4 = (te - kv[knot_i + 1]) / (kv[knot_i + 2] - kv[knot_i + 1])
                    y[eix] = (b_1 * b_2) + (b_3 * b_4)

                elif te >= kv[knot_i + 2] and te < kv[knot_i + 3]:

                    c_1 = (kv[knot_i + 3] - te) / (kv[knot_i + 3] - kv[knot_i + 1])
                    c_2 = (kv[knot_i + 3] - te) / (kv[knot_i + 3] - kv[knot_i + 2])
                    y[eix] = c_1 * c_2

        return t, y
        # else:
        #     print("Not implemented for p>0.")
        #     return None

    except AssertionError as error:
        if verbose:
            print(error)

        return error
