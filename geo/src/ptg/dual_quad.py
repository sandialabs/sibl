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

#  0000  # "all L0"            <-- unique T0
#  0001  # "single L1"         <-- unique T1
#  0010  #     "single L1" (2)
#  0011  # "half-half"         <-- unique T2

#  0100  #     "single L1" (3)
#  0101  #     "half-half" (2)
#  0110  # "fan"               <-- unique T3
#  0111  # "single L0"         <-- unique T4

#  1000  #     "single L1" (4)
#  1001  #     "fan" (2)
#  1010  #     "half-half" (3)
#  1011  #     "single L0" (2)

#  1100  #     "half-half" (4)
#  1101  #     "single L0" (3)
#  1110  #     "single L0" (4)
#  1111  #  "all L1"           <-- unique T5

# So slots in a 2x2 grid template, 4^2 = 16 configurations, but
# there are only six (6) unique configurations.

# import sys

# from typing import Iterable, NamedTuple, Tuple
from typing import Iterable, NamedTuple
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import rc

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
    "tab:cyan",
)

latex = True
if latex:
    rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
    rc("text", usetex=True)


class Template_0000(NamedTuple):
    """Creates the fully level 0 (L0) data structure.

    Attributes:
        name (str): Four digit binary unique identifier.
        vertices (list[float]): The (x, y) positions of vertices on the unit cube.
        faces (list[float]): The quadrilateral faces
            composed of a sequence of integer node numbers,
            in counter-clockwise (CCW) order, and first node is in the
            lower left corner of the quadrilateral.
        vertices_dual: to come.
        faces_dual: to come.
        ports: to come

    The 0000 pattern and node numbers:

    2---------5---------8
    |         |         |
    |         |         |
    |         |         |
    1---------4---------7
    |         |         |
    |         |         |
    |         |         |
    0---------3---------6

    and with dual node numbers:

    +---------+---------+
    |         |         |
    |    1    |    3    |
    |         |         |
    +---------+---------+
    |         |         |
    |    0    |    2    |
    |         |         |
    +---------+---------+

    where
      "+" is a fully four-valenced node
      "*" is a hanging node, connect to create a four-valence (none for this template)
    """

    name: str = "0000"

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

    vertices_dual: Iterable[Point2D] = (
        (1.0, 1.0),
        (1.0, 3.0),
        (3.0, 1.0),
        (3.0, 3.0),
    )

    faces_dual: Iterable[QuadFace] = ((0, 2, 3, 1),)

    ports: Iterable[Point2D] = (
        (1.0, 0.0),
        (3.0, 0.0),
        (4.0, 1.0),
        (4.0, 3.0),
        (3.0, 4.0),
        (1.0, 4.0),
        (0.0, 3.0),
        (0.0, 1.0),
    )


class Template_0001(NamedTuple):
    """Creates the three level 0 (L0) and one level 1 (L1) data structure.

    The 0001 pattern and node numbers:

    2---------6----9---13
    |         |    |    |
    |         5----8---12
    |         |    |    |
    1---------4----7---11
    |         |         |
    |         |         |
    |         |         |
    0---------3--------10

    and with dual node numbers:

    +---------+----+----+
    |         |  6 |  9 |
    |    1    *----+----+
    |       3 |  5 |  8 |
    +---------+----*----+
    |       2 |  4      |
    |    0    |      7  |
    |         |         |
    +---------+---------+

    where
      "+" is a fully four-valenced node
      "*" is a hanging node, connect to create a four-valence
    """

    name: str = "0001"

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

    vertices_dual: Iterable[Point2D] = (
        (1.0, 1.0),
        (1.0, 3.0),
        (1.667, 1.667),
        (1.667, 2.333),
        (2.333, 1.667),
        (2.5, 2.5),
        (2.5, 3.5),
        (3.0, 1.0),
        (3.5, 2.5),
        (3.5, 3.5),
    )

    faces_dual: Iterable[QuadFace] = (
        (0, 2, 3, 1),
        (0, 7, 4, 2),
        (2, 4, 5, 3),
        (3, 5, 6, 1),
        (4, 7, 8, 5),
        (5, 8, 9, 6),
    )

    ports: Iterable[Point2D] = (
        (1.0, 0.0),
        (3.0, 0.0),
        (4.0, 1.0),
        (4.0, 2.5),
        (4.0, 3.5),
        (3.5, 4.0),
        (2.5, 4.0),
        (1.0, 4.0),
        (0.0, 3.0),
        (0.0, 1.0),
    )


