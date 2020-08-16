#!/usr/bin/env python3
# bernstein_polynomial.py
import math
import numpy as np


def bernstein_polynomial(i, p, nti):
    """ Computes the Bernstein polynomial coefficient for
    control point i with
    polynomial degreee p
    for a 1D parameter array t in interval [0, 1] broken into
    nti number of equidistance time intervals. """

    if i >= 0 and p >= 1 and nti >= 2 and i <= p:
        t = np.linspace(0, 1, nti+1)
        bp = math.factorial(p) / \
            (math.factorial(i) * math.factorial(p-i)) * t**i * (1-t)**(p-i)
        return bp
    else:
        print(f'Input (i, p, nti) = ({i}, {p}, {nti}) is out of range.')
        print('i is non-negative integer 0, 1, 2, ... p')
        print('p is integer >= 1')
        print('nti is integer >= 2')
        return None
