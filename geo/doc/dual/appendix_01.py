# from itertools import chain

import matplotlib.pyplot as plt

# import ptg.quadtree as qt
from ptg.point import Points


def main():

    # inputs
    # nsd: int = 2  # number of space dimensions
    n_smoothing_iterations: int = 1
    boundary_shown: bool = True
    figure_shown: bool = True
    axes_shown: bool = True
    xlim = (0.5, 4.5)
    ylim = (0.5, 3.5)
    xticks = (1, 2, 3, 4)
    yticks = (1, 2, 3)
    title = ""  # empty string on default
    xlabel: str = r"$x$"
    ylabel: str = r"$y$"
    dpi: int = 100  # dots per inch

    element_edge_alpha = 1.0
    element_edge_color = "black"
    element_edge_linestyle = "solid"
    element_edge_linewidth = 1.0

    element_face_color = "white"

    boundary_edge_alpha = 0.5
    boundary_edge_color = "tab:blue"
    boundary_edge_linestyle = "dashed"
    boundary_edge_linewidth = 3.0

    boundary_point_alpha = 0.5
    boundary_point_color = "tab:orange"
    boundary_point_linewidth = 0.0
    boundary_point_marker = "."
    boundary_point_markersize = 10

    """
    create a six-element finite element mesh

    ^ y-axis
    |
    |
    3    8----9---10---11
         |    |    |    |
    2    4----5----6----7
         |    |    |    |
    1    0----1----2----3

    0    1    2    3    4  --> x-axis
    """

    p0 = Points(
        pairs=(
            (1.0, 1.0),  # row 1
            (2.0, 1.0),
            (3.0, 1.0),
            (4.0, 1.0),
            (1.0, 2.0),  # row 2
            (2.0 + 0.1, 2.0 + 0.2),
            (3.0, 2.0),
            (4.0, 2.0),
            (1.0, 3.0),  # row 3
            (2.0, 3.0),
            (3.0, 3.0),
            (4.0, 3.0),
        )
    )
    c0 = (
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (4, 5, 9, 8),
        (5, 6, 10, 9),
        (6, 7, 11, 10),
    )

    # edges0 = (
    #     (1, 4),  # row 1
    #     (2, 5, 0),
    #     (3, 6, 1),
    #     (7, 2),
    #     (0, 5, 8),  # row 2
    #     (6, 9, 4, 1),
    #     (7, 10, 5, 2),
    #     (11, 6, 3),
    #     (4, 9),  # row 3
    #     (8, 5, 10),
    #     (9, 6, 11),
    #     (10, 7),
    # )

    # boundaries (only a single boundary in this case, but use tuple of tuples
    # to allow multiple boundaries)
    b0 = ((0, 1, 2, 3, 7, 11, 10, 9, 8, 4),)

    # node_numbers = set(tuple(chain.from_iterable(c0)))
    # boundary_node_numbers = set(tuple(chain.from_iterable(b0)))

    # active_node_numbers = node_numbers - boundary_node_numbers  # as a set

    # active node numbers as a tuple
    # ann = tuple(i for i in active_node_numbers)

    # boundary positions
    xs = [p0.xs[i] for i in b0[0]]
    ys = [p0.ys[i] for i in b0[0]]

    # d0 = qt.Domain(mesh=m0, boundaries=b0)

    # visualization
    s = 6.0  # 6.0 inches
    fig = plt.figure(figsize=(s, s), dpi=dpi)

    ax = fig.gca()

    for iter in range(n_smoothing_iterations + 1):

        # plot elements
        for element in c0:
            element_xs = [p0.xs[node_number] for node_number in element]
            element_ys = [p0.ys[node_number] for node_number in element]
            plt.fill(
                element_xs,
                element_ys,
                alpha=element_edge_alpha,
                edgecolor=element_edge_color,
                facecolor=element_face_color,
                linestyle=element_edge_linestyle,
                linewidth=element_edge_linewidth,
            )

        if boundary_shown:
            # plot interpolated boundary
            ax.plot(
                xs,
                ys,
                alpha=boundary_edge_alpha,
                color=boundary_edge_color,
                linestyle=boundary_edge_linestyle,
                linewidth=boundary_edge_linewidth,
            )
            # plot discrete boundary points
            ax.plot(
                xs,
                ys,
                alpha=boundary_point_alpha,
                color=boundary_point_color,
                linewidth=boundary_point_linewidth,
                marker=boundary_point_marker,
                markersize=boundary_point_markersize,
            )

        ax.set_aspect("equal")

        ax.set_xticks(xticks)
        ax.set_yticks(yticks)

        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

        title = "iteration: " + str(iter)  # mutation
        plt.title(title)

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        if axes_shown:
            plt.axis("on")
        else:
            plt.axis("off")

        if figure_shown:
            plt.show()

        # TODO: saving the plot, and writing to a .mesh file


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
