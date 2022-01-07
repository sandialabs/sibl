import math
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

    # mesh
    mesh = xyb.QuadMesh(xs, ys)
    # deciding this loop is : in
    # inCurve with 40 points
    # Determining derivative...
    # Setting tangent and angle...
    # Finding corners...
    # Finding features...
    # Constructor complete

    # compute mesh
    mesh.compute(resolution=1)
    # Computing Mesh
    # Size of my nodes: 0
    # Size of my Primal nodes: 73
    # Size of my Primal Polys: 56
    # Unique loop size: 41

    # get the nodes
    nodes = mesh.nodes()
    # nnp = len(nodes)  # number of nodal points = 161

    # example nodes:
    # the first node:
    # > nodes[0]
    # [1.0, 0.5024999976158142, 0.5024999976158142, 0.0]

    # the second nod
    # > nodes[1]
    # [2.0, 0.5024999976158142, -0.5024999976158142, 0.0]

    # the last node
    # > nodes[-1]
    # [165.0, 1.4841588735580444, 1.0253148078918457, 0.0]

    # create a dictionary lookup table from the index to the nodal (x, y, z)
    # coordinates
    keys = [str(int(n[0])) for n in nodes]
    values = [(n[1], n[2]) for n in nodes]  # collect (x, y) pairs, ignore z value
    zip_iterator = zip(keys, values)
    key_value_dict = dict(zip_iterator)

    # get the elements
    elements = mesh.connectivity()
    # nel = len(elements)  # number of elements = 140

    # work with only three elements for debug purposes
    # elements = elements[0:3]

    # example elements:
    # the first element
    # > elements[0]
    # [1, 57, 58, 59]

    # the second element
    # > elements[1]
    # [57, 2, 60, 58]

    # the last element
    # > elements[-1]
    # [165, 164, 24, 161]

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

    plt.axis("on")

    plt.show()

    # TODO: saving the plot, and writing to a .mesh file


if __name__ == "__main__":
    main()
