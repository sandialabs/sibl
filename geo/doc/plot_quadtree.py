from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

import ptg.quadtree as qt


# def test_plot_quadtree():
def main():
    shown = True
    serialize = True

    color_fill = True

    colors = (
        "tab:blue",
        "tab:orange",
        "tab:green",
        "tab:red",
        "tab:purple",
        "tab:brown",
        "tab:pink",
        "tab:gray",
        "tab:olive",
    )

    index_x, index_y = 0, 1  # avoid magic numbers later

    latex = True
    if latex:
        rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
        rc("text", usetex=True)

    fig = plt.figure(figsize=(6.0, 6.0), dpi=100)
    ax = fig.gca()

    ax.set_aspect("equal")

    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")

    """
    ^  simple example:
    |
    |     *-----------*
    |     |           |
    *-----1-----2-----3-----4-->
    |     |           |
    |     *-----------*
    """
    simple_example = True
    level_max = 6
    ax.set_title(f"level max = {level_max}")

    if simple_example:
        ctr = qt.Coordinate(x=2.0, y=0.0)
        cell = qt.Cell(center=ctr, size=2.0)
        # points = tuple([qt.Coordinate(2.1, 0.1), qt.Coordinate(2.6, 0.6)])
        points = tuple([qt.Coordinate(2.6, 0.6)])
        ax.set_xticks([1, 2, 3])
        ax.set_yticks([-1, 0, 1])
    else:
        ctr = qt.Coordinate(x=0.0, y=0.0)
        cell = qt.Cell(center=ctr, size=1024.0)
        points = tuple(
            [
                qt.Coordinate(-128.0, -512.0),
                qt.Coordinate(-96.0, -384.0),
                qt.Coordinate(-64.0, -256.0),
                qt.Coordinate(-32.0, -128.0),
                qt.Coordinate(0.0, 0.0),
                qt.Coordinate(32.0, 128.0),
                qt.Coordinate(64.0, 256.0),
                qt.Coordinate(96.0, 384.0),
                qt.Coordinate(128.0, 512.0),
            ]
        )
        ax.set_xticks([-512, -256, -128, 0, 128, 256, 512])
        ax.set_yticks([-512, -256, -128, 0, 128, 256, 512])

    tree = qt.QuadTree(cell=cell, level=0, level_max=level_max, points=points)

    quads = tree.quads()
    quad_levels = tree.quad_levels()

    # draw remaining L1 through Ln quads
    for i, quad in enumerate(quads):
        xs = [quad[k][index_x] for k in range(len(quad))]
        ys = [quad[k][index_y] for k in range(len(quad))]
        if color_fill:
            color_level = colors[np.remainder(quad_levels[i], len(colors))]
            plt.fill(
                xs,
                ys,
                edgecolor=color_level,
                alpha=0.2,
                linestyle="solid",
                linewidth=1.0,
                facecolor=color_level,
            )
        else:
            plt.fill(
                xs,
                ys,
                edgecolor="black",
                alpha=0.2,
                linestyle="solid",
                linewidth=1.0,
                facecolor="white",
            )

    xs = [point.x for point in points]
    ys = [point.y for point in points]
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
