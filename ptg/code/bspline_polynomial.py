#!/usr/bin/env python3
# bspline_polynomial.py
import numpy as np


def bspline_polynomial(i, knot_vector, p, nti, verbose=True):
    """ Computes the B-spline polynomial for 
    knot vector index i = [0, 1, 2, ... k]
    polynomial degree p
    for a 1D parameter array t in interval
    [t0, t1, t2, ... tk].
    """

    num_knots = len(knot_vector)

    if i >= 0 and i <= (num_knots - 1) and p >= 0 and nti >= 2:
        knots_lhs = knot_vector[0:-1]  # left-hand-side knot values
        knots_rhs = knot_vector[1:]  # right-hand-side knot values
        knot_spans = np.array(knots_rhs) - np.array(knots_lhs)
        dt = knot_spans / nti
        t = [knots_lhs[i] + k * dt[i] for i in np.arange(num_knots-1) for k in np.arange(nti)]

        if verbose:
            print(f"Knot vector: {knot_vector}")
            print(f"Number of knots = {num_knots}")
            print(f"Left-hand-side knot values: {knots_lhs}")
            print(f"Right-hand-side knot values: {knots_rhs}")
            print(f"Knot spans: {knot_spans}")
            print(f"Number of time intervals: {nti}")
            print(f"Knot span deltas: {dt}")
            print(f"t = {t}")

    else:
        print("Input is out of range.")
        print("Knot index i must be:")
        print("  non-negative, and be")
        print("  less than index of last knot vector.")
        print("Polynomial degree p must be a non-negative integer.")
        print("Number of time intervals nti >= 2.")
