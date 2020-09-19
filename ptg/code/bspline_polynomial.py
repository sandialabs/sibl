#!/usr/bin/env python3
# bspline_polynomial.py
import numpy as np


def bspline_polynomial(knot_vector : list, knot_k : int, p=0, nti=2, verbose=True):
    """ Given the knot_vector = [t0, t1, t2, ... tK] of length (K+1)
    and the index knot_k in the knot_index = [0, 1, 2, ... K],
    computes the B-spline polynomial basis of degree p,
    (p=0: constant, p=1: linear, p=2: quadratic, p=3: cubic, etc.)
    as a function of parameter t (quasi-time) for t in [t0, tK], with
    at nti (number of time intervals) per knot span.
    """

    num_knots = len(knot_vector)

    if knot_k >= 0 and knot_k <= (num_knots - 1) and p >= 0 and nti >= 2:
        knots_lhs = knot_vector[0:-1]  # left-hand-side knot values
        knots_rhs = knot_vector[1:]  # right-hand-side knot values
        knot_spans = np.array(knots_rhs) - np.array(knots_lhs)
        dt = knot_spans / nti

        # improve index notation
        # t = [knots_lhs[i] + k * dt[i] for i in np.arange(num_knots-1) for k in np.arange(nti)]
        t = [knots_lhs[k] + j * dt[k] for k in np.arange(num_knots-1) for j in np.arange(nti)]
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
        else:
            print("Not implemented for p>0.")

    else:
        print("Input is out of range.")
        print("Knot index i must be:")
        print("  non-negative, and be")
        print("  less than index of last knot vector.")
        print("Polynomial degree p must be a non-negative integer.")
        print("Number of time intervals nti >= 2.")
