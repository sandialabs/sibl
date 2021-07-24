# L0 refinement is the base level
# L1 refinement is refined 1x relative to 0 refinement
#
# Consider a 2x2 grid template, composed of either L0 or L1 squares.
# For each of the four grid spaces of the 2x2 grid can be composed
# of either the L0 (one square) or L1 (four small squares).
# There are 2^4 = 16 variations, but not of all these are unique.
#
# Let the x-axis be the major axis, and y-axis be the minor axis.
# Then the array of fills for the 2x2 grid is
# 0 -> L0, 1 -> L1
#
# (x0, y0), (x0, y1), (x1, y0), (x1, y1)

#  0000  # "all L0"            <-- unique
#  0001  # "single L1"         <-- unique
#  0010  #     "single L1" (2)
#  0011  # "half-half"         <-- unique

#  0100  #     "single L1" (3)
#  0101  #     "half-half" (2)
#  0110  # "fan"               <-- unique
#  0111  # "single L0"         <-- unique

#  1000  #     "single L1" (4)
#  1001  #     "fan" (2)
#  1010  #     "half-half" (3)
#  1011  #     "single L0" (2)

#  1100  #     "half-half" (4)
#  1101  #     "single L0" (3)
#  1110  #     "single L0" (4)
#  1111  #  "all L1"           <-- unique

# So slots in a 2x2 grid template, 4^2 = 16 configurations, but
# there are only six (6) unique configurations.

# import sys

# from typing import Iterable, NamedTuple, Tuple
from typing import Iterable, NamedTuple
import matplotlib.pyplot as plt

# from matplotlib.ticker import MultipleLocator
# from matplotlib.patches import Polygon

# import numpy as np


# TODO: implement a base class Template
# class Template(NamedTuple):
#     vertices: tuple[tuple[float, float]]
#     faces: tuple[tuple[int, int, int, int]]

# Type alias
# https://docs.python.org/3/library/typing.html#type-aliases
Point2D = tuple[float, float]
QuadFace = tuple[int, int, int, int]


class Template_0000(NamedTuple):
    """Creates the fully level 0 (L0) data structure.

    The 0000 pattern:

    *-----*-----*
    |     |     |
    |     |     |
    |     |     |
    *-----*-----*
    |     |     |
    |     |     |
    |     |     |
    *-----*-----*

    Attributes:
        vertices (list[float]): The (x, y) positions of vertices on the unit cube.
        faces (list[float]): The quadrilateral faces
            composed of a sequence of integer node numbers,
            in counter-clockwise (CCW) order, and first node is in the
            lower left corner of the quadrilateral.
    """

    # vertices: tuple[tuple[float, float], ...] = (
    vertices: Iterable[Point2D] = (
        (0.0, 0.0),
        (0.0, 2.0),
        (0.0, 4.0),
        (2.0, 0.0),
        (2.0, 2.0),
        (2.0, 4.0),
        (4.0, 0.0),
        (4.0, 2.0),
        (4.0, 4.0),
    )

    # faces: tuple[tuple[int, int, int, int], ...] = (
    faces: Iterable[QuadFace] = (
        (0, 3, 4, 1),
        (1, 4, 5, 2),
        (3, 6, 7, 4),
        (4, 7, 8, 5),
    )


class Template_0001(NamedTuple):
    """Creates the three level 0 (L0) and one level 1 (L1) data structure.

    The 0001 pattern:

    *-----*--*--*
    |     |  |  |
    |     *--*--*
    |     |  |  |
    *-----*--*--*
    |     |     |
    |     |     |
    |     |     |
    *-----*-----*

    with node numbers:

    2   6 9 13
        5 8 12
    1   4 7 11

    0   3   10

    Attributes:
        vertices (list[float]): The (x, y) positions of vertices on the unit cube.
        faces (list[float]): The quadrilateral faces
            composed of a sequence of integer node numbers,
            in counter-clockwise (CCW) order, and first node is in the
            lower left corner of the quadrilateral.
    """

    # vertices: tuple[tuple[float, float], ...] = (
    vertices: Iterable[Point2D] = (
        (0.0, 0.0),
        (0.0, 2.0),
        (0.0, 4.0),
        (2.0, 0.0),
        (2.0, 2.0),
        (2.0, 3.0),
        (2.0, 4.0),
        (3.0, 2.0),
        (3.0, 3.0),
        (3.0, 4.0),
        (4.0, 0.0),
        (4.0, 2.0),
        (4.0, 3.0),
        (4.0, 4.0),
    )

    # faces: tuple[tuple[int, int, int, int], ...] = (
    faces: Iterable[QuadFace] = (
        (0, 3, 4, 1),
        (1, 4, 6, 2),
        (3, 10, 11, 4),
        (4, 7, 8, 5),
        (5, 8, 9, 6),
        (7, 11, 12, 8),
        (8, 12, 13, 9),
    )


