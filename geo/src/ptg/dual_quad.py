# L0 refinement is the base quad level, a singleton, the entire domain
# * full L1 refinement of L0 creates 2x2 = 4 quads
# * full L2 refinement of L0 creates 4x4 = 16 quads
# * full L3 refinement of L0 creates 8x8 = 64 quads
#
# Consider a 2x2 grid template, composed of either L1 or L2 squares.
# For each of the four grid spaces of the 2x2 grid can be composed
# of either the L1 (one square) or L2 (four small squares).
# There are 2^4 = 16 variations, but only six variations are unique,
# as shown below.
#
# Let the x-axis be the major axis, and y-axis be the minor axis.
# Then the array of fills for the 2x2 grid is
# 0 -> L1, 1 -> L2
#
# SW,       NW,       SE,       NE
# (x0, y0), (x0, y1), (x1, y0), (x1, y1)

#  0000  # "all L1"            <-- unique T0
#  0001  # "single L2"         <-- unique T1
#  0010  #     "single L2" (2)
#  0011  # "half-half"         <-- unique T2

#  0100  #     "single L2" (3)
#  0101  #     "half-half" (2)
#  0110  # "fan"               <-- unique T3
#  0111  # "single L1"         <-- unique T4

#  1000  #     "single L2" (4)
#  1001  #     "fan" (2)
#  1010  #     "half-half" (3)
#  1011  #     "single L1" (2)

#  1100  #     "half-half" (4)
#  1101  #     "single L1" (3)
#  1110  #     "single L1" (4)
#  1111  #  "all L2"           <-- unique T5

# So slots in a 2x2 grid template, 4^2 = 16 configurations, but
# there are only six (6) unique configurations.

from typing import NamedTuple

import math

# TODO: Inherit ABC to assure interface same across all templates.

# Type alias for functional style methods
# https://docs.python.org/3/library/typing.html#type-aliases
Coordinate = tuple[float, float]

Vertex = Coordinate

Face = tuple[int, int, int, int]

Port = Coordinate


