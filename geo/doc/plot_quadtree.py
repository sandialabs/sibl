from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import rc

import ptg.quadtree as qt


# def test_plot_quadtree():
def main():
    shown = True
    serialize = True

    index_x, index_y = 0, 1  # avoid magic numbers later
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
    points = tuple([qt.Coordinate(2.1, 0.1), qt.Coordinate(2.6, 0.6)])

    tree = qt.QuadTree(cell=cell, level=0, level_max=2, points=points)

    quads = tree.quads()

    fig = plt.figure(figsize=(6.0, 6.0), dpi=100)
    ax = fig.gca()

    ax.set_aspect("equal")

    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")

    # ax.set_xlim([1, 3])
    # ax.set_ylim([-1, 1])

    ax.set_xticks([1, 2, 3])
    ax.set_yticks([-1, 0, 1])

    for quad in quads:
        xs = [quad[k][index_x] for k in range(len(quad))]
        ys = [quad[k][index_y] for k in range(len(quad))]
        plt.fill(
            xs,
            ys,
            linestyle="dotted",
            edgecolor="magenta",
            alpha=0.5,
            facecolor="gray",
        )

    # quads = (
    #     tree.cell.vertices,
    #     tree.cell.sw.vertices,
    #     tree.cell.nw.vertices,
    #     tree.cell.se.vertices,
    #     tree.cell.ne.vertices,
    #     tree.cell.ne.sw.vertices,
    #     tree.cell.ne.nw.vertices,
    #     tree.cell.ne.se.vertices,
    #     tree.cell.ne.ne.vertices,
    # )

    # fig = plt.figure(figsize=(6.0, 6.0), dpi=100)
    # ax = fig.gca()

    # for quad in quads:
    #     # xys = tree.cell.vertices
    #     xs = [quad[k][index_x] for k in range(len(quad))]
    #     ys = [quad[k][index_y] for k in range(len(quad))]
    #     plt.fill(
    #         xs,
    #         ys,
    #         linestyle="dotted",
    #         edgecolor="magenta",
    #         alpha=0.5,
    #         facecolor="gray",
    #     )

    xs = [point.x for point in points]
    ys = [point.y for point in points]
    ax.scatter(xs, ys, linestyle="solid", edgecolor="black", color="tab:red")

    if shown:
        plt.show()

    if serialize:

        extension = ".png"  # or '.'.png' | '.pdf' | '.svg'
        filename = Path(__file__).stem + extension
        fig.savefig(filename, bbox_inches="tight", pad_inches=0)
        print(f"Serialized to {filename}")


if __name__ == "__main__":
    main()
