#!/usr/bin/env python3
# bspline_polynomial.py
import numpy as np


def bspline_polynomial(
    knot_vector: list, knot_k: int = 0, p: int = 0, nti: int = 1, verbose: bool = False
):
    """Computes the B-spline polynomial basis

    Args:
        knot_vector (float array): [t0, t1, t2, ... tK] of length (K+1), and K knot spans
            must have length of 2 or more
            must be a non-decreasing sequence
        knot_k (int): index in the list of possible knot_index values = [0, 1, 2, ... K]
        p (int): polynomial degree (p=0: constant, p=1: linear, p=2: quadratic, p=3: cubic, etc.)
        nti (int): number of time intervals for t in per knot span [t_k, t_{k+1}], nti = 1 is default
        verbose (bool): prints polynomial or error checking

    Returns:
        tuple: arrays of (t, f(t)) as time t and polynomial evaluated at t; or,
        AssertionError: if input is out of range
    """

    num_knots = len(knot_vector)
    MAX_DEGREE = 0

    try:
        assert len(knot_vector) >= 2, "Error: knot vector length must be two or larger."
        assert knot_k >= 0, "Error: knot index knot_k must be non-negative."
        assert p >= 0, "Error: polynomial degree p must be non-negative."
        assert (
            p <= MAX_DEGREE
        ), f"Error: polynomial degree p exceeds maximum of {MAX_DEGREE}"
        assert nti >= 1, "Error: number of time intervals nti must be 1 or greater."
        assert knot_k <= (
            num_knots - 1
        ), "Error: knot index knot_k exceeds knot vector length minus 1."

        num_knots_k_to_end = len(knot_vector[knot_k:])
        assert (
            num_knots_k_to_end >= p + 1
        ), "Error, insufficient remaining knots for local support."

        knots_lhs = knot_vector[0:-1]  # left-hand-side knot values
        knots_rhs = knot_vector[1:]  # right-hand-side knot values
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
        t.append(knot_vector[-1])
        t = np.array(t)

        y = np.zeros((num_knots - 1) * nti + 1)

        if verbose:
            print(f"Knot vector: {knot_vector}")
            print(f"Number of knots = {num_knots}")
            print(f"Knot index: {knot_k}")
            print(f"Left-hand-side knot vector values: {knots_lhs}")
            print(f"Right-hand-side knot vector values: {knots_rhs}")
            print(f"Knot spans: {knot_spans}")
            print(f"Number of time intervals per knot span: {nti}")
            print(f"Knot span deltas: {dt}")

        if p == 0:
            y[knot_k * nti : knot_k * nti + nti] = 1.0
            if verbose:
                print(f"t = {t}")
                print(f"y = {y}")

        return t, y
        # else:
        #     print("Not implemented for p>0.")
        #     return None

    except AssertionError as error:
        if verbose:
            print(error)

        return error

    # if knot_k >= 0 and knot_k <= (num_knots - 1) and p >= 0 and nti >= 1:
    #     knots_lhs = knot_vector[0:-1]  # left-hand-side knot values
    #     knots_rhs = knot_vector[1:]  # right-hand-side knot values
    #     knot_spans = np.array(knots_rhs) - np.array(knots_lhs)
    #     dt = knot_spans / nti

    #     # improve index notation
    #     # t = [knots_lhs[i] + k * dt[i] for i in np.arange(num_knots-1) for k in np.arange(nti)]
    #     t = [
    #         knots_lhs[k] + j * dt[k]
    #         for k in np.arange(num_knots - 1)
    #         for j in np.arange(nti)
    #     ]
    #     t.append(knot_vector[-1])
    #     t = np.array(t)

    #     y = np.zeros((num_knots - 1) * nti + 1)

    #     if verbose:
    #         print(f"Knot vector: {knot_vector}")
    #         print(f"Number of knots = {num_knots}")
    #         print(f"Knot index: {knot_k}")
    #         print(f"Left-hand-side knot vector values: {knots_lhs}")
    #         print(f"Right-hand-side knot vector values: {knots_rhs}")
    #         print(f"Knot spans: {knot_spans}")
    #         print(f"Number of time intervals per knot span: {nti}")
    #         print(f"Knot span deltas: {dt}")

    #     if p == 0:
    #         y[knot_k * nti : knot_k * nti + nti] = 1.0
    #         if verbose:
    #             print(f"t = {t}")
    #             print(f"y = {y}")
    #         return t, y
    #     else:
    #         print("Not implemented for p>0.")
    #         return None

    # else:
    #     if verbose:
    #         print("Input is out of range.")
    #         print("Knot index i must be:")
    #         print("  non-negative, and be")
    #         print("  less than index of last knot vector.")
    #         print("Polynomial degree p must be a non-negative integer.")
    #         print("Number of time intervals nti >= 2.")

    #     return None
