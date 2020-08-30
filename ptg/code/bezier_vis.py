# abstract base class for Bezier [curve, surface, solid] vis
from abc import ABC
import argparse
import json
from pathlib import Path
import sys

import matplotlib.tri as mtri
import matplotlib.pyplot as plt
import numpy as np

import bernstein_polynomial as bp


class BezierVis(ABC):
    def __init__(self, config, verbose=False):
        """Visualize Bezier [curve, surface, solid]."""

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
        config_schema = [
            "bezier-type",
            "data-path",
            "control-points",
            "control-nets",
        ]

        # check .json input schema
        for kw in config_schema:
            key = db.get(kw, None)
            if not key:
                sys.exit(f'Error: keyword "{kw}" not found in config file.')

        bezier_type = db.get("bezier-type")
        bezier_types = ("curve", "surface", "solid")
        if bezier_type not in bezier_types:
            sys.exit(f'Error: bezier-type "{bezier_type}" not supported.')

        data_path = db.get("data-path")
        data_path_expanded = Path(data_path).expanduser()
        cp_file = db.get("control-points")
        cn_file = db.get("control-nets")

        # number of time interval divisions nti_divisions
        # gives rise to the number of time intervals nti as
        # 2**nti_divisions = nti
        # 1 -> 2**1 = 2 (default)
        # 2 -> 2**2 = 4
        # 3 -> 2**3 = 8
        # 4 -> 2**4 = 64
        # etc.
        nti_divisions = db.get("nti_divisions", 1)
        if nti_divisions < 1:
            print("Error: number of time interval divisions (nti_divisions)")
            print("must be a positive integer, [1, 2, 3 ...].")
            sys.exit(f"Currint nti_divisions = {nti_divisions}")

        # control point data
        # do not set alpha, let scatter3D control this, which
        # automatically provides an implied depth of field
        #
        # control_points_alpha = db.get("control-alpha", 0.9)
        control_points_color = db.get("control-points-color", "red")
        control_points_label = db.get("control-points-label", False)
        control_points_size = db.get("control-points-size", 50)

        # draw a specific control net (or nets)
        control_nets_shown = db.get("control-nets-shown", False)

        # Bezier interpolation data
        # the alpha channel (transparency) for the Bezier curve,
        # surface, or volume when rendered
        # do not set alpha, let scatter3D control this, which
        # automatically provides an implied depth of field
        #
        # bezier_points_alpha = db.get("bezier-alpha", 0.9)
        bezier_points_color = db.get("bezier-points-color", "blue")
        bezier_points_shown = db.get("bezier-points-shown", True)
        bezier_points_size = db.get("bezier-points-size", 10)
        #
        bezier_lines_shown = db.get("bezier-lines-shown", False)

        if bezier_type == "surface":
            surface_triangulation = db.get("surface-triangulation", True)
            triangulation_alpha = db.get("triangulation-alpha", 1.0)

        xlabel = db.get("xlabel", "x")
        ylabel = db.get("ylabel", "y")
        zlabel = db.get("zlabel", "z")

        xlim = db.get("xlim", None)
        ylim = db.get("ylim", None)
        zlim = db.get("zlim", None)

        camera_elevation = db.get("camera-elevation", None)
        camera_azimuth = db.get("camera-azimuth", None)

        # check existence of path and files
        # if not Path(data_path_expanded).is_dir():
        if not data_path_expanded.is_dir():
            sys.exit(f"Error: cannot find {data_path}")

        # cp_path_file = data_path_expanded + cp_file
        cp_path_file = data_path_expanded.joinpath(cp_file)
        # if not Path(cp_path_file).is_file():
        if not cp_path_file.is_file():
            sys.exit(f"Error: cannot find {cp_path_file}")

        # cn_path_file = data_path_expanded + cn_file
        cn_path_file = data_path_expanded.joinpath(cn_file)
        # if not Path(cn_path_file).is_file():
        if not cn_path_file.is_file():
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

        if control_nets_shown:
            # example for control_nets_shown
            # False: show no control nets
            # [0]: show the first control net
            # [0, 2]: show the first and third control nets
            for net in [nets[k] for k in control_nets_shown]:
                net_x = [cp_x[i] for i in net]
                net_y = [cp_y[i] for i in net]
                net_z = [cp_z[i] for i in net]
                ax.plot3D(
                    net_x,
                    net_y,
                    net_z,
                    color=control_points_color,
                    linestyle="dashed",
                    linewidth=0.8,
                )

                if control_points_label:
                    for i, cp_index in enumerate(net):
                        ax.scatter3D(
                            net_x[i],
                            net_y[i],
                            net_z[i],
                            edgecolor=control_points_color,
                            facecolor=(0, 0, 0, 0),
                            marker="^",
                            s=control_points_size,
                        )
                        ax.text(
                            net_x[i], net_y[i], net_z[i], str(cp_index), color="black"
                        )
                        if verbose:
                            print(f"net node {i} is control point {cp_index}")

                if bezier_points_shown or bezier_lines_shown:
                    x, y, z = (0.0, 0.0, 0.0)

                    # assumes number of control points same along each axis
                    # for either 2D (or 3D, to come); 2D uses square root
                    # and 3D will use cube root
                    # n_cp_per_axis = int(np.sqrt(len(net)))
                    # 1D case:
                    if bezier_type == "curve":
                        n_cp_per_axis = len(net)

                    elif bezier_type == "surface":
                        n_cp_per_axis = int(np.sqrt(len(net)))

                    elif bezier_type == "solid":
                        n_cp_per_axis = int(np.cbrt(len(net)))

                    p_degree = n_cp_per_axis - 1  # polynomial degree
                    # nti = 2  # segment [0, 1] into nti intervals
                    # nti = 2**4  # segment [0, 1] into nti intervals
                    nti = 2 ** nti_divisions  # segment [0, 1] into nti intervals
                    # triangulate the surface
                    # https://matplotlib.org/3.1.1/gallery/mplot3d/trisurf3d_2.html
                    t = np.linspace(0, 1, num=nti + 1, endpoint=True)  # curve
                    u = np.linspace(0, 1, num=nti + 1, endpoint=True)  # surface
                    # v = np.linspace(0, 1, num=nti + 1, endpoint=True)  # solid

                    if bezier_type == "curve":

                        Point = net

                        for i in np.arange(n_cp_per_axis):
                            b_i = bp.bernstein_polynomial(i, p_degree, nti)

                            if verbose:
                                print(f"b{i} = {b_i}")

                            x += b_i * cp_x[Point[i]]
                            y += b_i * cp_y[Point[i]]
                            z += b_i * cp_z[Point[i]]

                    if bezier_type == "surface":

                        Point = np.reshape(net, (n_cp_per_axis, n_cp_per_axis))

                        for i in np.arange(n_cp_per_axis):
                            for j in np.arange(n_cp_per_axis):
                                b_i = bp.bernstein_polynomial(i, p_degree, nti)
                                b_j = bp.bernstein_polynomial(j, p_degree, nti)
                                bij = np.outer(b_i, b_j)

                                if verbose:
                                    print(f"bij = {bij}")

                                x += bij * cp_x[Point[i][j]]
                                y += bij * cp_y[Point[i][j]]
                                z += bij * cp_z[Point[i][j]]
                        # my convention is reverse of the (x, y) convention of
                        # mesh grid, see
                        # https://numpy.org/doc/stable/reference/generated/numpy.meshgrid.html
                        u, t = np.meshgrid(u, t)
                        u, t = u.flatten(), t.flatten()

                        if surface_triangulation:
                            # triangulate parameter space to determine the triangles, cf
                            # https://matplotlib.org/3.1.1/gallery/mplot3d/trisurf3d_2.html
                            tri = mtri.Triangulation(u, t)
                            ax.plot_trisurf(
                                x.flatten(),
                                y.flatten(),
                                z.flatten(),
                                triangles=tri.triangles,
                                alpha=triangulation_alpha,
                            )
                            if verbose:
                                print("Triangulation is complete.")

                    if bezier_type == "solid":
                        sys.exit(f"bezier_type {bezier_type} not implemented.")

                    # ax.scatter3D(x.flatten(), y.flatten(), z.flatten(), color="red")
                    if bezier_points_shown:
                        ax.scatter3D(
                            x.flatten(),
                            y.flatten(),
                            z.flatten(),
                            color=bezier_points_color,
                            s=bezier_points_size,
                        )
                        # ax.scatter3D(, net_y, net_z, linestyle="dashed", linewidth=0.8)

                    if bezier_lines_shown:
                        ax.plot(
                            x.flatten(),
                            y.flatten(),
                            z.flatten(),
                            color="black",
                            linewidth=1.0,
                        )

        else:
            # no specific control nets specified,
            # default is just to show all control points
            ax.scatter3D(
                cp_x,
                cp_y,
                cp_z,
                edgecolor=control_points_color,
                facecolor=(0, 0, 0, 0),
                marker="^",
                s=control_points_size,
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

    # BezierCurveVis(config, verbose)
    BezierVis(config, verbose)


if __name__ == "__main__":
    main(sys.argv[1:])
