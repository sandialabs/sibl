# bernstein_polynomial.py
import math
import numpy as np


def bernstein_polynomial(i: int, p: int, nti: int = 2, verbose: bool = False):
    """Computes the Bernstein polynomial

    Args:
        i (int): control point, i >= 0 and i <=p
        p (int): polynomial degree, p >= 1
        nti (int): number of time intervals for t in [0, 1]
            intervals are equidistant
            nti = 2 is default => t = [0.0, 0.5, 1.0]
            nti >=2
        verbose (bool): prints polynomial or error checking

    Returns:
        array: of floats, the polynomial evaluated at t values.
    """

    if i >= 0 and p >= 1 and nti >= 2 and i <= p:
        t = np.linspace(0, 1, nti + 1)
        bp = (
            math.factorial(p)
            / (math.factorial(i) * math.factorial(p - i))
            * t**i
            * (1 - t) ** (p - i)
        )
        if verbose:
            print(f"Bernstein polynomial = {bp}")

        return bp

    else:
        if verbose:
            print(f"Input (i, p, nti) = ({i}, {p}, {nti}) is out of range.")
            print("i is non-negative integer 0, 1, 2, ... p")
            print("p is integer >= 1")
            print("nti is integer >= 2")

        return None
