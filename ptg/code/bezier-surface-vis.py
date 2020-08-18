# Bezier surface visualization, e.g., the utah teapot
import argparse
import json
from pathlib import Path
import sys

import matplotlib.tri as mtri
import matplotlib.pyplot as plt
import numpy as np

import bernstein_polynomial as bp


class BezierSurfaceVis:
    def __init__(self, config, verbose=0):

        # abbreviations:
        # cp: control point; collection of control points forms the control net
        # cn: control net, composed of control points
        # n_cp: number of control points (int) per net
        # n_nets: number of control nets (int)

        if not Path(config).is_file():
            sys.exit(f"Error: cannot find file {config}")

        config_location = Path(config).parent

        if verbose:
            class_name = type(self).__name__
            print(f"This is {class_name} processing config file: {config}")
            print(f"located at: {config_location}")

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

        # number of time interval divisions nti_divisions
        # gives rise to the number of time intervals nti as
        # 2**nti_divisions = nti
        # 1 -> 2**1 = 2 (default)
        # 2 -> 2**2 = 4
        # 3 -> 2**3 = 8
        # 4 -> 2**4 = 64
        # etc.
        nti_divisions = db.get("nti_divisions", 1)

        # show/hide control point index labels
        cp_labels = db.get("control-points-label", False)
        cp_edge_color = db.get("control-points-edge-color", "blue")
        cp_marker_size = db.get("control-points-marker-size", 10)

        # draw a specific control net (or nets)
        cn_shown = db.get("control-nets-shown", False)

        # the alpha channel (transparency) for the Bezier curve,
        # surface, or volume when rendered
        bezier_alpha = db.get("bezier-alpha", 0.4)

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
            sys.exit(f"Error: cannot find {data_path}")

        cp_path_file = data_path + cp_file
        if not Path(cp_path_file).is_file():
            sys.exit(f"Error: cannot find {cp_path_file}")

        cn_path_file = data_path + cn_file
        if not Path(cn_path_file).is_file():
            sys.exit(f"Error: cannot find {cn_path_file}")

        # file io data type specification
        data_type_string = "float"
        data_type_int = "i8"
        data_type_delimiter = ","
        n_headers = 0  # no headers in the csv files

        # avoid "magic" numbers appears later in code
        idx, idy, idz = (0, 1, 2)  # column numbers from .csv file

        with open(cp_path_file) as fin:
            data = np.genfromtxt(
                cp_path_file,
                dtype=data_type_string,
                delimiter=data_type_delimiter,
                skip_header=n_headers,
            )
            cp_x = data[:, idx]
            cp_y = data[:, idy]
            cp_z = data[:, idz]

        with open(cn_path_file) as fin:
            nets = np.genfromtxt(
                cn_path_file,
                dtype=data_type_int,
                delimiter=data_type_delimiter,
                skip_header=n_headers,
            )

            if len(nets.shape) == 1:
                # handle special case of single net
                # https://numpy.org/devdocs/user/absolute_beginners.html#how-to-convert-a-1d-array-into-a-2d-array-how-to-add-a-new-axis-to-an-array
                nets = np.expand_dims(nets, axis=0)
                # otherwise, we have two or more nets, dims are ok

            n_nets, n_cp = nets.shape  # number (control nets, control points)

            if verbose:
                print(f"Number of control nets: {n_nets}")
                print(f"Number of control points per net: {n_cp}")

        ax = plt.axes(projection="3d")
        # ax.plot3D(cp_x, cp_y, cp_z)
        # ax.scatter3D(cp_x, cp_y, cp_z, edgecolor="blue",
        #              facecolor=(0, 0, 0, 0), s=10)

        if cn_shown:
            # example for cn_shown
            # False: show no control nets
            # [0]: show the first control net
            # [0, 2]: show the first and third control nets
            for net in [nets[k] for k in cn_shown]:
                net_x = [cp_x[i] for i in net]
                net_y = [cp_y[i] for i in net]
                net_z = [cp_z[i] for i in net]
                ax.plot3D(net_x, net_y, net_z, linestyle="dashed", linewidth=0.8)

                if cp_labels:
                    for i, cp_index in enumerate(net):
                        ax.scatter3D(
                            net_x[i],
                            net_y[i],
                            net_z[i],
                            edgecolor=cp_edge_color,
                            facecolor=(0, 0, 0, 0),
                            s=cp_marker_size,
                        )
                        ax.text(
                            net_x[i], net_y[i], net_z[i], str(cp_index), color="black"
                        )
                        if verbose:
                            print(f"net node {i} is control point {cp_index}")

                triangulate = True

                x, y, z = (0.0, 0.0, 0.0)
                if triangulate:
                    # assumes number of control points same along each axis
                    # for either 2D (or 3D, to come); 2D uses square root
                    # and 3D will use cube root
                    n_cp_per_axis = int(np.sqrt(len(net)))
                    p_degree = n_cp_per_axis - 1  # polynomial degree
                    # nti = 2  # segment [0, 1] into nti intervals
                    # nti = 2**4  # segment [0, 1] into nti intervals
                    nti = 2 ** nti_divisions  # segment [0, 1] into nti intervals
                    # triangulate the surface
                    # https://matplotlib.org/3.1.1/gallery/mplot3d/trisurf3d_2.html
                    t = np.linspace(0, 1, num=nti + 1, endpoint=True)
                    u = np.linspace(0, 1, num=nti + 1, endpoint=True)

                    Point = np.reshape(net, (n_cp_per_axis, n_cp_per_axis))

                    for i in np.arange(n_cp_per_axis):
                        for j in np.arange(n_cp_per_axis):
                            b_i = bp.bernstein_polynomial(i, p_degree, nti)
                            b_j = bp.bernstein_polynomial(j, p_degree, nti)
                            bij = np.outer(b_i, b_j)

                            if verbose:
                                print(f"bij = {bij}")

                            # x += bij * net_x[Point[i][j]]
                            # y += bij * net_y[Point[i][j]]
                            # z += bij * net_z[Point[i][j]]
                            x += bij * cp_x[Point[i][j]]
                            y += bij * cp_y[Point[i][j]]
                            z += bij * cp_z[Point[i][j]]

                    # my convention is reverse of the (x, y) convention of
                    # mesh grid, see
                    # https://numpy.org/doc/stable/reference/generated/numpy.meshgrid.html
                    u, t = np.meshgrid(u, t)
                    u, t = u.flatten(), t.flatten()

                    # triangulate paramter space to determine the triangles, cf
                    # https://matplotlib.org/3.1.1/gallery/mplot3d/trisurf3d_2.html
                    tri = mtri.Triangulation(u, t)
                    ax.plot_trisurf(
                        x.flatten(),
                        y.flatten(),
                        z.flatten(),
                        triangles=tri.triangles,
                        alpha=bezier_alpha,
                    )

                    if verbose:
                        print("Triangulation is complete.")
        else:
            # no specific control nets specified,
            # default is just to show all control points
            ax.scatter3D(
                cp_x,
                cp_y,
                cp_z,
                edgecolor=cp_edge_color,
                facecolor=(0, 0, 0, 0),
                s=cp_marker_size,
            )

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

    parser.add_argument(
        "--verbose", help="increased command line feedback", action="store_true"
    )

    args = parser.parse_args()

    config = args.config_file
    verbose = args.verbose

    BezierSurfaceVis(config, verbose)


if __name__ == "__main__":
    main(sys.argv[1:])
