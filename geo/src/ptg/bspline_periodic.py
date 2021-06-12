"""This module creates a sequence of modified Bezier curves from 3D control points.
The modified Bezier bases are recovered from the periodic B-spline bases.

Example:
> cd ~/sibl/geo/src/ptg
> conda activate siblenv
> python bspline_periodic.py --help
> python bspline_periodic.py
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


# def close_control_points(cpts: TripleSeries) -> TripleSeries:
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


def bspline_periodic(
    *, control_points_file: str, verbose: bool, degree: int, n_bisections: int
):

    if verbose:
        print("verbosity turned on")

    assert degree in (1, 2), "Must be 1 or 2."

    assert n_bisections >= 1, "Number of bisections must be >= 1."

    p = Path(control_points_file).resolve()
    if verbose:
        print(f"processing input file: {p}")

    db = Database(name=p.name, type=p.suffix, path=str(p.parent))

    control_points = data_from_input(db)

    # For periodic (non-open) linear (p=1) bases, number of valid controls points,
    # assuming the first control point is repeated by this script as also the last
    # control point, is (num_control_points, number_elements):
    # (4, 4) a quad-shape
    # (6, 6) a hex-shape
    # (8, 8) an oct-shape, etc.

    # For periodic (non-open) quadratic (p=2) bases, number of valid controls points,
    # assuming the first control point is repeated by this script as also the last
    # control point, is (num_control_points, number_elements):
    # (4, 2) a snap-back curve
    # (6, 3) a tri-shape
    # (8, 4) a quad-shape
    # (10, 5) a penta-shape
    # (12, 6) a hex-shape, etc.
    assert len(control_points.x) == len(control_points.y) == len(control_points.z)
    assert len(control_points.x) % 2 == 0, "Number of control points must be even."
    assert len(control_points.x) >= 4, "Number of control points must be >= 4."

    num_elements = int(len(control_points.x) / degree)
    if verbose:
        print(f"number of elements: {num_elements}")

    # control_points_closed = close_control_points(control_points)
    control_points_periodic = periodic_control_points(
        cpts=control_points, degree=degree
    )

    t_min, t_max = 0, 1
    n_intervals = 2 ** n_bisections + 1
    # t = np.linspace(0, 1, 2 ** n_bisections + 1)
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
        # periodic modified quadratic Bezier basis functions
        N0 = np.array(tuple(map(lambda t: 0.5 * (1.0 - t) ** 2, t)))  # $\hat{N}_0$
        N1 = np.array(
            tuple(
                map(
                    lambda t: 0.5 * (1.0 - t) ** 2 + 2 * (1.0 - t) * t + 0.5 * t ** 2, t
                )
            )
        )  # $\hat{N}_1$
        N2 = np.array(tuple(map(lambda t: 0.5 * t ** 2, t)))  # $\hat{N}_2$

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

    a = 4

    return (eval_x, eval_y, eval_z)


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

    return bspline_periodic(
        control_points_file=args.control_points_file,
        verbose=args.verbose,
        degree=args.degree,
        n_bisections=args.n_bisections,
    )


if __name__ == "__main__":
    _ = main(sys.argv[1:])
