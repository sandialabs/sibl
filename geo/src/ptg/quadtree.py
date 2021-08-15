from typing import NamedTuple
from functools import reduce
import math

import ptg.dual_quad as dual_quad


class Coordinate(NamedTuple):
    """Creates a coordinate as a (x, y) pair of floats."""

    x: float  # x-coordinate
    y: float  # y-coordinate


Vertex = Coordinate  # a vertex belongs to a quad
# A vertex and a coordinate have the same data type, but different
# semantic.  A quad is composed of four vertices.  A quad is not
# composed of four coordinates.


class Quad(NamedTuple):
    """Creates a Quad with vertices in a counter-clockwise manner,
    starting from (0, 0) as the southwest corner.
    """

    sw: Vertex  # southwest corner
    se: Vertex  # southeast corner
    ne: Vertex  # northeast corner
    nw: Vertex  # northwest corner


class DualHash(NamedTuple):
    """Creates dual hash of the parent primal cell's four corners.  Each int
    value is the number of dual ports in each of the four corner quadrants.

    Example:
        0 gives 2^0 = 1 port in each x and y directions within the corner quadrant,
        1 gives 2^1 = 2 ports, and
        2 gives 2^2 = 4 ports.

    Current has table,
    https://github.com/sandialabs/sibl/blob/master/geo/doc/dual_quad_transitions.md
    suports only "0", "1" and "2" as int possibilities.
    """

    sw: int  # southwest corner
    nw: int  # northwest corner
    se: int  # southeast corner
    ne: int  # northeast corner


def number_bisections(n_quads: int) -> int:
    assert n_quads >= 0
    # n = log_2 [sqrt(n_quads)]
    number = math.sqrt(n_quads)
    base = 2
    exponent = int(math.log(number, base))
    return exponent


def quad_key(*, quad_corners: tuple[int, ...]) -> str:
    _rooted_quad_corners = tuple(map(number_bisections, quad_corners))
    # _quad_key = "Q" + str(reduce(lambda x, y: str(x) + str(y), quad_corners))
    _quad_key = "Q" + str(reduce(lambda x, y: str(x) + str(y), _rooted_quad_corners))
    return _quad_key


class QuadsToTemplate(NamedTuple):
    """Maps keys, which are converstion of tuple(int, int, int, int) to string, to a
    specific template.
    """

    Q0000: NamedTuple = dual_quad.Template_0000()

    Q0001: NamedTuple = dual_quad.Template_0001()
    Q0010: NamedTuple = dual_quad.Template_0010()
    Q0100: NamedTuple = dual_quad.Template_0100()
    Q1000: NamedTuple = dual_quad.Template_1000()

    Q0112: NamedTuple = dual_quad.Template_0112()


# Reference: recursive type hinting:
# https://stackoverflow.com/questions/53845024/defining-a-recursive-type-hint-in-python
# Quads = Union[Quad, Iterable["Quads"]]


def coordinates(*, pairs: tuple[tuple[float, float], ...]) -> tuple[Coordinate, ...]:
    """Creates a tuple of Coordinates from a tuple of (x, y) pairs.

    Argments:
        pairs (tuple of tuple of floats), e.g.,
            ((x0, y0), (x1, y1), ... (xn, yn))


    Returns:
        tuple of Coordinates:
            A tuple of Coordinates, which is a NamedTuple
            representation of the pairs.
    """
    xs = tuple(pairs[k][0] for k in range(len(pairs)))
    ys = tuple(pairs[k][1] for k in range(len(pairs)))
    cs = tuple(map(Coordinate, xs, ys))  # coordinates
    return cs


