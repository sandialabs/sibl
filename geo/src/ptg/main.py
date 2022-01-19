"""This module runs the SIBL Mesh Engine from the command line.

Example:
> conda activate siblenv
> cd ~/sibl
> python geo/src/ptg/main.py -i path_to_file/input_template.yml
"""

import argparse
from pathlib import Path
import sys
from types import SimpleNamespace

import numpy as np

from ptg import reader as reader


def main(argv):

    print("SIBL Mesh Engine initialized.")
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
    db = r.database
    print(f"The database is {db}")

    # for key, value in db.items():
    #     print(f"key: {key}, value: {value} of value type: {type(value)}")

    yml = SimpleNamespace(**db)

    assert yml.version == 1.1

    print(f"Reading in boundary file: {yml.boundary}")
    path_file_in = Path(yml.boundary).expanduser()
    if not path_file_in.is_file():
        raise OSError(f"File not found: {path_file_in}")

    n_header_rows_skipped, n_footer_rows_skipped = 1, 0
    ix, iy = 0, 1
    boundary = np.genfromtxt(
        path_file_in,
        dtype="float",
        delimiter="    ",
        skip_header=n_header_rows_skipped,
        skip_footer=n_footer_rows_skipped,
        usecols=(ix, iy),
    )

    print("SIBL Mesh Engine completed.")


if __name__ == "__main__":
    main(sys.argv[1:])
