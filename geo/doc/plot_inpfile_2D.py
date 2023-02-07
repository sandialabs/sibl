from pathlib import Path
from typing import Final

from matplotlib import rc
import matplotlib.pyplot as plt

import ptg.translator as trans
import ptg.mesh as mesh


def main():
    # input_userstring = "~/sibl/geo/data/mesh/two_quads.inp"
    input_userstring = "~/sibl/geo/data/mesh/two_quads_nonseq.inp"
    # input_userstring = "~/sibl/geo/doc/dual/lesson_04/lesson_04_mesh.inp"
    #
    # input_pathfile = Path("~/sibl/geo/data/mesh/two_quads.inp").expanduser()
    input_pathfile = Path(input_userstring).expanduser()
    input_pathfile_base = input_pathfile.stem
    fig_shown: Final = True
    nodes_shown: Final = True
    node_numbers_shown: Final = True
    node_size: Final = 100
    node_alpha: Final = 0.9

    serialize: Final = True
    ix: Final = 0  # index to x-coordinate
    iy: Final = 1  # index to y-coordinate
    # color_file: Final = True
    # plot_kwargs: {"alpha": 1.0, "color": "black", "linestyle": "solid", "linewidth": 0.1}
    # plot_kwargs: {"alpha": 1.0, "color": "black"}

    latex: Final = False
    if latex:
        rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
        rc("text", usetex=True)

    dpi = 100  # dots per inch
    # xticks = (-1, 0, 1, 2)
    # yticks = xticks

    fig = plt.figure(figsize=(6.0, 6.0), dpi=dpi)
    ax = fig.gca()

    ax.set_aspect("equal")

    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")

    # ax.set_title(f"level max = {level_max}")
    plt.axis("on")
    # ax.set_xticks(xticks)
    # ax.set_yticks(yticks)

    nodes = trans.inp_path_file_to_coordinates(pathfile=str(input_pathfile))
    elements = trans.inp_path_file_to_connectivities(pathfile=str(input_pathfile))
    elements_wo_element_number = tuple([x[1:] for x in elements])

    edges = mesh.adjacencies_upper_diagonal(xs=elements_wo_element_number)

    for edge in edges:
        edge_points = [nodes[ii] for ii in map(str, edge)]
        # xs = [nodes[e - 1][ix] for e in edge]  # nodes[e-1] to convert from 1-index to 0-index
        # ys = [nodes[e - 1][iy] for e in edge]
        xs = [point[ix] for point in edge_points]
        ys = [point[iy] for point in edge_points]
        # plt.plot(xs, ys, **plot_kwargs)
        plt.plot(
            xs,
            ys,
            alpha=1.0,
            linewidth=0.5,
            color="blue",
            marker=None,
            markerfacecolor="red",
        )

    if nodes_shown:
        xs = [item[ix] for item in nodes.values()]
        ys = [item[iy] for item in nodes.values()]
        ax.scatter(
            xs,
            ys,
            linestyle="solid",
            edgecolor="black",
            color="yellow",
            alpha=node_alpha,
            s=node_size,
        )

    if node_numbers_shown:
        # cannot do xs and ys format, must do text one at a time
        for item in nodes.items():
            c = item[0]
            x = item[1][ix]
            y = item[1][iy]
            ax.text(x, y, c, horizontalalignment="center", verticalalignment="center")

    if fig_shown:
        plt.show()

    if serialize:
        extension = ".png"  # ".png" | ".pdf" | ".svg"
        filename = input_pathfile_base + extension
        pathfilename = Path.cwd().joinpath(filename)
        fig.savefig(pathfilename, bbox_inches="tight", pad_inches=0)
        print(f"Serialized to {pathfilename}")


if __name__ == "__main__":
    main()


"""
Copyright 2023 Sandia National Laboratories

Notice: This computer software was prepared by National Technology and Engineering Solutions of
Sandia, LLC, hereinafter the Contractor, under Contract DE-NA0003525 with the Department of Energy
(DOE). All rights in the computer software are reserved by DOE on behalf of the United States
Government and the Contractor as provided in the Contract. You are authorized to use this computer
software for Governmental purposes but it is not to be released or distributed to the public.
NEITHER THE U.S. GOVERNMENT NOR THE CONTRACTOR MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR ASSUMES
ANY LIABILITY FOR THE USE OF THIS SOFTWARE. This notice including this sentence must appear on any
copies of this computer software. Export of this data may require a license from the United States
Government.
"""