class Template_0011(NamedTuple):
    """Creates the two level 0 (L0) and two level 1 (L1) data structure.

    The 0011 pattern and node numbers:

    2---------7---12---17
    |         |    |    |
    |         6---11---16
    |         |    |    |
    1---------5---10---15
    |         |    |    |
    |         4----9---14
    |         |    |    |
    0---------3----8---13

    and with dual node numbers:

    +---------+----+----+
    |         |  7 | 11 |
    |    1    *----+----+
    |       3 |  6 | 10 |
    +---------+----+----+
    |       2 |  5 |  9 |
    |    0    *----+----+
    |         |  4 |  8 |
    +---------+----+----+

    where
      "+" is a fully four-valenced node
      "*" is a hanging node, connect to create a four-valence
    """

    name: str = "0011"

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

    vertices_dual: Iterable[Point2D] = (
        (1.0, 1.0),
        (1.0, 3.0),
        (1.667, 1.667),
        (1.667, 2.333),
        (2.5, 0.5),
        (2.5, 1.5),
        (2.5, 2.5),
        (2.5, 3.5),
        (3.5, 0.5),
        (3.5, 1.5),
        (3.5, 2.5),
        (3.5, 3.5),
    )

    faces_dual: Iterable[QuadFace] = (
        (0, 2, 3, 1),
        (0, 4, 5, 2),
        (2, 5, 6, 3),
        (3, 6, 7, 1),
        (4, 8, 9, 5),
        (5, 9, 10, 6),
        (6, 10, 11, 7),
    )

    ports: Iterable[Point2D] = (
        (1.0, 0.0),
        (2.5, 0.0),
        (3.5, 0.0),
        (4.0, 0.5),
        (4.0, 1.5),
        (4.0, 2.5),
        (4.0, 3.5),
        (3.5, 4.0),
        (2.5, 4.0),
        (1.0, 4.0),
        (0.0, 3.0),
        (0.0, 1.0),
    )


class Template_0110(NamedTuple):
    """Creates the two level 0 (L0) and two level 1 (L1) data structure in opposition.

    Attributes:
        name (str): Four digit binary unique identifier.
        vertices (list[float]): The (x, y) positions of vertices on the unit cube.
        faces (list[float]): The quadrilateral faces
            composed of a sequence of integer node numbers,
            in counter-clockwise (CCW) order, and first node is in the
            lower left corner of the quadrilateral.

    The 0110 pattern and node numbers:

    3----6---11--------18
    |    |    |         |
    2----5---10         |
    |    |    |         |
    1----4----9---14---17
    |         |    |    |
    |         8---13---16
    |         |    |    |
    0---------7---12---15

    and with dual node numbers:

    +----+----+---------+
    |  2 |  5 |         |
    +----+----*   11    |
    |  1 |  4 | 8       |
    +----*----+----*----+
    |       3 |  7 | 10 |
    |    0    *----+----+
    |         |  6 |  9 |
    +---------+----+----+

    where
      "+" is a fully four-valenced node
      "*" is a hanging node, connect to create a four-valence
    """

    name: str = "0110"

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

    vertices_dual: Iterable[Point2D] = (
        (1.0, 1.0),
        (0.5, 2.5),
        (0.5, 3.5),
        (1.667, 1.667),
        (1.5, 2.5),
        (1.5, 3.5),
        (2.5, 0.5),
        (2.5, 1.5),
        (2.333, 2.333),
        (3.5, 0.5),
        (3.5, 1.5),
        (3.0, 3.0),
    )

    faces_dual: Iterable[QuadFace] = (
        (0, 3, 4, 1),
        (1, 4, 5, 2),
        (0, 6, 7, 3),
        (3, 7, 8, 4),
        (4, 8, 11, 5),
        (6, 9, 10, 7),
        (7, 10, 11, 8),
    )

    ports: Iterable[Point2D] = (
        (1.0, 0.0),
        (2.5, 0.0),
        (3.5, 0.0),
        (4.0, 0.5),
        (4.0, 1.5),
        (4.0, 3.0),
        (3.0, 4.0),
        (1.5, 4.0),
        (0.5, 4.0),
        (0.0, 3.5),
        (0.0, 2.5),
        (0.0, 1.0),
    )


