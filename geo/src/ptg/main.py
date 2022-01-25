"""This module runs the SIBL Mesh Engine from the command line.

Example:
> conda activate siblenv
> cd ~/sibl
> python geo/src/ptg/main.py -i path_to_file/input_template.yml
"""

import argparse
from pathlib import Path
import sys

# from types import SimpleNamespace
# from typing import NamedTuple
from collections import namedtuple

import numpy as np

from ptg import reader as reader
import xybind as xyb


def main(argv):

    print("SIBL Mesh Engine initialized.")
    print(f"driver: {__file__}")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_file",
        "-i",
        action="store",
        required=True,
        help="input file in yml format",
    )

    args = parser.parse_args()

    input_path = args.input_file

    r = reader.Reader(input_file=input_path)
    database = r.database
    print(f"The database is {database}")

    # for key, value in db.items():
    #     print(f"key: {key}, value: {value} of value type: {type(value)}")

    # c = {"r": 50, "g": 205, "b": 50, "alpha": 0.5}
    # Color = namedtuple("Color", c)
    # Color(**c)

    # yml = SimpleNamespace(**db)
    TupleDatabase = namedtuple("TupleDatabase", database)
    db = TupleDatabase(**database)

    assert db.version == 1.1

    print(f"Reading in boundary file: {db.boundary}")
    path_file_in = Path(db.boundary).expanduser()
    if not path_file_in.is_file():
        raise OSError(f"File not found: {path_file_in}")

    n_header_rows_skipped, n_footer_rows_skipped = 1, 0
    ix, iy = 0, 1
    boundary = np.genfromtxt(
        path_file_in,
        dtype="float",
        skip_header=n_header_rows_skipped,
        skip_footer=n_footer_rows_skipped,
        usecols=(ix, iy),
    )

    xs, ys = boundary[:, ix], boundary[:, iy]

    mesh = xyb.QuadMesh(xs, ys)

    mesh.compute(resolution=db.resolution)

    print("SIBL Mesh Engine completed.")


if __name__ == "__main__":
    main(sys.argv[1:])
