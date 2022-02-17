import math
from pathlib import Path

import matplotlib.pyplot as plt

import xybind as xyb


def main():

    n_samples = 40
    radius = 2.0

    # parameterize the curve
    ts = tuple(range(n_samples))

    # create x and y points
    xs = [radius * math.cos(2.0 * math.pi * t / n_samples) for t in ts]
    ys = [radius * math.sin(2.0 * math.pi * t / n_samples) for t in ts]

    # other user-defined parameters
    refine = True  # don't refine at the boundary
    res = 1.0  # the first resolution attempt
    # res = 0.5  # the second resolution attempt
    # res = 0.25  # the third resolution attempt
    ll_x, ll_y = -2.1, -2.1  # ll = lower left
    ur_x, ur_y = 2.1, 2.1  # ur = upper right
    dev_out = False
    ofile = Path(__file__).stem  # automatically get the 'lesson_03' string

    # mesh
    mesh = xyb.QuadMesh()
    mesh.initialize(
        boundary_xs=xs,
        boundary_ys=ys,
        boundary_refine=refine,
        resolution=res,
        lower_bound_x=ll_x,
        lower_bound_y=ll_y,
        upper_bound_x=ur_x,
        upper_bound_y=ur_y,
        developer_output=dev_out,
        output_file=ofile,
    )

    mesh.compute()

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
    # nel = len(elements)  # number of elements

    # visualization
    s = 6.0  # 6.0 inches
    fig = plt.figure(figsize=(s, s))

    ax = fig.gca()

    ax.plot(xs, ys, "-", alpha=0.5)
    ax.plot(xs, ys, ".")

    ix = 0  # the x-coordinate index
    iy = 1  # the y-coordinate index

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
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")

    ax.set_xlim([ll_x, ur_x])
    ax.set_ylim([ll_y, ur_y])

    plt.axis("on")

    plt.show()

    # TODO: saving the plot, and writing to a .mesh file, use the .yml input file


if __name__ == "__main__":
    main()
