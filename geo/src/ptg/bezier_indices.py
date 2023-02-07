# Copyright 2020 National Technology and Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
# certain rights in this software.


# Type hints:
# https://docs.python.org/3/library/typing.html
from typing import Tuple

# number of time intervals in along a Bezier axis
interpolations = ("constant", "linear", "quadratic", "cubic")
VERBOSE = True  # show/hide command line interaction

# manual development of the tuple indices, used to later define the
# method knot_indices(...)

for p, kw in enumerate(interpolations):
    if VERBOSE:
        print(f"\ndegree p = {p}")
        print(f"  interpolation: {kw}")

    if p < 1:
        if VERBOSE:
            print("  no indices for constant")

    else:
        knots = range(p + 1)
        # print(f"  knots = {knots}")
        indices = tuple(i for i in knots)
        if VERBOSE:
            print(f"  knots = {knots}")
            print("  1D case:")
            print(f"    indices = {indices}")
            print(f"    number of knots = {len(indices)}")

        indices = tuple((i, j) for i in knots for j in knots)
        if VERBOSE:
            print("  2D case:")
            print(f"    indices = {indices}")
            print(f"    number of knots = {len(indices)}")

        indices = tuple((i, j, k) for i in knots for j in knots for k in knots)
        if VERBOSE:
            print("  3D case:")
            print(f"    indices = {indices}")
            print(f"    number of knots = {len(indices)}")


def knot_indices(degree: int = 1, dimension: int = 1) -> Tuple:
    p = degree
    if p >= 1 and p <= 3 and dimension >= 1 and dimension <= 3:
        if dimension == 1:
            indices = tuple(i for i in range(p + 1))

        elif dimension == 2:
            indices = tuple((i, j) for i in range(p + 1) for j in range(p + 1))

        else:  # dimension must == 3
            indices = tuple(
                (i, j, k)
                for i in range(p + 1)
                for j in range(p + 1)
                for k in range(p + 1)
            )

        return indices

    else:
        if VERBOSE:
            print("Input is out of range:")
            print(f"  (degree, dimension) = ({degree}, {dimension})")
            print("  degree (int) can be 1 (linear), 2 (quadratic), or 3 (cubic)")
            print("  dimension (int) can be 1 (1D), 2 (2D) or 3 (3D)")

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
