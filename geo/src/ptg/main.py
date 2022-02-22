"""This module runs the SIBL Mesh Engine from the command line.

Example:
> conda activate siblenv
> cd ~/sibl
> python geo/src/ptg/main.py -i path_to_file/input_template.yml
"""

import argparse
import os

# import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Final

import numpy as np
import matplotlib.pyplot as plt

from ptg import reader as reader
import xybind as xyb


def dualize(*, input_path_file: str) -> bool:
    """This wrapper method supports command line use and test."""

    r = reader.Reader(input_file=input_path_file)
    database = r.database

    print(f"The database is {database}")

    db: Final = SimpleNamespace(**database)
    print(f"This input file has version {db.version}")
    version_required: Final = 1.4
    if db.version != version_required:
        _used = f"yml input file version error: version {db.version} was used,"
        _required = f" and version {version_required} is required."
        raise ValueError(_used + _required)

    working_path = Path(db.io_path).expanduser()
    if working_path.is_dir():
        print(f"io_path: {working_path}")
        try:
            os.chdir(working_path)
            print(f"Current working directory changed to {working_path}")
        except PermissionError:
            print(f"Permission denied to change into directory {working_path}")

    figure: Final = SimpleNamespace(**db.figure)

    print(f"yml specified boundary file: {db.boundary}")
    path_file_in = Path(db.boundary).expanduser()
    if path_file_in.is_file():
        print("  located boundary file at:")
        print(f"  {path_file_in}")
    else:
        raise OSError(f"File not found: {path_file_in}")

    # np.genfromtxt will automatically ignore comment lines starting with
    # the "#" character
    # https://numpy.org/devdocs/reference/generated/numpy.genfromtxt.html
    ix, iy = 0, 1
    boundary = np.genfromtxt(
        path_file_in,
        dtype="float",
        usecols=(ix, iy),
    )

    xs, ys = boundary[:, ix], boundary[:, iy]
    ((ll_x, ll_y), (ur_x, ur_y)) = db.bounding_box

    mesh = xyb.QuadMesh()
    mesh.initialize(
        boundary_xs=xs,
        boundary_ys=ys,
        boundary_refine=db.boundary_refine,
        resolution=db.resolution,
        lower_bound_x=ll_x,
        lower_bound_y=ll_y,
        upper_bound_x=ur_x,
        upper_bound_y=ur_y,
        developer_output=db.developer_output,
        output_file=db.output_file,
    )

    mesh.compute()

    if figure.show or figure.save:

        if figure.latex:
            from matplotlib import rc

            rc("text", usetex=True)
            rc("font", family="serif")

        # get the nodes
        nodes = mesh.nodes()
        # nnp = len(nodes)  # number of nodal points

        # create a dictionary lookup table from the index to the nodal (x, y, z)
        # coordinates
        keys = [str(int(n[0])) for n in nodes]
        values = [(n[1], n[2]) for n in nodes]  # collect (x, y) pairs, ignore z value
        zip_iterator = zip(keys, values)
        key_value_dict = dict(zip_iterator)

        # get the elements
        elements = mesh.connectivity()

        fig_size_x, fig_size_y = figure.size
        fig = plt.figure(figsize=(fig_size_x, fig_size_y))

        ax = fig.gca()
        xmin = db.bounding_box[0][ix]
        xmax = db.bounding_box[1][ix]
        ymin = db.bounding_box[0][iy]
        ymax = db.bounding_box[1][iy]

        ax.set_xlim([xmin, xmax])
        ax.set_ylim([ymin, ymax])

        if figure.grid:
            ax.grid()

        if figure.boundary_shown:
            # plot boundary used to create the mesh
            ax.plot(xs, ys, "-", alpha=0.5)
            ax.plot(xs, ys, ".")

        if figure.elements_shown:
            # plot the mesh
            ix, iy = 0, 1  # the x- and y-coordinate indices
            for e in elements:
                element_points = [key_value_dict[ii] for ii in map(str, e)]
                exs = [pt[ix] for pt in element_points]
                eys = [pt[iy] for pt in element_points]
                plt.fill(
                    exs,
                    eys,
                    edgecolor="black",
                    alpha=1.0,
                    linestyle="solid",
                    linewidth=1.0,
                    facecolor="white",
                )

        ax.set_aspect("equal")
        ax.set_frame_on(b=figure.frame)
        if figure.frame:
            ax.set_title(figure.title)
            ax.set_xlabel(figure.label_x)
            ax.set_ylabel(figure.label_y)
            ax.set_axis_on()
        else:
            ax.set_axis_off()

        if figure.show:
            plt.show()

        if figure.save:
            ofile = figure.filename + "." + figure.format
            fig.savefig(ofile, dpi=figure.dpi, bbox_inches="tight")
            print(f"  Saved figure to {ofile}")

        plt.close("all")  # close all figures if they are still open

    print("SIBL Mesh Engine completed.")
    engine_completed = True
    return engine_completed


def main():

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

    args_path_file = args.input_file

    print("Dualization initiated.")
    success = dualize(input_path_file=args_path_file)
    if success:
        print("Dualization is complete.")
    else:
        print("Dualization is incomplete.")

    print("SIBL Mesh Engine completed.")


if __name__ == "__main__":
    main()
