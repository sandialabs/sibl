"""This module runs the SIBL Mesh Engine from the command line.

Example:
> conda activate siblenv
> cd ~/sibl
> python geo/src/ptg/main.py -i path_to_file/imput_template.yml
"""

import argparse
import sys

# import yaml

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
    print("SIBL Mesh Engine completed.")


if __name__ == "__main__":
    main(sys.argv[1:])
