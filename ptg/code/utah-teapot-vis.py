# utah teapot visualization
import argparse
import json
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np


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

        ax = plt.axes(projection='3d')
        # ax.plot3D(cp_x, cp_y, cp_z)
        ax.scatter3D(cp_x, cp_y, cp_z)

        # for patch in patches:
        # patch number, description
        # 0, rim
        # 1, body
        # 2, body continued
        # 3, lid
        # 4, lid continued
        # 5, handle
        # 6, handle continued
        # 7, spout
        # 8, spout continued
        # 9, bottom
        cp_labels = True  # show/hide control point index
        # patch_number = 6
        # for patch in [patches[patch_number]]:
        patch_numbers = (5, 6)
        for patch in [patches[k] for k in patch_numbers]:
            patch_x = [cp_x[i] for i in patch]
            patch_y = [cp_y[i] for i in patch]
            patch_z = [cp_z[i] for i in patch]
            ax.plot3D(patch_x, patch_y, patch_z, linestyle='dashed')

            if cp_labels:
                for i, cp_index in enumerate(patch):
                    if verbose:
                        print(f'patch node {i} is control point {cp_index}')
                    ax.text(patch_x[i], patch_y[i], patch_z[i],
                            str(cp_index), color='black')
                    a = 4


        # ax.set_xlabel(r'$t$')
        ax.set_xlabel(r'$x$')
        ax.set_ylabel(r'$y$')
        ax.set_zlabel(r'$z$')

        plt.show()


        b = 4


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