class Cell:
    def __init__(self, *, center: Coordinate, size: float):
        """A square shape centered at (cx, cy) with
            size = width = height.

        Arguments:
            center (Coordinate): The (x, y) float coordinate of the center of the cell.
            size (float): The side length dimension of the square-shaped cell.
                The cell width = cell height = cell size.
        """
        self.center = center
        self.size = size

        self.west = center.x - size / 2.0
        self.east = center.x + size / 2.0

        self.south = center.y - size / 2.0
        self.north = center.y + size / 2.0

        # # children are non-existent on construction
        # self.sw = None
        # self.nw = None
        # self.se = None
        # self.ne = None
        # self._sw = None
        # self._nw = None
        # self._se = None
        # self._ne = None
        self.has_children = False

        # A cell has a Quad scheme collection of Vertices.
        self.vertices = Quad(
            sw=Vertex(self.west, self.south),
            se=Vertex(self.east, self.south),
            ne=Vertex(self.east, self.north),
            nw=Vertex(self.west, self.north),
        )

    def contains(self, point: Coordinate) -> bool:
        """Determines if the coordinates of a point lie within the boundary of a cell.

        Arguments:
            point (Coordinate): The (x, y) float coordinate of a points for testing
                inside the Cell or not.  A point on the Cell boundary is considered
                as inside and thus contained by the Cell.

        Returns:
            bool:
                True if the point is on the interior or boundary of the cell.
                False if the point is on the exterior of the cell.
        """
        return (
            point.x >= self.west
            and point.x <= self.east
            and point.y >= self.south
            and point.y <= self.north
        )

    # getter property
    # @property
    # def sw(self):
    #     # raise error if self._sw is None, indicate Cell.divide has not yet been called
    #     if self._sw is None:
    #         raise

    # Do not implement the setter, on purpose, to prohibit client from setting
    # self.sw, self.nw, self.se, and self.ne except by calling self.divide() method.
    # setter property
    # @sw.setter
    # def sw(self, val):
    #     pass

    def divide(self):
        """Divides the Cell into four children Cells:
            Southwest (sw)
            Northwest (nw)
            Southeast (se)
            Northeast (ne)
        The side length of a child cell is half of the side length of the parent cell.
        """
        center_west_x = (self.center.x + self.west) / 2.0
        center_east_x = (self.center.x + self.east) / 2.0

        center_south_y = (self.center.y + self.south) / 2.0
        center_north_y = (self.center.y + self.north) / 2.0

        divided_size = self.size / 2.0

        self.sw = Cell(
            center=Coordinate(x=center_west_x, y=center_south_y), size=divided_size
        )
        self.nw = Cell(
            center=Coordinate(x=center_west_x, y=center_north_y), size=divided_size
        )
        self.se = Cell(
            center=Coordinate(x=center_east_x, y=center_south_y), size=divided_size
        )
        self.ne = Cell(
            center=Coordinate(x=center_east_x, y=center_north_y), size=divided_size
        )

        self.has_children = True  # overwrite from False in __init__

        print("Finished cell division.")


