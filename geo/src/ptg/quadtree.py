from typing import NamedTuple


# Coordinate = tuple[float, float]  # 2D coordinate


class Coordinate(NamedTuple):
    x: float  # x-coordinate
    y: float  # y-coordinate


# class Children(NamedTuple):
#     sw: Cell  # southwest
#     nw: Cell  # northwest


Population = tuple[Coordinate, ...]


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

        self._children = []  # empty list at init
        # self._children = None

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

        sw = Cell(
            center=Coordinate(x=center_west_x, y=center_south_y), size=divided_size
        )
        nw = Cell(
            center=Coordinate(x=center_west_x, y=center_north_y), size=divided_size
        )
        se = Cell(
            center=Coordinate(x=center_east_x, y=center_south_y), size=divided_size
        )
        ne = Cell(
            center=Coordinate(x=center_east_x, y=center_north_y), size=divided_size
        )

        # self._children = Children(parent=self, sw=sw, nw=nw, se=se, ne=ne)
        self._children.append(Children(parent=self, sw=sw, nw=nw, se=se, ne=ne))

        print("Finished cell division.")

    @property
    def children(self):  # as AP how to type hint here
        # if self._children is None:
        #     return None
        # else:
        #     return self._children
        return self._children


class Children:
    def __init__(self, *, parent: Cell, sw: Cell, nw: Cell, se: Cell, ne: Cell):
        self.parent = parent
        self.southwest = sw
        self.northwest = nw
        self.southeast = se
        self.northeast = ne

    @property
    def southwest(self):
        return self._sw

    @southwest.setter
    def southwest(self, newsw: Cell):
        self._sw = newsw

    @property
    def northwest(self):
        return self._nw

    @northwest.setter
    def northwest(self, newnw: Cell):
        self._nw = newnw

    @property
    def southeast(self):
        return self._se

    @southeast.setter
    def southeast(self, newse: Cell):
        self._se = newse

    @property
    def northeast(self):
        return self._ne

    @northeast.setter
    def northeast(self, newne: Cell):
        self._ne = newne


# class QuadTree:
#     def __init__(self):
#         a = 4
