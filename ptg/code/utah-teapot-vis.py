# utah teapot visualization
import argparse
import csv
import json
from pathlib import Path
import sys

import numpy as np

# functional programming, named tuple, Dan Bader, Real Python
# https://realpython.com/lessons/immutable-data-structures-namedtuple/
# import collections

# csv file to namedtuple
# https://stackoverflow.com/questions/9007174/what-is-the-pythonic-way-to-read-csv-file-data-as-rows-of-namedtuples


# from collections import namedtuple

# input file begin
# file_control_points = 'utah-teapot-coordinates.csv'
# data_type_string = 'float'
# data_type_delimiter = ','
# n_headers = 0  # no headers in the file_control_points csv file
# 
# # input file end
# 
# # visualize control points
# 
# # tea pot bottom
# 
# # named tuple, a named tuple instance is immutable
# # ControlPoint = collections.namedtuple('ControlPoint', ['x', 'y', 'z'])
# # ControlPoint = namedtuple('ControlPoint', ['x', 'y', 'z'])
# 
# control_points_list = []  # this feel wrong b/c it is mutable
# 
# with open(file_control_points, mode='rt') as fin:
#     reader = csv.reader(fin)
#     # ControlPoint = namedtuple("ControlPoint", next(reader))
#     ControlPoint = namedtuple("ControlPoint", ['x', 'y', 'z'])
#     for data in map(ControlPoint._make, reader):
#         print(data.x)
#         control_points_list.append(ControlPoint)
# 
# 
# control_points = tuple(control_points_list)
# 
# a = 4

# with open(file_control_points) as fin:
#     data = np.genfromtxt(file_control_points,
#                          dtype=data_type_string,
#                          delimiter=data_type_delimiter, 
#                          skip_header=n_headers)

# tea pot original (without bottom)

# label control points

# visualize low-frequency Bezier surface

# visualize high-frequency Bezier surface

class BezierSurfaceVis:

    def __init__(self, config, verbose=0):

        if not Path(config).is_file():
            sys.exit(f'Error: cannot fine file {config}')

        config_location = Path(config).parent

        if verbose:
            print(f'\nBezierSolid processing config file: {config}')
            print(f'located at: {config_location}')

        with open(config) as fin:
            db = json.load(fin)

        config_schema = ["data-path", "control-points", "connections"]

        # check .json input schema
        for kw in config_schema:
            key = db.get(kw, None)
            if not key:
                sys.exit(f'Error: keyword "{kw}" not found in config file.')

        # data_path = db.get("data-path", None)
        # if not data_path:
        #     sys.exit('Error: no data path specified.')

        # cp_file = db.get("control-points", None)
        # if not cp_file:
        #     sys.exit('Error: no control points file specified.')

        # co_file = db.get("connections", None)
        # if not co_file:
        #     sys.exit('Error: no connections file specified.')

        data_path = db.get("data-path", None)
        cp_file = db.get("control-points", None)
        co_file = db.get("connections", None)

        if not Path(data_path).is_dir():
            sys.exit(f'Error: cannot find {data_path}')

        cp_path_file = data_path + cp_file
        if not Path(cp_path_file).is_file():
            sys.exit(f'Error: cannot find {cp_path_file}')

        co_path_file = data_path + co_file
        if not Path(co_path_file).is_file():
            sys.exit(f'Error: cannot find {co_path_file}')

        data_type_string = 'float'
        data_type_int = 'i8'
        data_type_delimiter = ','
        n_headers = 0  # no headers in the csv files

        # cp_x, cp_y, cp_z = (None, None, None)
        idx, idy, idz = (0, 1, 2)  # column numbers from .csv file

        with open(cp_path_file) as fin:
            data = np.genfromtxt(cp_path_file,
                                 dtype=data_type_string,
                                 delimiter=data_type_delimiter,
                                 skip_header=n_headers)
            cp_x = data[:, idx]
            cp_y = data[:, idy]
            cp_z = data[:, idz]

        with open(co_path_file) as fin:
            patches = np.genfromtxt(co_path_file,
                                    dtype=data_type_int,
                                    delimiter=data_type_delimiter,
                                    skip_header=n_headers)

        a = 4



def main(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument("config_file", help=".json 3D solid specification")

    parser.add_argument("--verbose",
                        help="increased command line feedback",
                        action="store_true")

    args = parser.parse_args()

    config = args.config_file
    verbose = args.verbose

    BezierSurfaceVis(config, verbose)


if __name__ == '__main__':
    main(sys.argv[1:])
