from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import rc

import ptg.quadtree as qt


def main():
    shown = True
    serialize = False

    latex = True
    if latex:
        rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
        rc("text", usetex=True)

    """
    ^
    |     *-----------*
    |     |           |
    *-----1-----2-----3-----4-->
    |     |           |
    |     *-----------*
    """
    ctr = qt.Coordinate(x=2.0, y=0.0)
    cell = qt.Cell(center=ctr, size=2.0)

    # two trigger point variation
    # points = tuple([qt.Coordinate(2.1, 0.1), qt.Coordinate(2.6, 0.6)],)

    # one trigger point variation
    points = tuple(
        [qt.Coordinate(2.6, 0.6)],
    )

    tree = qt.QuadTree(cell=cell, level=0, level_max=3, points=points)

    quads = tree.quads()

    fig = plt.figure(figsize=(6.0, 6.0), dpi=100)
    ax = fig.gca()

    ax.set_aspect("equal")

    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")

    ax.set_xticks([])
    ax.set_yticks([])

    quad_color = (
        "tab:orange",
        "tab:orange",
        "tab:orange",
        "tab:green",
        "tab:green",
        "tab:green",
        "tab:red",
        "tab:red",
        "tab:red",
        "tab:red",
    )  # hard code colors for this specific example

    # draw the base L0 quad
    plt.fill(
        [0.98, 3.02, 3.02, 0.98],
        [-1.02, -1.02, 1.02, 1.02],
        edgecolor="tab:blue",
        alpha=1.0,
        linewidth=2.0,
        linestyle="dashed",
        facecolor="white",
    )

    # draw remaining L1 through L3 quads
    for i, quad in enumerate(quads):
        xs = (quad.sw.x, quad.se.x, quad.ne.x, quad.nw.x)
        ys = (quad.sw.y, quad.se.y, quad.ne.y, quad.nw.y)
        plt.fill(
            xs,
            ys,
            edgecolor=quad_color[i],
            alpha=1.0,
            linewidth=2.0,
            facecolor="white",
        )

    xs = tuple(point.x for point in points)
    ys = tuple(point.y for point in points)
    ax.scatter(xs, ys, linestyle="solid", edgecolor="black", color="tab:red")

    plt.annotate(
        r"$\bf{00}$",
        xy=(1.5, -0.5),
        color="tab:orange",
        horizontalalignment="center",
        verticalalignment="center",
        fontsize="xx-large",
    )
    plt.annotate(
        r"$\bf{01}$",
        xy=(1.5, 0.5),
        color="tab:orange",
        horizontalalignment="center",
        verticalalignment="center",
        fontsize="xx-large",
    )
    plt.annotate(
        r"$\bf{10}$",
        xy=(2.5, -0.5),
        color="tab:orange",
        horizontalalignment="center",
        verticalalignment="center",
        fontsize="xx-large",
    )
    plt.annotate(
        r"$\bf{1100}$",
        xy=(2.25, 0.25),
        color="tab:green",
        horizontalalignment="center",
        verticalalignment="center",
        fontsize="x-large",
    )
    plt.annotate(
        r"$\bf{1101}$",
        xy=(2.25, 0.75),
        color="tab:green",
        horizontalalignment="center",
        verticalalignment="center",
        fontsize="x-large",
    )
    plt.annotate(
        r"$\bf{1110}$",
        xy=(2.75, 0.25),
        color="tab:green",
        horizontalalignment="center",
        verticalalignment="center",
        fontsize="x-large",
    )
    plt.annotate(
        r"$\bf{111100}$",
        xy=(2.625, 0.625),
        color="tab:red",
        horizontalalignment="center",
        verticalalignment="center",
        fontsize="small",
    )
    plt.annotate(
        r"$\bf{111101}$",
        xy=(2.625, 0.875),
        color="tab:red",
        horizontalalignment="center",
        verticalalignment="center",
        fontsize="small",
    )
    plt.annotate(
        r"$\bf{111110}$",
        xy=(2.875, 0.625),
        color="tab:red",
        horizontalalignment="center",
        verticalalignment="center",
        fontsize="small",
    )
    plt.annotate(
        r"$\bf{111111}$",
        xy=(2.875, 0.875),
        color="tab:red",
        horizontalalignment="center",
        verticalalignment="center",
        fontsize="small",
    )

    if shown:
        plt.show()

    if serialize:

        extension = ".png"  # ".png" | ".pdf" | ".svg"
        filename = Path(__file__).stem + extension
        fig.savefig(filename, bbox_inches="tight", pad_inches=0)
        print(f"Serialized to {filename}")


if __name__ == "__main__":
    main()
