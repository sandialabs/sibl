"""This module shows examples of quadtrees that have been refined around boundaries.

To run
> conda active siblenv
> cd ~/sibl/geo/examples
> python quadtree_example.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import rc

import ptg.quadtree as qt


def main():

    level_max = 4
    shown = True
    serialize = False

    latex = False
    if latex:
        rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
        rc("text", usetex=True)

    # index_x, index_y = 0, 1  # indices, avoid magic numbers

    ctr = qt.Coordinate(x=100.0, y=100.0)
    cell = qt.Cell(center=ctr, size=100.0)

    # points = tuple(
    #     [qt.Coordinate(95.0, 80.0), qt.Coordinate(101.0, 101.0), qt.Coordinate(105.0, 120.0)]
    # )
    points = (
        qt.Coordinate(95.0, 80.0),
        qt.Coordinate(101.1, 101.1),
        qt.Coordinate(105.0, 120.0),
    )

    tree = qt.QuadTree(cell=cell, level=0, level_max=level_max, points=points)

    quads = tree.quads()

    fig = plt.figure(figsize=(6.0, 6.0), dpi=100)
    ax = fig.gca()

    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")

    # ax.set_xticks([])
    # ax.set_yticks([])

    # draw remaining L1 through Ln quads
    for i, quad in enumerate(quads):
        xs = (quad.sw.x, quad.se.x, quad.ne.x, quad.nw.x)
        ys = (quad.sw.y, quad.se.y, quad.ne.y, quad.nw.y)
        plt.fill(
            xs,
            ys,
            edgecolor="black",
            alpha=0.2,
            linestyle="solid",
            linewidth=1.0,
            facecolor="white",
        )

    xs = tuple(point.x for point in points)
    ys = tuple(point.y for point in points)
    ax.scatter(xs, ys, linestyle="solid", edgecolor="black", color="tab:red")

    if shown:
        plt.show()

    if serialize:

        extension = ".png"  # ".png" | ".pdf" | ".svg"
        filename = Path(__file__).stem + extension
        fig.savefig(filename, bbox_inches="tight", pad_inches=0)
        print(f"Serialized to {filename}")


if __name__ == "__main__":
    main()
