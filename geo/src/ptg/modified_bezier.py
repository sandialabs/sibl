# Copyright 2020 National Technology and Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
# certain rights in this software.


"""This module creates a sequence of modified Bezier curves from 3D control points.
The modified Bezier bases are derived from the periodic B-spline bases.

Example:
> cd ~/sibl/geo/src/ptg
> conda activate siblenv
> python modified_bezier.py --help
> python modified_bezier.py ../../data/bezier/circle-points.csv --verbose --degree 1 --bisections 1
This is file 'modified_bezier.py'
verbosity turned on
processing input file: /Users/sparta/sibl/geo/data/bezier/circle-points.csv
number of elements: 8
"""
import argparse

# import os
import sys
from typing import NamedTuple, Tuple

import numpy as np
from pathlib import Path  # stop using os.path, use pathlib instead


class Database(NamedTuple):
    name: str  # = "filename.csv"
    type: str  # = ".csv"
    path: str  # = "/path/to/some/location"


class TripleSeries(NamedTuple):
    x: Tuple  # = (0.0,)
    y: Tuple  # = (0.0,)
    z: Tuple  # = (0.0,)


def data_from_input(db: Database) -> TripleSeries:

    path_name = Path.joinpath(Path(db.path), db.name)

    data = np.genfromtxt(
        path_name, dtype="float", delimiter=",", skip_header=1, usecols=(0, 1, 2)
    )
    return TripleSeries(x=tuple(data[:, 0]), y=tuple(data[:, 1]), z=tuple(data[:, 2]))


def periodic_control_points(*, cpts: TripleSeries, degree: int) -> TripleSeries:
    # repeat the first control point as the new last control point
    # return TripleSeries(
    #     x=cpts.x + tuple([cpts.x[0]]),
    #     y=cpts.y + tuple([cpts.y[0]]),
    #     z=cpts.z + tuple([cpts.z[0]]),
    # )

    # similar to an open b-spline with repeated knots, here we actual repeat the
    # control points
    # return TripleSeries(
    #     x=tuple([cpts.x[-degree]]) + cpts.x + cpts.x[0:degree],
    #     y=tuple([cpts.y[-degree]]) + cpts.y + cpts.y[0:degree],
    #     z=tuple([cpts.z[-degree]]) + cpts.z + cpts.z[0:degree],
    # )

    # similar to an open b-spline with repeated knots, here we actual repeat the
    # control points at the end of the original control points
    return TripleSeries(
        x=cpts.x + cpts.x[0:degree],
        y=cpts.y + cpts.y[0:degree],
        z=cpts.z + cpts.z[0:degree],
    )