def rotate(ref: tuple[Vertex, ...], angle: float) -> tuple[Vertex, ...]:
    """Rotates about the origin an amount of angle (degrees) a tuple of points
    in the reference position to a new position.

    Attributes:
        ref (tuple[Vertex, ...]): The tuple of (x, y) coordinates in the reference
            configurations, e.g., ((x0, y0), (x1, y1), ... (xn, yn)).
        angle (float): The magnitude of rotation in degrees about the origin.

    Returns:
        new (tuple[Vertex, ...]):  The new positions of the ref coordinates, now
            rotated about the origin by an angle (in degrees).
    """

    xs = tuple(ref[k][0] for k in range(len(ref)))
    ys = tuple(ref[k][1] for k in range(len(ref)))

    xnew = tuple(
        xs[k] * math.cos(angle * math.pi / 180.0)
        - ys[k] * math.sin(angle * math.pi / 180.0)
        for k in range(len(xs))
    )

    ynew = tuple(
        xs[k] * math.sin(angle * math.pi / 180.0)
        + ys[k] * math.cos(angle * math.pi / 180.0)
        for k in range(len(ys))
    )

    new = tuple((xnew[k], ynew[k]) for k in range(len(ref)))
    return new


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
    """Creates the fully level 1 (L1) data structure.

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
        (-1.0, -1.0),
        (-1.0, 0.0),
        (-1.0, 1.0),
        (0.0, -1.0),
        (0.0, 0.0),
        (0.0, 1.0),
        (1.0, -1.0),
        (1.0, 0.0),
        (1.0, 1.0),
    )

    vertices_revalence = None

    faces: tuple[Face, ...] = (
        (0, 3, 4, 1),
        (1, 4, 5, 2),
        (3, 6, 7, 4),
        (4, 7, 8, 5),
    )

    vertices_dual: tuple[Vertex, ...] = (
        (-0.5, -0.5),
        (-0.5, 0.5),
        (0.5, -0.5),
        (0.5, 0.5),
    )

    faces_dual: tuple[Face, ...] = ((0, 2, 3, 1),)

    ports: tuple[Port, ...] = (
        (-0.5, -1.0),
        (0.5, -1.0),
        (1.0, -0.5),
        (1.0, 0.5),
        (0.5, 1.0),
        (-0.5, 1.0),
        (-1.0, 0.5),
        (-1.0, -0.5),
    )


class Template_0001(NamedTuple):
    """Creates the three level 1 (L1) and one level 2 (L2) data structure.

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
        (-1.0, -1.0),
        (-1.0, 0.0),
        (-1.0, 1.0),
        (0.0, -1.0),
        (0.0, 0.0),
        (0.0, 0.5),
        (0.0, 1.0),
        (0.5, 0.0),
        (0.5, 0.5),
        (0.5, 1.0),
        (1.0, -1.0),
        (1.0, 0.0),
        (1.0, 0.5),
        (1.0, 1.0),
    )

    vertices_revalence: tuple[tuple[Vertex, ...]] = (
        (
            (0.0, 0.5),
            (-0.5, 0.0),
            (0.0, -0.5),
            (0.5, 0.0),
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
        (-0.5, -0.5),
        (-0.5, 0.5),
        (-0.1665, -0.1665),
        (-0.1665, 0.1665),
        (0.1665, -0.1665),
        (0.25, 0.25),
        (0.25, 0.75),
        (0.5, -0.5),
        (0.75, 0.25),
        (0.75, 0.75),
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
        (-0.5, -1.0),
        (0.5, -1.0),
        (1.0, -0.5),
        (1.0, 0.25),
        (1.0, 0.75),
        (0.75, 1.0),
        (0.25, 1.0),
        (-0.5, 1.0),
        (-1.0, 0.5),
        (-1.0, -0.5),
    )


class Template_0010(NamedTuple):
    """This is a non-unique template, visualized as the unique 0001 template,
    rotated -90 degrees (90 degrees clockwise rotation).
    """

    name: str = "0010"

    _base = Template_0001()
    _angles = tuple(-90.0 for _ in range(len(_base.vertices_revalence)))

    vertices: tuple[Vertex, ...] = rotate(ref=_base.vertices, angle=-90.0)

    vertices_revalence = tuple(map(rotate, _base.vertices_revalence, _angles))

    faces: tuple[Face, ...] = _base.faces

    vertices_dual: tuple[Vertex, ...] = rotate(ref=_base.vertices_dual, angle=-90.0)

    faces_dual: tuple[Face, ...] = _base.faces_dual

    ports: tuple[Vertex, ...] = rotate(ref=_base.ports, angle=-90.0)


class Template_0100(NamedTuple):
    """This is a non-unique template, visualized as the unique 0001 template,
    rotated 90 degrees (90 degrees counter clockwise rotation).
    """

    name: str = "0100"

    _base = Template_0001()
    _angles = tuple(90.0 for _ in range(len(_base.vertices_revalence)))

    vertices: tuple[Vertex, ...] = rotate(ref=_base.vertices, angle=90.0)

    vertices_revalence = tuple(map(rotate, _base.vertices_revalence, _angles))

    faces: tuple[Face, ...] = _base.faces

    vertices_dual: tuple[Vertex, ...] = rotate(ref=_base.vertices_dual, angle=90.0)

    faces_dual: tuple[Face, ...] = _base.faces_dual

    ports: tuple[Vertex, ...] = rotate(ref=_base.ports, angle=90.0)


class Template_1000(NamedTuple):
    """This is a non-unique template, visualized as the unique 0001 template,
    rotated 180 degrees (180 degrees counter clockwise rotation).
    """

    name: str = "1000"

    _base = Template_0001()
    _angles = tuple(180.0 for _ in range(len(_base.vertices_revalence)))

    vertices: tuple[Vertex, ...] = rotate(ref=_base.vertices, angle=180.0)

    vertices_revalence = tuple(map(rotate, _base.vertices_revalence, _angles))

    faces: tuple[Face, ...] = _base.faces

    vertices_dual: tuple[Vertex, ...] = rotate(ref=_base.vertices_dual, angle=180.0)

    faces_dual: tuple[Face, ...] = _base.faces_dual

    ports: tuple[Vertex, ...] = rotate(ref=_base.ports, angle=180.0)


class Template_0011(NamedTuple):
    """Creates the two level 1 (L1) and two level 2 (L2) data structure.

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
        (-1.0, -1.0),
        (-1.0, 0.0),
        (-1.0, 1.0),
        (0.0, -1.0),
        (0.0, -0.5),
        (0.0, 0.0),
        (0.0, 0.5),
        (0.0, 1.0),
        (0.5, -1.0),
        (0.5, -0.5),
        (0.5, 0.0),
        (0.5, 0.5),
        (0.5, 1.0),
        (1.0, -1.0),
        (1.0, -0.5),
        (1.0, 0.0),
        (1.0, 0.5),
        (1.0, 1.0),
    )

    vertices_revalence: tuple[tuple[Vertex, ...]] = (
        (
            (0.0, 0.5),
            (-0.5, 0.0),
            (0.0, -0.5),
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
        (-0.5, -0.5),
        (-0.5, 0.5),
        (-0.1665, -0.1665),
        (-0.1665, 0.1665),
        (0.25, -0.75),
        (0.25, -0.25),
        (0.25, 0.25),
        (0.25, 0.75),
        (0.75, -0.75),
        (0.75, -0.25),
        (0.75, 0.25),
        (0.75, 0.75),
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
        (-0.5, -1.0),
        (0.25, -1.0),
        (0.75, -1.0),
        (1.0, -0.75),
        (1.0, -0.25),
        (1.0, 0.25),
        (1.0, 0.75),
        (0.75, 1.0),
        (0.25, 1.0),
        (-0.5, 1.0),
        (-1.0, 0.5),
        (-1.0, -0.5),
    )


class Template_0101(NamedTuple):
    """This is a non-unique template, visualized as the unique 0011 template,
    rotated 90 degrees (90 degrees counter clockwise rotation).
    """

    name: str = "0101"

    _base = Template_0011()
    _angles = tuple(90.0 for _ in range(len(_base.vertices_revalence)))

    vertices: tuple[Vertex, ...] = rotate(ref=_base.vertices, angle=90.0)

    vertices_revalence = tuple(map(rotate, _base.vertices_revalence, _angles))

    faces: tuple[Face, ...] = _base.faces

    vertices_dual: tuple[Vertex, ...] = rotate(ref=_base.vertices_dual, angle=90.0)

    faces_dual: tuple[Face, ...] = _base.faces_dual

    ports: tuple[Vertex, ...] = rotate(ref=_base.ports, angle=90.0)


class Template_1010(NamedTuple):
    """This is a non-unique template, visualized as the unique 0011 template,
    rotated -90 degrees (90 degrees clockwise rotation).
    """

    name: str = "1010"

    _base = Template_0011()
    _angles = tuple(-90.0 for _ in range(len(_base.vertices_revalence)))

    vertices: tuple[Vertex, ...] = rotate(ref=_base.vertices, angle=-90.0)

    vertices_revalence = tuple(map(rotate, _base.vertices_revalence, _angles))

    faces: tuple[Face, ...] = _base.faces

    vertices_dual: tuple[Vertex, ...] = rotate(ref=_base.vertices_dual, angle=-90.0)

    faces_dual: tuple[Face, ...] = _base.faces_dual

    ports: tuple[Vertex, ...] = rotate(ref=_base.ports, angle=-90.0)


class Template_1100(NamedTuple):
    """This is a non-unique template, visualized as the unique 0011 template,
    rotated 180 degrees (180 degrees counter clockwise rotation).
    """

    name: str = "1100"

    _base = Template_0011()
    _angles = tuple(180.0 for _ in range(len(_base.vertices_revalence)))

    vertices: tuple[Vertex, ...] = rotate(ref=_base.vertices, angle=180.0)

    vertices_revalence = tuple(map(rotate, _base.vertices_revalence, _angles))

    faces: tuple[Face, ...] = _base.faces

    vertices_dual: tuple[Vertex, ...] = rotate(ref=_base.vertices_dual, angle=180.0)

    faces_dual: tuple[Face, ...] = _base.faces_dual

    ports: tuple[Vertex, ...] = rotate(ref=_base.ports, angle=180.0)


class Template_0110(NamedTuple):
    """Creates the two level 1 (L1) and two level 2 (L2) data structure in opposition.

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
        (-1.0, -1.0),
        (-1.0, 0.0),
        (-1.0, 0.5),
        (-1.0, 1.0),
        (-0.5, 0.0),
        (-0.5, 0.5),
        (-0.5, 1.0),
        (0.0, -1.0),
        (0.0, -0.5),
        (0.0, 0.0),
        (0.0, 0.5),
        (0.0, 1.0),
        (0.5, -1.0),
        (0.5, -0.5),
        (0.5, 0.0),
        (1.0, -1.0),
        (1.0, -0.5),
        (1.0, 0.0),
        (1.0, 1.0),
    )

    vertices_revalence: tuple[tuple[Vertex, ...], ...] = (
        (
            (-0.5, 0.0),
            (0.0, -0.5),
        ),
        (
            (0.5, 0.0),
            (0.0, 0.5),
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
        (-0.5, -0.5),
        (-0.75, 0.25),
        (-0.75, 0.75),
        (-0.1665, -0.1665),
        (-0.25, 0.25),
        (-0.25, 0.75),
        (0.25, -0.75),
        (0.25, -0.25),
        (0.1665, 0.1665),
        (0.75, -0.75),
        (0.75, -0.25),
        (0.5, 0.5),
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
        (-0.5, -1.0),
        (0.25, -1.0),
        (0.75, -1.0),
        (1.0, -0.75),
        (1.0, -0.25),
        (1.0, 0.5),
        (0.5, 1.0),
        (-0.25, 1.0),
        (-0.75, 1.0),
        (-1.0, 0.75),
        (-1.0, 0.25),
        (-1.0, -0.5),
    )


class Template_1001(NamedTuple):
    """This is a non-unique template, visualized as the unique 0111 template,
    rotated 90 degrees (90 degrees counter clockwise rotation).
    """

    name: str = "1001"

    _base = Template_0110()
    _angles = tuple(90.0 for _ in range(len(_base.vertices_revalence)))

    vertices: tuple[Vertex, ...] = rotate(ref=_base.vertices, angle=90.0)

    vertices_revalence = tuple(map(rotate, _base.vertices_revalence, _angles))

    faces: tuple[Face, ...] = _base.faces

    vertices_dual: tuple[Vertex, ...] = rotate(ref=_base.vertices_dual, angle=90.0)

    faces_dual: tuple[Face, ...] = _base.faces_dual

    ports: tuple[Vertex, ...] = rotate(ref=_base.ports, angle=90.0)


class Template_0111(NamedTuple):
    """Creates the one level 1 (L1) and three level 2 (L2) data structure.

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
        (-1.0, -1.0),
        (-1.0, 0.0),
        (-1.0, 0.5),
        (-1.0, 1.0),
        (-0.5, 0.0),
        (-0.5, 0.5),
        (-0.5, 1.0),
        (0.0, -1.0),
        (0.0, -0.5),
        (0.0, 0.0),
        (0.0, 0.5),
        (0.0, 1.0),
        (0.5, -1.0),
        (0.5, -0.5),
        (0.5, 0.0),
        (0.5, 0.5),
        (0.5, 1.0),
        (1.0, -1.0),
        (1.0, -0.5),
        (1.0, 0.0),
        (1.0, 0.5),
        (1.0, 1.0),
    )

    vertices_revalence: tuple[tuple[Vertex, ...]] = (
        (
            (-0.5, 0.0),
            (0.0, -0.5),
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
        (-0.5, -0.5),
        (-0.75, 0.25),
        (-0.75, 0.75),
        (-0.1665, -0.1665),
        (-0.25, 0.25),
        (-0.25, 0.75),
        (0.25, -0.75),
        (0.25, -0.25),
        (0.25, 0.25),
        (0.25, 0.75),
        (0.75, -0.75),
        (0.75, -0.25),
        (0.75, 0.25),
        (0.75, 0.75),
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
        (-0.5, -1.0),
        (0.25, -1.0),
        (0.75, -1.0),
        (1.0, -0.75),
        (1.0, -0.25),
        (1.0, 0.25),
        (1.0, 0.75),
        (0.75, 1.0),
        (0.25, 1.0),
        (-0.25, 1.0),
        (-0.75, 1.0),
        (-1.0, 0.75),
        (-1.0, 0.25),
        (-1.0, -0.5),
    )


class Template_1011(NamedTuple):
    """This is a non-unique template, visualized as the unique 0111 template,
    rotated -90 degrees (90 degrees clockwise rotation).
    """

    name: str = "1011"

    _base = Template_0111()
    _angles = tuple(-90.0 for _ in range(len(_base.vertices_revalence)))

    vertices: tuple[Vertex, ...] = rotate(ref=_base.vertices, angle=-90.0)

    vertices_revalence = tuple(map(rotate, _base.vertices_revalence, _angles))

    faces: tuple[Face, ...] = _base.faces

    vertices_dual: tuple[Vertex, ...] = rotate(ref=_base.vertices_dual, angle=-90.0)

    faces_dual: tuple[Face, ...] = _base.faces_dual

    ports: tuple[Vertex, ...] = rotate(ref=_base.ports, angle=-90.0)


class Template_1101(NamedTuple):
    """This is a non-unique template, visualized as the unique 0111 template,
    rotated 90 degrees (90 degrees counter clockwise rotation).
    """

    name: str = "1101"

    _base = Template_0111()
    _angles = tuple(90.0 for _ in range(len(_base.vertices_revalence)))

    vertices: tuple[Vertex, ...] = rotate(ref=_base.vertices, angle=90.0)

    vertices_revalence = tuple(map(rotate, _base.vertices_revalence, _angles))

    faces: tuple[Face, ...] = _base.faces

    vertices_dual: tuple[Vertex, ...] = rotate(ref=_base.vertices_dual, angle=90.0)

    faces_dual: tuple[Face, ...] = _base.faces_dual

    ports: tuple[Vertex, ...] = rotate(ref=_base.ports, angle=90.0)


class Template_1110(NamedTuple):
    """This is a non-unique template, visualized as the unique 0111 template,
    rotated 180 degrees (180 degrees counter clockwise rotation).
    """

    name: str = "1110"

    _base = Template_0111()
    _angles = tuple(180.0 for _ in range(len(_base.vertices_revalence)))

    vertices: tuple[Vertex, ...] = rotate(ref=_base.vertices, angle=180.0)

    vertices_revalence = tuple(map(rotate, _base.vertices_revalence, _angles))

    faces: tuple[Face, ...] = _base.faces

    vertices_dual: tuple[Vertex, ...] = rotate(ref=_base.vertices_dual, angle=180.0)

    faces_dual: tuple[Face, ...] = _base.faces_dual

    ports: tuple[Vertex, ...] = rotate(ref=_base.ports, angle=180.0)


class Template_1111(NamedTuple):
    """Creates the fully level 2 (L2) data structure.

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
        (-1.0, -1.0),
        (-1.0, -0.5),
        (-1.0, 0.0),
        (-1.0, 0.5),
        (-1.0, 1.0),
        (-0.5, -1.0),
        (-0.5, -0.5),
        (-0.5, 0.0),
        (-0.5, 0.5),
        (-0.5, 1.0),
        (0.0, -1.0),
        (0.0, -0.5),
        (0.0, 0.0),
        (0.0, 0.5),
        (0.0, 1.0),
        (0.5, -1.0),
        (0.5, -0.5),
        (0.5, 0.0),
        (0.5, 0.5),
        (0.5, 1.0),
        (1.0, -1.0),
        (1.0, -0.5),
        (1.0, 0.0),
        (1.0, 0.5),
        (1.0, 1.0),
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
        (-0.75, -0.75),
        (-0.75, -0.25),
        (-0.75, 0.25),
        (-0.75, 0.75),
        (-0.25, -0.75),
        (-0.25, -0.25),
        (-0.25, 0.25),
        (-0.25, 0.75),
        (0.25, -0.75),
        (0.25, -0.25),
        (0.25, 0.25),
        (0.25, 0.75),
        (0.75, -0.75),
        (0.75, -0.25),
        (0.75, 0.25),
        (0.75, 0.75),
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
        (-0.75, -1.0),
        (-0.25, -1.0),
        (0.25, -1.0),
        (0.75, -1.0),
        (1.0, -0.75),
        (1.0, -0.25),
        (1.0, 0.25),
        (1.0, 0.75),
        (0.75, 1.0),
        (0.25, 1.0),
        (-0.25, 1.0),
        (-0.75, 1.0),
        (-1.0, 0.75),
        (-1.0, 0.25),
        (-1.0, -0.25),
        (-1.0, -0.75),
    )