class Template_0111(NamedTuple):
    """Creates the one level 0 (L0) and three level 1 (L1) data structure.

    The 0111 pattern and node numbers:

    3----6---11---16---21
    |    |    |    |    |
    2----5---10---15---20
    |    |    |    |    |
    1----4----9---14---19
    |         |    |    |
    |         8---13---18
    |         |    |    |
    0---------7---12---17

    and with dual node numbers:

    +----+----+----+----+
    |  2 |  5 |  9 | 13 |
    +----+----+----+----+
    |  1 |  4 |  8 | 12 |
    +----*----+----+----+
    |       3 |  7 | 11 |
    |    0    *----+----+
    |         |  6 | 10 |
    +---------+----+----+

    where
      "+" is a fully four-valenced node
      "*" is a hanging node, connect to create a four-valence
    """

    name: str = "0111"

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
        (0, 7, 9, 1),
        (1, 4, 5, 2),
        (2, 5, 6, 3),
        (4, 9, 10, 5),
        (5, 10, 11, 6),
        (7, 12, 13, 8),
        (8, 13, 14, 9),
        (9, 14, 15, 10),
        (10, 15, 16, 11),
        (12, 17, 18, 13),
        (13, 18, 19, 14),
        (14, 19, 20, 15),
        (15, 20, 21, 16),
    )

    vertices_dual: Iterable[Point2D] = (
        (1.0, 1.0),
        (0.5, 2.5),
        (0.5, 3.5),
        (1.667, 1.667),
        (1.5, 2.5),
        (1.5, 3.5),
        (2.5, 0.5),
        (2.5, 1.5),
        (2.5, 2.5),
        (2.5, 3.5),
        (3.5, 0.5),
        (3.5, 1.5),
        (3.5, 2.5),
        (3.5, 3.5),
    )
    faces_dual: Iterable[QuadFace] = (
        (0, 3, 4, 1),
        (1, 4, 5, 2),
        (0, 6, 7, 3),
        (3, 7, 8, 4),
        (4, 8, 9, 5),
        (6, 10, 11, 7),
        (7, 11, 12, 8),
        (8, 12, 13, 9),
    )
    ports: Iterable[Point2D] = (
        (1.0, 0.0),
        (2.5, 0.0),
        (3.5, 0.0),
        (4.0, 0.5),
        (4.0, 1.5),
        (4.0, 2.5),
        (4.0, 3.5),
        (3.5, 4.0),
        (2.5, 4.0),
        (1.5, 4.0),
        (0.5, 4.0),
        (0.0, 3.5),
        (0.0, 2.5),
        (0.0, 1.0),
    )


class Template_1111(NamedTuple):
    """Creates the fully level 1 (L1) data structure.

    The 1111 pattern and node numbers:

    4----9---14---19---24
    |    |    |    |    |
    3----8---13---18---23
    |    |    |    |    |
    2----7---12---17---22
    |    |    |    |    |
    1----6---11---15---21
    |    |    |    |    |
    0----5---10---15---20

    and with dual node numbers:

    +----+----+----+----+
    |  3 |  7 | 11 | 15 |
    +----+----+----+----+
    |  2 |  6 | 10 | 14 |
    +----+----+----+----+
    |  1 |  5 |  9 | 13 |
    +----+----+----+----+
    |  0 |  4 |  8 | 12 |
    +----+----+----+----+

    where
      "+" is a fully four-valenced node
      "*" is a hanging node, connect to create a four-valence (none for this template)
    """

    name: str = "1111"

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

    vertices_dual: Iterable[Point2D] = (
        (0.5, 0.5),
        (0.5, 1.5),
        (0.5, 2.5),
        (0.5, 3.5),
        (1.5, 0.5),
        (1.5, 1.5),
        (1.5, 2.5),
        (1.5, 3.5),
        (2.5, 0.5),
        (2.5, 1.5),
        (2.5, 2.5),
        (2.5, 3.5),
        (3.5, 0.5),
        (3.5, 1.5),
        (3.5, 2.5),
        (3.5, 3.5),
    )
    faces_dual: Iterable[QuadFace] = (
        (0, 4, 5, 1),
        (1, 5, 6, 2),
        (2, 6, 7, 3),
        (4, 8, 9, 5),
        (5, 9, 10, 6),
        (6, 10, 11, 7),
        (8, 12, 13, 9),
        (9, 13, 14, 10),
        (10, 14, 15, 11),
    )
    ports: Iterable[Point2D] = (
        (0.5, 0.0),
        (1.5, 0.0),
        (2.5, 0.0),
        (3.5, 0.0),
        (4.0, 0.5),
        (4.0, 1.5),
        (4.0, 2.5),
        (4.0, 3.5),
        (3.5, 4.0),
        (2.5, 4.0),
        (1.5, 4.0),
        (0.5, 4.0),
        (0.0, 3.5),
        (0.0, 2.5),
        (0.0, 1.5),
        (0.0, 0.5),
    )