class Template_0011(NamedTuple):
    """Creates the two level 0 (L0) and two level 1 (L1) data structure.

    The 0011 pattern:

    *-----*--*--*
    |     |  |  |
    |     *--*--*
    |     |  |  |
    *-----*--*--*
    |     |  |  |
    |     *--*--*
    |     |  |  |
    *-----*--*--*

    with node numbers:

    2   7 12 17
        6 11 16
    1   5 10 15
        4  9 14
    0   3  8 13

    Attributes:
        vertices (list[float]): The (x, y) positions of vertices on the unit cube.
        faces (list[float]): The quadrilateral faces
            composed of a sequence of integer node numbers,
            in counter-clockwise (CCW) order, and first node is in the
            lower left corner of the quadrilateral.
    """

    # vertices: tuple[tuple[float, float], ...] = (
    vertices: Iterable[Point2D] = (
        (0.0, 0.0),
        (0.0, 2.0),
        (0.0, 4.0),
        (2.0, 0.0),
        (2.0, 1.0),
        (2.0, 2.0),
        (2.0, 3.0),
        (2.0, 4.0),
        (3.0, 0.0),
        (3.0, 1.0),
        (3.0, 2.0),
        (3.0, 3.0),
        (3.0, 4.0),
        (4.0, 0.0),
        (4.0, 1.0),
        (4.0, 2.0),
        (4.0, 3.0),
        (4.0, 4.0),
    )

    # faces: tuple[tuple[int, int, int, int], ...] = (
    faces: Iterable[QuadFace] = (
        (0, 3, 5, 1),
        (1, 5, 7, 2),
        (3, 8, 9, 4),
        (4, 9, 10, 5),
        (5, 10, 11, 6),
        (6, 11, 12, 7),
        (8, 13, 14, 9),
        (9, 14, 15, 10),
        (10, 15, 16, 11),
        (11, 16, 17, 12),
    )


class Template_0110(NamedTuple):
    """Creates the two level 0 (L0) and two level 1 (L1) data structure in opposition.

    The 0110 pattern:

    *--*--*-----*
    |  |  |     |
    *--*--*     |
    |  |  |     |
    *--*--*--*--*
    |     |  |  |
    |     *--*--*
    |     |  |  |
    *-----*--*--*

    with node numbers:

    3 6 11    18
    2 5 10
    1 4  9 14 17
         8 13 16
    0    7 12 15

    Attributes:
        vertices (list[float]): The (x, y) positions of vertices on the unit cube.
        faces (list[float]): The quadrilateral faces
            composed of a sequence of integer node numbers,
            in counter-clockwise (CCW) order, and first node is in the
            lower left corner of the quadrilateral.
    """

    # vertices: tuple[tuple[float, float], ...] = (
    vertices: Iterable[Point2D] = (
        (0.0, 0.0),
        (0.0, 2.0),
        (0.0, 3.0),
        (0.0, 4.0),
        (1.0, 2.0),
        (1.0, 3.0),
        (1.0, 4.0),
        (2.0, 0.0),
        (2.0, 1.0),
        (2.0, 2.0),
        (2.0, 3.0),
        (2.0, 4.0),
        (3.0, 0.0),
        (3.0, 1.0),
        (3.0, 2.0),
        (4.0, 0.0),
        (4.0, 1.0),
        (4.0, 2.0),
        (4.0, 4.0),
    )

    # faces: tuple[tuple[int, int, int, int], ...] = (
    faces: Iterable[QuadFace] = (
        (0, 7, 9, 1),
        (1, 4, 5, 2),
        (2, 5, 6, 3),
        (4, 9, 10, 5),
        (5, 10, 11, 6),
        (7, 12, 13, 8),
        (8, 13, 14, 9),
        (12, 15, 16, 13),
        (13, 16, 17, 14),
        (9, 17, 18, 11),
    )


