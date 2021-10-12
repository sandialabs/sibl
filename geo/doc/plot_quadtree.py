from pathlib import Path
from typing import Final

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc


import ptg.quadtree as qt


def main():
    shown: Final = False
    serialize: Final = True
    color_fill: Final = True

    latex: Final = False
    if latex:
        rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
        rc("text", usetex=True)

    # test_cases: "benchmark", "brush", "diagonal", "nested_0001", "simple", "wall_0011"
    test_case = "benchmark"

    level_max: Final = 2

    if test_case == "simple":
        ctr = qt.Coordinate(x=0.0, y=0.0)
        cell = qt.Cell(center=ctr, size=2.0)
        # points = tuple([qt.Coordinate(2.1, 0.1), qt.Coordinate(2.6, 0.6)])
        points = tuple(
            [qt.Coordinate(0.6, 0.6)],
        )
        _xticks = [-2, -1, 0, 1, 2]
        _yticks = _xticks
        # ax.set_xticks([1, 2, 3])
        # ax.set_yticks([-1, 0, 1])

    elif test_case == "brush":
        ctr = qt.Coordinate(x=1024.0, y=1024.0)
        cell = qt.Cell(center=ctr, size=2048.0)
        num_points = 2
        axis_1 = np.linspace(start=0.0, stop=0.0, num=num_points, endpoint=True)
        axis_0 = np.linspace(start=0.0, stop=0.0, num=num_points, endpoint=True)
        xaxis = tuple(map(qt.Coordinate, axis_1, axis_0))
        yaxis = tuple(map(qt.Coordinate, axis_0, axis_1))
        points = xaxis + yaxis

        # ax.set_xticks([0, 128, 256, 512, 1024, 2048])
        # ax.set_yticks([0, 128, 256, 512, 1024, 2048])
        _xticks = [0, 128, 256, 512, 1024, 2048]
        _yticks = [0, 128, 256, 512, 1024, 2048]

    elif test_case == "nested_0001":
        ctr = qt.Coordinate(x=0.0, y=0.0)
        cell = qt.Cell(center=ctr, size=2.0)
        points = tuple([qt.Coordinate(0.8, 0.8)])
        _xticks = [-2, -1, 0, 1, 2]
        _yticks = _xticks

    elif test_case == "wall_0011":
        ctr = qt.Coordinate(x=0.0, y=0.0)
        cell = qt.Cell(center=ctr, size=2.0)
        points = tuple(
            [
                qt.Coordinate(0.8, 0.8),
                qt.Coordinate(0.8, 0.2),
                qt.Coordinate(0.8, -0.2),
                qt.Coordinate(0.8, -0.8),
            ]
        )
        _xticks = [-2, -1, 0, 1, 2]
        _yticks = _xticks

    elif test_case == "benchmark":
        ctr = qt.Coordinate(x=2.0, y=2.0)
        cell = qt.Cell(center=ctr, size=4.0)
        # circle cut out, boundary must run counterclockwise for winding number defn
        # https://en.wikipedia.org/wiki/Winding_number
        # theta = np.linspace(np.pi, 3.0 * np.pi / 2.0, num=9, endpoint=True)
        theta = np.linspace(3.0 * np.pi / 2.0, np.pi, num=9, endpoint=True)
        x0, y0 = 4.0, 4.0
        xs_seeds = tuple(np.cos(theta) + x0)
        ys_seeds = tuple(np.sin(theta) + y0)
        pairs = tuple(zip(xs_seeds, ys_seeds))
        points = qt.coordinates(pairs=pairs)
        # points = tuple([qt.Coordinate(3.0, 4.0)])
        _xticks = [0, 1, 2, 3, 4]
        _yticks = _xticks

    else:
        ctr = qt.Coordinate(x=0.0, y=0.0)
        cell = qt.Cell(center=ctr, size=1024.0)

        # boundary points
        num_points = 17  # 9 for single density, or 17 for double density
        if test_case == "diagonal":
            bpx = np.linspace(start=-512.0, stop=512.0, num=num_points, endpoint=True)
            bpy = bpx
        else:
            # bpx = (-128.0, -96.0, -64.0, -32.0, 0.0, 32.0, 64.0, 96.0, 128.0)
            bpx = np.linspace(start=-128.0, stop=128.0, num=num_points, endpoint=True)
            # bpy = (-512.0, -384.0, -256.0, -128.0, 0.0, 128.0, 256.0, 384.0, 512.0)
            bpy = np.linspace(start=-512.0, stop=512.0, num=num_points, endpoint=True)

        points = tuple(map(qt.Coordinate, bpx, bpy))
        # ax.set_xticks([-512, -256, -128, 0, 128, 256, 512])
        # ax.set_yticks([-512, -256, -128, 0, 128, 256, 512])
        _xticks = [-512, -256, -128, 0, 128, 256, 512]
        _yticks = [-512, -256, -128, 0, 128, 256, 512]

    tree = qt.QuadTree(cell=cell, level=0, level_max=level_max, points=points)

    quads = tree.quads()
    quad_levels = tree.quad_levels()
    # quad_levels_recursive = tree.quad_levels_recursive()

    # draw remaining L1 through Ln quads
    fig = plt.figure(figsize=(6.0, 6.0), dpi=100)
    ax = fig.gca()

    ax.set_aspect("equal")

    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")

    # ax.set_title(f"level max = {level_max}")
    plt.axis("on")
    ax.set_xticks(_xticks)
    ax.set_yticks(_yticks)

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

    xs_seeds = tuple(point.x for point in points)
    ys_seeds = tuple(point.y for point in points)
    ax.scatter(
        xs_seeds, ys_seeds, linestyle="solid", edgecolor="black", color="tab:red"
    )

    if test_case in ("nested_0001", "wall_0011"):
        # mesh_dual = tree.mesh_dual()
        domain_dual = tree.domain_dual()

        # meshes = tuple(filter(lambda x: x is not None, mesh_dual))

        # for mesh in mesh_dual:
        for domain in domain_dual:

            # coordinates = mesh.coordinates
            # faces = mesh.connectivity
            coordinates = domain.mesh.coordinates
            faces = domain.mesh.connectivity
            xs = tuple(map(lambda item: item.x, coordinates))
            ys = tuple(map(lambda item: item.y, coordinates))

            for face in faces:
                xf = [xs[k] for k in face]
                yf = [ys[k] for k in face]
                plt.fill(
                    xf,
                    yf,
                    linestyle="solid",
                    edgecolor="black",
                    facecolor=colors[0],
                    alpha=0.5,
                )

    if test_case in ("benchmark"):
        domain_dual = tree.domain_dual()

        # merge domains if there are two or more domains
        if len(domain_dual) >= 2:
            aa = 4

        # plot boundary, and only include dual finite elements with cg inside of that
        # boundary
        xs_seeds = tuple(point.x for point in points)
        ys_seeds = tuple(point.y for point in points)
        xs_corners = (0.0, 0.0, 4.0)  # the other three corners
        ys_corners = (4.0, 0.0, 0.0)
        xs_boundary = xs_seeds + xs_corners
        ys_boundary = ys_seeds + ys_corners
        ax.plot(
            xs_boundary, ys_boundary, marker="+", linestyle="dashed", color="tab:orange"
        )

        for domain in domain_dual:
            coordinates = domain.mesh.coordinates
            faces = domain.mesh.connectivity
            xs = tuple(map(lambda item: item.x, coordinates))
            ys = tuple(map(lambda item: item.y, coordinates))

            for face in faces:
                xf = [xs[k] for k in face]
                yf = [ys[k] for k in face]
                xcg = np.mean(xf)
                ycg = np.mean(yf)

                # if all([xcg < xi for xi in xs_boundary]) and all(
                #     [ycg < yi for yi in ys_boundary]
                # ):
                plt.fill(
                    xf,
                    yf,
                    linestyle="solid",
                    edgecolor="black",
                    facecolor=colors[0],
                    alpha=0.5,
                )

    if shown:
        plt.show()

    if serialize:
        extension = ".png"  # ".png" | ".pdf" | ".svg"
        filename = Path(__file__).stem + "_" + test_case + extension
        fig.savefig(filename, bbox_inches="tight", pad_inches=0)
        print(f"Serialized to {filename}")


if __name__ == "__main__":
    main()
