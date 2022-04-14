"""
This module recreates the flower boundary representation presented in Figure 15 of
Rushdi AA, Mitchell SA, Mahmoud AH, Bajaj CC, Ebeida MS.
All-quad meshing without cleanup. Computer-Aided Design. 2017 Apr 1;85:83-98.

To run:
> cd ~/sibl
> conda activate siblenv
# update lesson_21.py as needed
> python lesson_21.py
"""
import math
from pathlib import Path
from typing import Final

import matplotlib.pyplot as plt
from matplotlib import rc

import xybind as xyb


def main():
    shown: Final = False
    axes_shown: Final = False
    serialize: Final = True
    meshed: Final = True

    latex: Final = False
    if latex:
        rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
        rc("text", usetex=True)

    n_samples: Final = 2**8
    radius: Final = 2.0
    mesh_resolution: Final = 0.09
    mesh_resolution_str = str("_res=" + str(mesh_resolution) + "_")

    # parameterize the curve
    # ts = tuple(range(n_samples + 1))
    ts = tuple(range(n_samples))
    rs = tuple(radius + 0.5 * math.cos(12.0 * math.pi * t / n_samples) for t in ts)
    # create x and y points
    xs = tuple(r * math.cos(radius * math.pi * t / n_samples) for (r, t) in zip(rs, ts))
    ys = tuple(r * math.sin(radius * math.pi * t / n_samples) for (r, t) in zip(rs, ts))

    # visualization
    s = 6.0  # 6.0 inches
    fig = plt.figure(figsize=(s, s))
    ax = fig.gca()

    # plot boundary as connected discrete points
    ax.plot(xs, ys, "-", alpha=0.5, color="orange")
    ax.plot(xs, ys, ",", alpha=0.8, color="purple")

    ix = 0  # the x-coordinate index
    iy = 1  # the y-coordinate index

    # mesh
    if meshed:
        mesh = xyb.QuadMesh(xs, ys)
        mesh.compute(resolution=mesh_resolution)
        nodes = mesh.nodes()

        keys = [str(int(n[0])) for n in nodes]
        values = [(n[1], n[2]) for n in nodes]  # collect (x, y) pairs, ignore z value
        zip_iterator = zip(keys, values)
        key_value_dict = dict(zip_iterator)

        elements = mesh.connectivity()
        # work with only three elements for debug purposes
        # elements = elements[0:3]

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
                linewidth=0.5,
                facecolor="white",
            )

    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    bounds = int(radius + 1)
    ticks = list(range(-bounds, bounds + 1))

    ax.set_xticks(ticks)
    ax.set_yticks(ticks)

    if not axes_shown:
        plt.axis("off")
    else:
        plt.axis("on")

    if shown:
        plt.show()

    # TODO: saving the plot, and writing to a .mesh file
    if serialize:
        # cwd = Path.cwd()
        parent_path = Path(__file__).parent
        extension = ".pdf"  # ".png" | ".pdf" | ".svg"
        # filename = Path(__file__).stem + "_" + test_case + extension
        test_case = Path(__file__).stem
        filename = test_case + mesh_resolution_str + extension
        # filepath = cwd.joinpath(filename)
        folder_name = "fig"
        filepath = parent_path.joinpath(folder_name, filename)
        fig.savefig(filepath, bbox_inches="tight", pad_inches=0)
        print(f"Serialized figure to {filepath}")


if __name__ == "__main__":
    main()
