from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

import ptg.quadtree as qt


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

    latex = False
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
    simple_example = False
    quarter_brush = True
    diagonal_example = False
    level_max = 4
    # ax.set_title(f"level max = {level_max}")
    plt.axis("off")

    if simple_example:
        ctr = qt.Coordinate(x=2.0, y=0.0)
        cell = qt.Cell(center=ctr, size=2.0)
        # points = tuple([qt.Coordinate(2.1, 0.1), qt.Coordinate(2.6, 0.6)])
        points = tuple(
            [qt.Coordinate(2.6, 0.6)],
        )
        ax.set_xticks([1, 2, 3])
        ax.set_yticks([-1, 0, 1])

    elif quarter_brush:
        ctr = qt.Coordinate(x=1024.0, y=1024.0)
        cell = qt.Cell(center=ctr, size=2048.0)
        num_points = 2
        axis_1 = np.linspace(start=0.0, stop=0.0, num=num_points, endpoint=True)
        axis_0 = np.linspace(start=0.0, stop=0.0, num=num_points, endpoint=True)
        xaxis = tuple(map(qt.Coordinate, axis_1, axis_0))
        yaxis = tuple(map(qt.Coordinate, axis_0, axis_1))
        points = xaxis + yaxis

        ax.set_xticks([0, 128, 256, 512, 1024, 2048])
        ax.set_yticks([0, 128, 256, 512, 1024, 2048])

    else:
        ctr = qt.Coordinate(x=0.0, y=0.0)
        cell = qt.Cell(center=ctr, size=1024.0)

        # boundary points
        num_points = 17  # 9 for single density, or 17 for double density
        if diagonal_example:
            bpx = np.linspace(start=-512.0, stop=512.0, num=num_points, endpoint=True)
            bpy = bpx
        else:
            # bpx = (-128.0, -96.0, -64.0, -32.0, 0.0, 32.0, 64.0, 96.0, 128.0)
            bpx = np.linspace(start=-128.0, stop=128.0, num=num_points, endpoint=True)
            # bpy = (-512.0, -384.0, -256.0, -128.0, 0.0, 128.0, 256.0, 384.0, 512.0)
            bpy = np.linspace(start=-512.0, stop=512.0, num=num_points, endpoint=True)

        points = tuple(map(qt.Coordinate, bpx, bpy))
        ax.set_xticks([-512, -256, -128, 0, 128, 256, 512])
        ax.set_yticks([-512, -256, -128, 0, 128, 256, 512])

    tree = qt.QuadTree(cell=cell, level=0, level_max=level_max, points=points)

    quads = tree.quads()
    quad_levels = tree.quad_levels()

    # draw remaining L1 through Ln quads
    for i, quad in enumerate(quads):
        xs = (quad.sw.x, quad.se.x, quad.ne.x, quad.nw.x)
        ys = (quad.sw.y, quad.se.y, quad.ne.y, quad.nw.y)
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

    xs = tuple(point.x for point in points)
    ys = tuple(point.y for point in points)
    ax.scatter(xs, ys, linestyle="solid", edgecolor="black", color="tab:red")

    if shown:
        plt.show()

    if serialize:
        extension = ".pdf"  # ".png" | ".pdf" | ".svg"
        filename = Path(__file__).stem + extension
        fig.savefig(filename, bbox_inches="tight", pad_inches=0)
        print(f"Serialized to {filename}")


if __name__ == "__main__":
    main()