def face_as_coordinates(
    face: tuple[int, int, int, int],
    vertices: tuple[tuple[float, float]],
) -> tuple[tuple[float, float], ...]:

    b = tuple(vertices[i] for i in face)
    return b


def plot_template(template, *, dual_shown=False, serialize=False):
    faces_as_points = tuple(
        face_as_coordinates(face, template.vertices) for face in template.faces
    )

    fig = plt.figure(figsize=plt.figaspect(1.0), dpi=100)
    ax = fig.gca()

    for face in faces_as_points:
        xs = [face[i][0] for i in range(len(face))]
        ys = [face[i][1] for i in range(len(face))]
        plt.fill(
            xs, ys, linestyle="dotted", edgecolor="magenta", alpha=0.5, facecolor="gray"
        )

    if dual_shown:
        faces_as_points = tuple(
            face_as_coordinates(face, template.vertices_dual)
            for face in template.faces_dual
        )

        for face in faces_as_points:
            xs = [face[i][0] for i in range(len(face))]
            ys = [face[i][1] for i in range(len(face))]
            plt.fill(
                xs,
                ys,
                linestyle="solid",
                edgecolor="black",
                facecolor=colors[0],
                alpha=0.5,
            )

        xs = [template.ports[i][0] for i in range(len(template.ports))]
        ys = [template.ports[i][1] for i in range(len(template.ports))]
        # ax.plt(xs, ys, "o")
        ax.scatter(
            xs,
            ys,
            edgecolor="black",
            facecolor="white",
            alpha=0.7,
            marker="o",
            s=20,  # markersize
        )
    # ax.set_ylim([0.0 - 2 * _eps, 1.0 + 2 * _eps])

    # ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)

    ax.set_aspect("equal")
    # ax.grid(True, which="major", linestyle="-")
    # ax.grid(True, which="minor", linestyle=":")

    # ax.xaxis.set_major_locator(MultipleLocator(1.0))
    # ax.xaxis.set_minor_locator(MultipleLocator(0.25))
    # ax.yaxis.set_major_locator(MultipleLocator(1.0))
    # ax.yaxis.set_minor_locator(MultipleLocator(0.25))

    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")

    ax.set_xticks([0, 1, 2, 3, 4])
    ax.set_yticks([0, 1, 2, 3, 4])

    plt.show()

    if serialize:

        extension = "_" + template.name + ".png"  # or '.svg'
        filename = Path(__file__).stem + extension
        fig.savefig(filename, bbox_inches="tight", pad_inches=0)
        print(f"Serialized to {filename}")


def main():

    plot_template(Template_0000(), dual_shown=True, serialize=True)
    plot_template(Template_0001(), dual_shown=True, serialize=True)
    plot_template(Template_0011(), dual_shown=True, serialize=True)
    plot_template(Template_0110(), dual_shown=True, serialize=True)
    plot_template(Template_0111(), dual_shown=True, serialize=True)
    plot_template(Template_1111(), dual_shown=True, serialize=True)


if __name__ == "__main__":
    main()
