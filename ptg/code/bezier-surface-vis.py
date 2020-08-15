# utah teapot visualization
import argparse
import json
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np


class BezierSurfaceVis:

    def __init__(self, config, verbose=0):

        # abbreviations:
        # cp: control point; collection of control points forms the control net
        # cn: control net, composed of control points
        # n_cp: number of control points (int) per net
        # n_nets: number of control nets (int)

        if not Path(config).is_file():
            sys.exit(f'Error: cannot find file {config}')

        config_location = Path(config).parent

        if verbose:
            print(f'\nBezierSolid processing config file: {config}')
            print(f'located at: {config_location}')

        with open(config) as fin:
            db = json.load(fin)

        # config parameters without defaults, user specification required
        config_schema = ["data-path", "control-points", "control-nets"]

        # check .json input schema
        for kw in config_schema:
            key = db.get(kw, None)
            if not key:
                sys.exit(f'Error: keyword "{kw}" not found in config file.')

        data_path = db.get("data-path")
        cp_file = db.get("control-points")
        cn_file = db.get("control-nets")

        # config parameters with defaults, no user specification required

        # show/hide control point index labels
        cp_labels = db.get("control-points-label", False)

        # draw a specific control net (or nets)
        cn_shown = db.get("control-nets-shown", False)

        xlabel = db.get("xlabel", "x")
        ylabel = db.get("ylabel", "y")
        zlabel = db.get("zlabel", "z")

        xlim = db.get("xlim", None)
        ylim = db.get("ylim", None)
        zlim = db.get("zlim", None)

        camera_elevation = db.get("camera-elevation", None)
        camera_azimuth = db.get("camera-azimuth", None)

        # check existence of path and files
        if not Path(data_path).is_dir():
            sys.exit(f'Error: cannot find {data_path}')

        cp_path_file = data_path + cp_file
        if not Path(cp_path_file).is_file():
            sys.exit(f'Error: cannot find {cp_path_file}')

        cn_path_file = data_path + cn_file
        if not Path(cn_path_file).is_file():
            sys.exit(f'Error: cannot find {cn_path_file}')

        # file io data type specification
        data_type_string = 'float'
        data_type_int = 'i8'
        data_type_delimiter = ','
        n_headers = 0  # no headers in the csv files

        # avoid "magic" numbers appears later in code
        idx, idy, idz = (0, 1, 2)  # column numbers from .csv file

        with open(cp_path_file) as fin:
            data = np.genfromtxt(cp_path_file,
                                 dtype=data_type_string,
                                 delimiter=data_type_delimiter,
                                 skip_header=n_headers)
            cp_x = data[:, idx]
            cp_y = data[:, idy]
            cp_z = data[:, idz]

        with open(cn_path_file) as fin:
            nets = np.genfromtxt(cn_path_file,
                                 dtype=data_type_int,
                                 delimiter=data_type_delimiter,
                                 skip_header=n_headers)

            if len(nets.shape) == 1:
                # handle special case of single net
                # https://numpy.org/devdocs/user/absolute_beginners.html#how-to-convert-a-1d-array-into-a-2d-array-how-to-add-a-new-axis-to-an-array
                nets = np.expand_dims(nets, axis=0)
                # otherwise, we have two or more nets, dims are ok

            n_nets, n_cp = nets.shape  # number (control nets, control points)

            if verbose:
                print(f'Number of control nets: {n_nets}')
                print(f'Number of control points per net: {n_cp}')

        ax = plt.axes(projection='3d')
        # ax.plot3D(cp_x, cp_y, cp_z)
        ax.scatter3D(cp_x, cp_y, cp_z)

        if cn_shown:
            # for utah-teapot debugging:
            # net number, description
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
            for net in [nets[k] for k in cn_shown]:
                net_x = [cp_x[i] for i in net]
                net_y = [cp_y[i] for i in net]
                net_z = [cp_z[i] for i in net]
                ax.plot3D(net_x, net_y, net_z, linestyle='dashed')

                if cp_labels:
                    for i, cp_index in enumerate(net):
                        if verbose:
                            print(f'net node {i} is control point {cp_index}')
                        ax.text(net_x[i], net_y[i], net_z[i],
                                str(cp_index), color='black')
                        a = 4

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_zlabel(zlabel)

        if xlim:
            ax.set_xlim(xlim)

        if ylim:
            ax.set_ylim(ylim)

        if zlim:
            ax.set_zlim(zlim)

        ax.view_init(elev=camera_elevation, azim=camera_azimuth)

        plt.show()


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