def modified_bezier(
    *, control_points_file: str, verbose: bool, degree: int, n_bisections: int
) -> Tuple:
    """Creates a periodic modified Bezier curve evaluated between 0 and 1.

    Args:
        control_points_file (string): A fully pathed text file that contains a
            comma-separated list of 3D control points.
            For example, 'home/chovey/documents/points.csv' might contain three points:
                # some comment, the first line of the .csv file is ignored
                1.0, 0.0, 0.0
                1.0, 1.0, 0.0
                0.0, 1.0, 0.0
        verbose (bool): prints additional information to the command line
        degree (int): Bezier polynomial degree, currently limited to 1 or 2.
        n_bisections (int): number bisections of parameter t interval [0, 1].
            For example
            n_bisections = 1 gives t = [0.0, 0.5, 1.0]
            n_bisections = 2 gives t = [0.0, 0.25, 0.5, 0.75, 1.0]
            ... and so on
            Intervals are equidistant.  n_bisections must be greater or equal to 1.

    Raises:
        ValueError: If `degree` does not equal 1 or 2.
        ValueError: If `n_bisections` < 1.
    """

    if verbose:
        print("verbosity turned on")

    # assert degree in (1, 2), "Must be 1 or 2."
    if degree not in (1, 2):
        raise ValueError("Error: Degree must be 1 or 2.")

    # assert n_bisections >= 1, "Number of bisections must be >= 1."
    if n_bisections < 1:
        raise ValueError("Error: Number of bisections must be >= 1.")

    p = Path(control_points_file).resolve()
    if verbose:
        print(f"processing input file: {p}")

    db = Database(name=p.name, type=p.suffix, path=str(p.parent))

    control_points = data_from_input(db)

    assert len(control_points.x) == len(control_points.y) == len(control_points.z)
    assert len(control_points.x) % 2 == 0, "Number of control points must be even."
    assert len(control_points.x) >= 4, "Number of control points must be >= 4."

    num_elements = len(control_points.x)
    if verbose:
        print(f"number of elements: {num_elements}")

    # control_points_closed = close_control_points(control_points)
    control_points_periodic = periodic_control_points(
        cpts=control_points, degree=degree
    )

    t_min, t_max = 0, 1
    n_intervals = 2**n_bisections + 1
    t = np.linspace(t_min, t_max, n_intervals)

    if degree == 1:
        N0 = np.array(tuple(map(lambda t: (1.0 - t), t)))
        N1 = np.array(tuple(map(lambda t: t, t)))

        eval_x = tuple(
            map(
                lambda x0, x1: tuple(N0 * x0 + N1 * x1),
                control_points.x,
                control_points_periodic.x[1:],
            )
        )
        eval_y = tuple(
            map(
                lambda y0, y1: tuple(N0 * y0 + N1 * y1),
                control_points.y,
                control_points_periodic.y[1:],
            )
        )
        eval_z = tuple(
            map(
                lambda z0, z1: tuple(N0 * z0 + N1 * z1),
                control_points.z,
                control_points_periodic.z[1:],
            )
        )

    else:  # args.degree = 2
        # These are not the normal B-spline basis functions.  Rather, they are the
        # periodic modified quadratic Bezier basis functions.
        N0 = np.array(tuple(map(lambda t: 0.5 * (1.0 - t) ** 2, t)))  # $\hat{N}_0$
        N1 = np.array(
            tuple(
                map(lambda t: 0.5 * (1.0 - t) ** 2 + 2 * (1.0 - t) * t + 0.5 * t**2, t)
            )
        )  # $\hat{N}_1$
        N2 = np.array(tuple(map(lambda t: 0.5 * t**2, t)))  # $\hat{N}_2$

        eval_x = tuple(
            map(
                lambda x0, x1, x2: tuple(N0 * x0 + N1 * x1 + N2 * x2),
                # control_points.x[::degree],
                control_points.x,
                # control_points.x[1:][::degree],
                control_points_periodic.x[1:],
                # control_points_periodic.x[2:][::degree],
                control_points_periodic.x[2:],
            )
        )

        eval_y = tuple(
            map(
                lambda y0, y1, y2: tuple(N0 * y0 + N1 * y1 + N2 * y2),
                # control_points.y[::degree],
                control_points.y,
                # control_points.y[1:][::degree],
                control_points_periodic.y[1:],
                # control_points_periodic.y[2:][::degree],
                control_points_periodic.y[2:],
            )
        )

        eval_z = tuple(
            map(
                lambda z0, z1, z2: tuple(N0 * z0 + N1 * z1 + N2 * z2),
                # control_points.z[::degree],
                control_points.z,
                # control_points.z[1:][::degree],
                control_points_periodic.z[1:],
                # control_points_periodic.z[2:][::degree],
                control_points_periodic.z[2:],
            )
        )

    return eval_x, eval_y, eval_z


def main(argv):
    filename = __file__
    print(f"This is file '{filename}'")

    # reference: https://www.golinuxcloud.com/python-argparse/
    parser = argparse.ArgumentParser()

    # verbosity
    parser.add_argument(
        "-v", "--verbose", help="increase output verbosity", action="store_true"
    )

    parser.add_argument(
        "-d",
        "--degree",
        default=1,
        dest="degree",
        help="polynomial degree, integer in [1, 2], defaults to 1",
        type=int,
    )

    parser.add_argument(
        "-b",
        "--bisections",
        default=1,
        dest="n_bisections",
        help="number of bisections of parameter interval, integer in [1, 2, ...), defaults to 1",
        type=int,
    )

    # client data input
    parser.add_argument(
        "control_points_file",
        help="fully pathed location to the control points .csv file",
    )

    args = parser.parse_args()

    return modified_bezier(
        control_points_file=args.control_points_file,
        verbose=args.verbose,
        degree=args.degree,
        n_bisections=args.n_bisections,
    )


if __name__ == "__main__":
    _ = main(sys.argv[1:])


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