class QuadTree:
    def __init__(
        self, *, cell: Cell, level: int, level_max: int, points: tuple[Coordinate, ...]
    ):
        """A QuadTree is a specific instance of a cell with zero ore more recursive cell
        subdivisions.  Points passed into the QuadTree trigger cell division.  If points
        lie within a cell, then a cell will divide, otherwise a cell will not divide.
        Cell division occurs level_max number of times.

        Arguments:
            cell (Cell): The root cell to be recursively bisected.  Must be square.
            level (int): The starting level of the root cell, typically zero (0).
            level_max (int): The maximum level of bisection.
                level_max >= level
            points (tuple[Coordinate,...]): Coordinates (x, y) that trigger local
                refinement.
        """

        self.cell = cell

        if level_max < 0:
            raise ValueError("level_max must be zero or greater.")

        self.level_max = level_max

        if level + 1 > level_max:
            return  # no further refinement occurs

        assert level <= level_max

        self.level = level

        # Avoid blind acceptance of all client points.  Thus, avoid this original
        # implementation the first list of points supplied from a client may contain
        # points outside of the cell.
        # self.points = points  # <-- avoid this original implementation
        #
        # Instead, filter to make sure points lie only within the cell boundary.
        self.points = tuple(filter(self.cell.contains, points))

        # If there is one or more point(s) inside of this parent cell, then subdivide.
        if len(self.points) > 0:
            self.cell.divide()
            self.level += 1

            if self.cell.has_children:
                self.sw = QuadTree(
                    cell=self.cell.sw,
                    level=self.level,
                    level_max=self.level_max,
                    points=self.points,
                )
                self.nw = QuadTree(
                    cell=self.cell.nw,
                    level=self.level,
                    level_max=self.level_max,
                    points=self.points,
                )
                self.se = QuadTree(
                    cell=self.cell.se,
                    level=self.level,
                    level_max=self.level_max,
                    points=self.points,
                )
                self.ne = QuadTree(
                    cell=self.cell.ne,
                    level=self.level,
                    level_max=self.level_max,
                    points=self.points,
                )

    def quads(self) -> tuple[Quad, ...]:
        """Maps the quadtree to an assembly of quadrilateral elements.
        Each quad has vertices composed of (x, y) coordinates.
        Each quad has vertices ordered counter-clockwise, as sw, se, ne, nw.

        Returns:
            For (n+1) quads, the return will be
            (
                ((x0, y0), (x1, y1), (x2, y2), (x3, y3)),  # <-- quad 0
                ((x0, y0), (x1, y1), (x2, y2), (x3, y3)),  # <-- quad 1
                ...
                ((x0, y0), (x1, y1), (x2, y2), (x3, y3)),  # <-- quad n
            )
        """

        # _vertices will have nested tuples
        _vertices = QuadTree._child_vertices(self.cell)

        # quads will have the same tuples, just flattened
        _quads = tuple(QuadTree._quads_flatten(_vertices))

        return _quads

    def duals(self):
        """Returns the dual hashes embedded in the QuadTree.
        See
        https://github.com/sandialabs/sibl/blob/master/geo/doc/dual_quad_transitions.md
        for the has illustrations.

        Returns:
            A tuple of the dual hashes embedded by the QuadTree.
        """
        if self.level_max < 1:
            raise ValueError(
                "level_max must be one or greater for dual hashes to exist."
            )

        if self.level_max == 1:
            return (DualHash(sw=0, nw=0, se=0, ne=0),)

        _quad_levels = QuadTree._quad_levels(cell=self.cell, level=0)
        return _quad_levels

    def quad_levels_recursive(self) -> tuple[tuple[int, ...], ...]:
        qls = QuadTree._quad_levels(cell=self.cell, level=0)
        return qls

    def quad_levels(self) -> tuple[int, ...]:
        # qls = QuadTree._quad_levels(cell=self.cell, level=0)
        qls = self.quad_levels_recursive()
        return tuple(QuadTree._tuple_flatten(qls))

    # figure out type hinting soon
    # def _child_vertices(cell: Cell) -> tuple[tuple[float, float], ...]:
    # def _child_vertices(cell: Cell) -> Quads:   # <-- this works in part
    @staticmethod
    def _child_vertices(cell: Cell):
        """Given a cell, returns the cell's vertices, and (recursively) the vertices of
        the cell's children, grandchildren, et cetera.  Recursion ends when a cell level
        has no children.
        """
        if cell.has_children:
            return (
                QuadTree._child_vertices(cell.sw),
                QuadTree._child_vertices(cell.nw),
                QuadTree._child_vertices(cell.se),
                QuadTree._child_vertices(cell.ne),
            )
        else:
            return (cell.vertices,)
            # return cell.vertices

    # ) -> Union[
    #     tuple[
    #         tuple[int],
    #         Union[
    #             tuple[tuple[int], ...],
    #             tuple[int],
    #             Union[
    #                 tuple[tuple[int], ...],
    #                 tuple[int],
    #                 Union[
    #                     tuple[tuple[int], ...],
    #                     tuple[int],
    #                     tuple[tuple[int], ...],
    #                 ],
    #             ],
    #         ],
    #     ]
    # ]:
    #
    # OR
    #
    #         tuple[int],
    #         Union[
    #             tuple[tuple[int], ...],
    #             tuple[int],
    #             Union[
    #                 tuple[tuple[int], ...],
    #                 tuple[int],
    #                 Union[
    #                     tuple[tuple[int], ...],
    #                     tuple[int],
    #                 ],
    #             ],
    #         ],
    #         tuple[tuple[int], ...],
    #     ]
    # ]:

    @staticmethod
    def _quad_levels(*, cell: Cell, level: int):
        """Given a cell, returns the cell's quad levels, and (recursively) the quad levels of
        the cell's children, grandchildren, et cetera.  Recursion ends when a cell level
        has no children.
        """
        if cell.has_children:
            return (
                QuadTree._quad_levels(cell=cell.sw, level=level + 1),
                QuadTree._quad_levels(cell=cell.nw, level=level + 1),
                QuadTree._quad_levels(cell=cell.se, level=level + 1),
                QuadTree._quad_levels(cell=cell.ne, level=level + 1),
            )
        else:
            # return (cell.vertices,)
            # return cell.level
            return (level,)

    @staticmethod
    def _tuple_flatten(nested: tuple):
        """Given a tuple of items, yields a tuple item in a flattened sequence."""
        for i in nested:
            yield from [i] if not isinstance(i, tuple) else QuadTree._tuple_flatten(i)

    @staticmethod
    def _quads_flatten(nested: tuple):
        """Given a tuple of nested quads, yields a quad in a flattened sequence."""
        for i in nested:
            yield from [i] if isinstance(i, Quad) else QuadTree._quads_flatten(i)
