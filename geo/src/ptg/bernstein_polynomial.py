# Copyright 2020 National Technology and Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
# certain rights in this software.


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


"""
Copyright 2023 Sandia National Laboratories

Notice: This computer software was prepared by National Technology and Engineering Solutions of
Sandia, LLC, hereinafter the Contractor, under Contract DE-NA0003525 with the Department of Energy
(DOE). All rights in the computer software are reserved by DOE on behalf of the United States
Government and the Contractor as provided in the Contract. You are authorized to use this computer
software for Governmental purposes but it is not to be released or distributed to the public.
NEITHER THE U.S. GOVERNMENT NOR THE CONTRACTOR MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR ASSUMES
ANY LIABILITY FOR THE USE OF THIS SOFTWARE. This notice including this sentence must appear on any
copies of this computer software. Export of this data may require a license from the United States
Government.
"""
