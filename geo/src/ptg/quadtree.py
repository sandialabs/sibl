from typing import NamedTuple


class Coordinate(NamedTuple):
    x: float  # x-coordinate
    y: float  # y-coordinate


def coordinates(*, pairs: tuple[tuple[float, float], ...]) -> tuple[Coordinate, ...]:
    xs = tuple(pairs[k][0] for k in range(len(pairs)))
    ys = tuple(pairs[k][1] for k in range(len(pairs)))
    cs = tuple(map(Coordinate, xs, ys))  # coordinates
    return cs


class Cell:
    def __init__(self, *, center: Coordinate, size: float):
        """
        A square shape centered at (cx, cy) with size = width = height.

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

        # vertices start in sw corner, and proceed counter-clockwise
        self.vertices = (
            (self.west, self.south),
            (self.east, self.south),
            (self.east, self.north),
            (self.west, self.north),
        )

    def contains(self, point: Coordinate) -> bool:
        """
        Determines if the coordinates of a point lie within the boundary of a cell.

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
                    level_max=level_max,
                    points=self.points,
                )
                self.nw = QuadTree(
                    cell=self.cell.nw,
                    level=self.level,
                    level_max=level_max,
                    points=self.points,
                )
                self.se = QuadTree(
                    cell=self.cell.se,
                    level=self.level,
                    level_max=level_max,
                    points=self.points,
                )
                self.ne = QuadTree(
                    cell=self.cell.ne,
                    level=self.level,
                    level_max=level_max,
                    points=self.points,
                )

    def quads(self) -> tuple[list[float], ...]:
        """Maps the quadtree to an assembly of quadrilateral elements.
        Each quad has vertices composed of (x, y) coordinates.
        Each quad has vertices ordered counter-clockwise, as sw, se, ne, nw.

        Returns:
            For (n+1) quads, the return will be
            (
                ([x0, y0], [x1, y1], [x2, y2], [x3, y3]),  # <-- quad 0
                ([x0, y0], [x1, y1], [x2, y2], [x3, y3]),  # <-- quad 1
                ...
                ([x0, y0], [x1, y1], [x2, y2], [x3, y3]),  # <-- quad n
            )
        """
        _vertices = QuadTree._child_vertices(self.cell)

        bb = tuple(QuadTree._tuple_flatten(_vertices))

        # A quad with four vertices in 2D has eight (8) total coordinates:
        # nnc = length of ((x0, y0), (x1, y1), (x2, y2), (x3, y3))
        nnc = 8  # number of nodal (x or y) coordinates (per element) nnc
        nel = int(len(bb) / nnc)  # number of elements

        cc = tuple(bb[k * nnc : nnc + k * nnc] for k in range(nel))

        xs = tuple(tuple(cc[k][i] for i in (0, 2, 4, 6)) for k in range(nel))
        ys = tuple(tuple(cc[k][j] for j in (1, 3, 5, 7)) for k in range(nel))

        qs = tuple(
            tuple([xs[k][n], ys[k][n]] for n in (0, 1, 2, 3)) for k in range(nel)
        )

        # return the list of quads qs
        return qs

    def quad_levels(self) -> tuple[int, ...]:
        qls = QuadTree._quad_levels(cell=self.cell, level=0)
        return tuple(QuadTree._tuple_flatten(qls))

    # figure out type hinting soon
    # def _child_vertices(cell: Cell) -> tuple[tuple[float, float], ...]:
    @staticmethod
    def _child_vertices(cell: Cell):
        """Given a cell, returns the cell's vertices, and (recursively) the vertices of
        the cell's children, grandchildren, et cetera.  Recursion ends when a cell level
        has no children."""
        if cell.has_children:
            return (
                QuadTree._child_vertices(cell.sw),
                QuadTree._child_vertices(cell.nw),
                QuadTree._child_vertices(cell.se),
                QuadTree._child_vertices(cell.ne),
            )
        else:
            # return (cell.vertices,)
            return cell.vertices

    @staticmethod
    def _quad_levels(*, cell: Cell, level: int):
        """Given a cell, returns the cell's quad levels, and (recursively) the quad levels of
        the cell's children, grandchildren, et cetera.  Recursion ends when a cell level
        has no children."""
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
        """Given a nested tuple, which is generated from the QuadTree class recursive
        __init__ function calls, yields a flattened tuple."""
        for i in nested:
            yield from [i] if not isinstance(i, tuple) else QuadTree._tuple_flatten(i)