class Template_1111(NamedTuple):
    """Creates the fully level 1 (L1) data structure.

    The 1111 pattern:

    *--*--*--*--*
    |  |  |  |  |
    *--*--*--*--*
    |  |  |  |  |
    *--*--*--*--*
    |  |  |  |  |
    *--*--*--*--*
    |  |  |  |  |
    *--*--*--*--*

    with node numbers:

    4 9 14 19 24
    3 8 13 18 23
    2 7 12 17 22
    1 6 11 16 21
    0 5 10 15 20

    Attributes:
        vertices (list[float]): The (x, y) positions of vertices on the unit cube.
        faces (list[float]): The quadrilateral faces
            composed of a sequence of integer node numbers,
            in counter-clockwise (CCW) order, and first node is in the
            lower left corner of the quadrilateral.
    """

    # vertices: tuple[tuple[float, float], ...] = (
    vertices: Iterable[Point2D] = (
        (0.0, 0.0),
        (0.0, 1.0),
        (0.0, 2.0),
        (0.0, 3.0),
        (0.0, 4.0),
        (1.0, 0.0),
        (1.0, 1.0),
        (1.0, 2.0),
        (1.0, 3.0),
        (1.0, 4.0),
        (2.0, 0.0),
        (2.0, 1.0),
        (2.0, 2.0),
        (2.0, 3.0),
        (2.0, 4.0),
        (3.0, 0.0),
        (3.0, 1.0),
        (3.0, 2.0),
        (3.0, 3.0),
        (3.0, 4.0),
        (4.0, 0.0),
        (4.0, 1.0),
        (4.0, 2.0),
        (4.0, 3.0),
        (4.0, 4.0),
    )

    # faces: tuple[tuple[int, int, int, int], ...] = (
    faces: Iterable[QuadFace] = (
        (0, 5, 6, 1),
        (1, 6, 7, 2),
        (2, 7, 8, 3),
        (3, 8, 9, 4),
        (5, 10, 11, 6),
        (6, 11, 12, 7),
        (7, 12, 13, 8),
        (8, 13, 14, 9),
        (10, 15, 16, 11),
        (11, 16, 17, 12),
        (12, 17, 18, 13),
        (13, 18, 19, 14),
        (15, 20, 21, 16),
        (16, 21, 22, 17),
        (17, 22, 23, 18),
        (18, 23, 24, 19),
    )


def face_as_coordinates(
    face: tuple[int, int, int, int],
    vertices: tuple[tuple[float, float]],
) -> tuple[tuple[float, float], ...]:

    b = tuple(vertices[i] for i in face)
    return b


def plot_template(template):
    faces_as_points = tuple(
        face_as_coordinates(face, template.vertices) for face in template.faces
    )

    fig = plt.figure(figsize=plt.figaspect(1.0), dpi=100)
    ax = fig.gca()

    for face in faces_as_points:
        xs = [face[i][0] for i in range(len(face))]
        ys = [face[i][1] for i in range(len(face))]
        plt.fill(
            xs, ys, linestyle="dashed", edgecolor="blue", alpha=0.5, facecolor="gray"
        )

    # verts = ((0, 0), (1, 0), (1, 2), (0, 1))
    # xs = [verts[i][0] for i in range(len(verts))]
    # ys = [verts[i][1] for i in range(len(verts))]

    # poly = Polygon(verts, facecolor="red", edgecolor="blue")
    # ax.add_patch(poly)
    # plt.fill(xs, ys, linestyle="dashed", edgecolor="red", alpha=0.5, facecolor="gray")

    # ax.set_ylim([0.0 - 2 * _eps, 1.0 + 2 * _eps])

    # ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)

    ax.set_aspect("equal")
    # ax.grid(True, which="major", linestyle="-")
    # ax.grid(True, which="minor", linestyle=":")

    # ax.xaxis.set_major_locator(MultipleLocator(1.0))
    # ax.xaxis.set_minor_locator(MultipleLocator(0.25))
    # ax.yaxis.set_major_locator(MultipleLocator(1.0))
    # ax.yaxis.set_minor_locator(MultipleLocator(0.25))

    ax.set_xlabel(r"x")
    ax.set_ylabel(r"y")

    # ax.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
    # ax.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])

    plt.show()


def main():
    T0 = Template_0000()
    plot_template(T0)

    T1 = Template_0001()
    plot_template(T1)

    T2 = Template_0011()
    plot_template(T2)

    T3 = Template_0110()
    plot_template(T3)

    T5 = Template_1111()
    plot_template(T5)


if __name__ == "__main__":
    main()
