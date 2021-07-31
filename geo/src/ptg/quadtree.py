from typing import NamedTuple


class Coordinate(NamedTuple):
    x: float  # x-coordinate
    y: float  # y-coordinate


class Cell:
    """A square shape centered at (cx, cy) with size = width = height."""

    def __init__(self, *, center: Coordinate, size: float):
        """
        Arguments:
            center (Coordinate): The (x, y) float coordinate of the center of the cell.
            size (float): The side length dimension of the cell.
                The cell width = cell height = cell size.
        """
        self.center = center
        self.size = size

        self.west = center.x - size / 2.0
        self.east = center.x + size / 2.0

        self.south = center.y - size / 2.0
        self.north = center.y + size / 2.0

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
        Arguments:
            point (Coordinate): The (x, y) float coordinate of a points for testing
                inside the Cell or not.  A point on the Cell boundary is considered
                as inside and thus contained by the Cell.

        Returns:
            bool:
                True is the point is on the interior or boundary of the cell.
                False if the point is on the exterior of the cell.
        """
        return (
            point.x >= self.west
            and point.x <= self.east
            and point.y >= self.south
            and point.y <= self.north
        )

    def divide(self):
        """Divides the Cell into four children Cells."""
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
        """A QuadTree is a specific instance of a cell with cell subdivisions.
        If points lie within a cell, then a cell will divide, otherwise a cell
        will not divide.
        Cell division occurs level_max number of times.
        """

        self.cell = cell

        if level_max < 0:
            raise ValueError("level_max must be zero or greater.")

        if level > level_max:
            return  # no further refinement occurs

        assert level <= level_max

        self.level = level

        # Avoid blind acceptance of all client points.  Instead, filter to
        # make sure points lie only within the cell boundary.
        # self.points = points  # avoid since may contain points outside of the cell
        self.points = tuple(filter(self.cell.contains, points))

        # If there is one or more point(s) inside of this cell, then subdivide.
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

    def quads(self):
        """Returns a tuple of levels.
        Each level consists of cells, ordered sw, nw, se, ne.
        Each cell has vertices, ordered counter-clockwise as sw, se, ne, nw.
        """
        # _vertices = [(self.cell.vertices,)]  # Level 0 vertices, must exist

        _vertices = QuadTree.child_vertices(self.cell)

        # while self.cell.has_children:
        #     aa = QuadTree.child_vertices(self.cell)
        #     _vertices.append(aa)
        #     # L0.append(QuadTree.child_vertices(self.cell))

        # L1 = self.quads_on_level(self.cell)

        # if self.cell.has_children:
        #     L1 = (
        #         self.cell.sw.vertices,
        #         self.cell.se.vertices,
        #         self.cell.ne.vertices,
        #         self.cell.nw.vertices,
        #     )

        bb = tuple(QuadTree.tuple_flatten(_vertices))
        nnc = 8  # number of nodal x or y coordinates per element
        nel = int(len(bb) / nnc)  # number of elements
        cc = tuple(bb[k * nnc : nnc + k * nnc] for k in range(nel))
        xs = tuple(tuple(cc[k][i] for i in (0, 2, 4, 6)) for k in range(nel))
        ys = tuple(tuple(cc[k][j] for j in (1, 3, 5, 7)) for k in range(nel))

        qs = tuple(
            tuple([xs[k][n], ys[k][n]] for n in (0, 1, 2, 3)) for k in range(nel)
        )

        # dd = tuple(
        #     (cc[k][i], cc[k][j])
        #     for i in (0, 2, 4, 6)
        #     for j in (1, 3, 5, 7)
        #     for k in range(nel)
        # )
        # return _vertices
        return qs

    @staticmethod
    def child_vertices(cell: Cell):
        if cell.has_children:
            return (
                QuadTree.child_vertices(cell.sw),
                QuadTree.child_vertices(cell.nw),
                QuadTree.child_vertices(cell.se),
                QuadTree.child_vertices(cell.ne),
            )
        else:
            # return (cell.vertices,)
            return cell.vertices

    @staticmethod
    def tuple_flatten(nested: tuple):
        for i in nested:
            yield from [i] if not isinstance(i, tuple) else QuadTree.tuple_flatten(i)
