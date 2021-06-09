"""This module creates a sequence of Bezier curves from 3D control points.
The Bezier bases are recovered from the B-spline bases.

Example:
> cd ~/sibl/geo/src/ptg
> conda activate siblenv
> python view_bezier_recovery.py --help
> python view_bezier_recovery.py
"""
import argparse

# import os
import sys
from typing import NamedTuple, Tuple, Union

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


def main(argv):
    filename = __file__
    print(f"This is file '{filename}'")

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v", "--verbose", help="increase output verbosity", action="store_true"
    )

    parser.add_argument(
        "input",
        help="fully pathed location to the points.csv input data",
    )

    args = parser.parse_args()

    p = Path(args.input).resolve()

    db = Database(name=p.name, type=p.suffix, path=str(p.parent))

    points = data_from_input(db)

    if args.verbose:
        print("verbosity turned on")


if __name__ == "__main__":
    main(sys.argv[1:])
