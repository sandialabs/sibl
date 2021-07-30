# L0 refinement is the base level
# L1 refinement is refined 1x relative to the 0 base level
#
# Consider a 2x2 grid template, composed of either L0 or L1 squares.
# For each of the four grid spaces of the 2x2 grid can be composed
# of either the L0 (one square) or L1 (four small squares).
# There are 2^4 = 16 variations, but only six variations are unique,
# as shown below.
#
# Let the x-axis be the major axis, and y-axis be the minor axis.
# Then the array of fills for the 2x2 grid is
# 0 -> L0, 1 -> L1
#
# SW,       NW,       SE,       NE
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

from typing import NamedTuple

# TODO: Inherit ABC to assure interface same across all templates.

# Type alias for functional style methods
# https://docs.python.org/3/library/typing.html#type-aliases
Coordinate = tuple[float, float]

Vertex = Coordinate

Face = tuple[int, int, int, int]

Port = Coordinate


class Template_Base(NamedTuple):
    """The base data type for all Templates.

    Attributes:
        name: Four digit binary unique identifier, as a unique string.
        vertices: The (x, y) positions of vertices on the primal mesh.
        faces: The faces composing the primal mesh.  Face nodes are identified
            in counter-clockwise (CCW) order, and first node is in the
            lower left corner of the quadrilateral.
        vertices_dual: The (x, y) positions of vertices on the dual mesh.
        faces_dual: The faces composing the dual mesh.  Ordering rules are the same
            as for the primal mesh (above).
        ports: The (x, y) positions of admissible template-to-template connections.
            When two templated are jointed, a set of ports on an edge of a template
            much match with the set of ports on the edge of an adjoining template.
    """

    name: str
    vertices: tuple[Vertex, ...]
    faces: tuple[Face, ...]
    vertices_dual: tuple[Vertex, ...]
    faces_dual: tuple[Face, ...]
    ports: tuple[Port, ...]


class Template_0000(NamedTuple):
    """Creates the fully level 0 (L0) data structure.

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

    vertices: tuple[Vertex, ...] = (
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

    vertices_revalence = None

    faces: tuple[Face, ...] = (
        (0, 3, 4, 1),
        (1, 4, 5, 2),
        (3, 6, 7, 4),
        (4, 7, 8, 5),
    )

    vertices_dual: tuple[Vertex, ...] = (
        (1.0, 1.0),
        (1.0, 3.0),
        (3.0, 1.0),
        (3.0, 3.0),
    )

    faces_dual: tuple[Face, ...] = ((0, 2, 3, 1),)

    ports: tuple[Port, ...] = (
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

    vertices: tuple[Vertex, ...] = (
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

    vertices_revalence: tuple[tuple[Vertex, ...]] = (
        (
            (2.0, 3.0),
            (1.0, 2.0),
            (2.0, 1.0),
            (3.0, 2.0),
        ),
    )

    faces: tuple[Face, ...] = (
        (0, 3, 4, 1),
        (1, 4, 6, 2),
        (3, 10, 11, 4),
        (4, 7, 8, 5),
        (5, 8, 9, 6),
        (7, 11, 12, 8),
        (8, 12, 13, 9),
    )

    vertices_dual: tuple[Vertex, ...] = (
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

    faces_dual: tuple[Face, ...] = (
        (0, 2, 3, 1),
        (0, 7, 4, 2),
        (2, 4, 5, 3),
        (3, 5, 6, 1),
        (4, 7, 8, 5),
        (5, 8, 9, 6),
    )

    ports: tuple[Port, ...] = (
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

    vertices: tuple[Vertex, ...] = (
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

    vertices_revalence: tuple[tuple[Vertex, ...]] = (
        (
            (2.0, 3.0),
            (1.0, 2.0),
            (2.0, 1.0),
        ),
    )

    faces: tuple[Face, ...] = (
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

    vertices_dual: tuple[Vertex, ...] = (
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

    faces_dual: tuple[Face, ...] = (
        (0, 2, 3, 1),
        (0, 4, 5, 2),
        (2, 5, 6, 3),
        (3, 6, 7, 1),
        (4, 8, 9, 5),
        (5, 9, 10, 6),
        (6, 10, 11, 7),
    )

    ports: tuple[Port, ...] = (
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

    vertices: tuple[Vertex, ...] = (
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

    vertices_revalence: tuple[tuple[Vertex, ...], ...] = (
        (
            (1.0, 2.0),
            (2.0, 1.0),
        ),
        (
            (3.0, 2.0),
            (2.0, 3.0),
        ),
    )

    faces: tuple[Face, ...] = (
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

    vertices_dual: tuple[Vertex, ...] = (
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

    faces_dual: tuple[Face, ...] = (
        (0, 3, 4, 1),
        (1, 4, 5, 2),
        (0, 6, 7, 3),
        (3, 7, 8, 4),
        (4, 8, 11, 5),
        (6, 9, 10, 7),
        (7, 10, 11, 8),
    )

    ports: tuple[Port, ...] = (
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

    vertices: tuple[Vertex, ...] = (
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

    vertices_revalence: tuple[tuple[Vertex, ...]] = (
        (
            (1.0, 2.0),
            (2.0, 1.0),
        ),
    )

    faces: tuple[Face, ...] = (
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

    vertices_dual: tuple[Vertex, ...] = (
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

    faces_dual: tuple[Face, ...] = (
        (0, 3, 4, 1),
        (1, 4, 5, 2),
        (0, 6, 7, 3),
        (3, 7, 8, 4),
        (4, 8, 9, 5),
        (6, 10, 11, 7),
        (7, 11, 12, 8),
        (8, 12, 13, 9),
    )

    ports: tuple[Port, ...] = (
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

    vertices: tuple[Vertex, ...] = (
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

    vertices_revalence = None

    faces: tuple[Face, ...] = (
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

    vertices_dual: tuple[Vertex, ...] = (
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

    faces_dual: tuple[Face, ...] = (
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

    ports: tuple[Port, ...] = (
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
