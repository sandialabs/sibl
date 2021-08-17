from typing import NamedTuple
from functools import reduce
import math
from itertools import permutations

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


class Mesh(NamedTuple):
    """Creates a mesh, which consists of a tuple of Coordinates and Connectivity."""

    coordinates: tuple[Coordinate, ...]
    connectivity: tuple[tuple[int, int, int, int], ...]


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
    """Helper function of template_key to map from number of sub-quads composing a
    corner quadrant to level of additional refinement above zero of a sub-quad.

    Arguments:
        n_quads (int):  The number of sub-quads composing a particular corner quadrant.
            Must be in [0, 4, 16, 64, ... ).
    """
    assert n_quads >= 0
    # n = log_2 [sqrt(n_quads)]
    number = math.sqrt(n_quads)
    base = 2
    exponent = int(math.log(number, base))
    return exponent


def known_quad_corners(*, quad_corners: tuple[int, ...]) -> bool:
    flat_L1 = ((1, 1, 1, 1),)
    convex = tuple(set(permutations([1, 1, 1, 4])))  # assert len == 4
    wave_and_diagonal = tuple(set(permutations([1, 1, 4, 4])))  # assert len == 6
    concave = tuple(set(permutations([1, 4, 4, 4])))  # assert len == 4
    flat_L2 = ((4, 4, 4, 4),)
    weak = ((1, 4, 4, 16), (4, 1, 16, 4), (4, 16, 1, 4), (16, 4, 4, 1))

    _known_quad_corners = (
        flat_L1 + convex + wave_and_diagonal + concave + flat_L2 + weak
    )

    if quad_corners in _known_quad_corners:
        return True
    else:
        return False


def template_key(*, quad_corners: tuple[int, ...]) -> str:
    """Provides a string template key, e.g., "key_0001" that can be used with the
    TemplateFactory to return a Template.

    Arguments:
        quad_corners (tuple[int, ...]): The number of sub-quads in each of the four
            quadrant corners (sw, nw, se, ne).

    Example:
        template_key(quad_corners=(1, 1, 1, 4)) returns "key_0001"
    """
    if known_quad_corners(quad_corners=quad_corners):
        _rooted_quad_corners = tuple(map(number_bisections, quad_corners))
        # _quad_key = "Q" + str(reduce(lambda x, y: str(x) + str(y), quad_corners))
        # _quad_key = "Q" + str(reduce(lambda x, y: str(x) + str(y), _rooted_quad_corners))
        _template_key = "key_" + str(
            reduce(lambda x, y: str(x) + str(y), _rooted_quad_corners)
        )
    else:
        _template_key = "key_unknown"

    return _template_key


def scale_then_translate(
    ref: tuple[tuple[float, float], ...], scale: float, translate: Coordinate
) -> tuple[tuple[float, float], ...]:
    """Scales about the origin and then translates a tuple of points
    in the reference position to a new position.

    Attributes:
        ref (tuple[Vertex, ...]): The tuple of (x, y) coordinates in the reference
            configurations, e.g., ((x0, y0), (x1, y1), ... (xn, yn)).
        scale (float): The magnitude of scale up (scale > 1) or scale down (scale < 1).
            Note that scale > 0.

    Returns:
        new (tuple[Vertex, ...]):  The new positions of the ref coordinates, now
            scaled about the origin and translated to the new coordinates.

    Raises:
        ValueError if scale is not positive.
    """
    if scale <= 0.0:
        raise ValueError("Error: scale must be positive.")

    # Chad, upzip these, way more Pythonic!  -Chad
    # xs = tuple(ref[k][0] for k in range(len(ref)))
    # ys = tuple(ref[k][1] for k in range(len(ref)))
    xs, ys = zip(*ref)

    # Chad, map these, way more Pythonic!  -Chad
    # xnew = tuple(xs[k] * scale + translate.x for k in range(len(xs)))
    # ynew = tuple(ys[k] * scale + translate.y for k in range(len(ys)))
    xnew = tuple(map(lambda x: x * scale + translate.x, xs))
    ynew = tuple(map(lambda y: y * scale + translate.y, ys))

    # Chad, zip these, way more Pythonic!  -Chad
    # new = tuple((xnew[k], ynew[k]) for k in range(len(ref)))
    new = tuple(zip(xnew, ynew))
    return new


class TemplateFactory(NamedTuple):
    """Maps keys, which are converstion of tuple(int, int, int, int) to string, to a
    specific template.

    See https://github.com/sandialabs/sibl/blob/master/geo/doc/dual_quad_transitions.md
        for visual representations of these Template types.
    """

    key_0000: NamedTuple = dual_quad.Template_0000()

    key_0001: NamedTuple = dual_quad.Template_0001()
    key_0010: NamedTuple = dual_quad.Template_0010()
    key_0100: NamedTuple = dual_quad.Template_0100()
    key_1000: NamedTuple = dual_quad.Template_1000()

    key_0011: NamedTuple = dual_quad.Template_0011()
    key_0101: NamedTuple = dual_quad.Template_0101()
    key_1010: NamedTuple = dual_quad.Template_1010()
    key_1100: NamedTuple = dual_quad.Template_1100()

    key_0110: NamedTuple = dual_quad.Template_0110()
    key_1001: NamedTuple = dual_quad.Template_1001()

    key_0111: NamedTuple = dual_quad.Template_0111()
    key_1011: NamedTuple = dual_quad.Template_1011()
    key_1101: NamedTuple = dual_quad.Template_1101()
    key_1110: NamedTuple = dual_quad.Template_1110()

    key_1111: NamedTuple = dual_quad.Template_1111()

    key_0112: NamedTuple = dual_quad.Template_0112()
    key_1021: NamedTuple = dual_quad.Template_1021()
    key_1201: NamedTuple = dual_quad.Template_1201()
    key_2110: NamedTuple = dual_quad.Template_2110()


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
                level_max >= level.  Must be >= 1.
            points (tuple[Coordinate,...]): Coordinates (x, y) that trigger local
                refinement.

        Raises:
            ValueError if level_max is < 1.
        """

        self.cell = cell

        if level_max < 1:
            raise ValueError("level_max must be one or greater")

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

    # def quads_dual(self) -> tuple[Quad, ...]:
    # def quads_dual(self):
    def mesh_dual(self):
        """Maps the quadtree to an assembly of dualized quadrilateral elements mesh.
        Returns the (vertices, faces) for all templates embedded in the quadtree.
        """
        _quad_levels_recursive = self.quad_levels_recursive()
        _mesh_dual = QuadTree._mesh_dual(
            cell=self.cell, level=0, quad_levels_recursive_subset=_quad_levels_recursive
        )
        return _mesh_dual
        # quads_recursive = ((1,), (1,), (1,), ((2,), (2,), (2,), ((3,), (3,), (3,), (3,))))

        # _cell = self.cell

        # _quads_recursive = self.quad_levels_recursive()
        # _quad_corners = tuple(len(corner) for corner in _quads_recursive)
        # # for example, _quad_corners == (1, 1, 1, 4)

        # _template_key = template_key(quad_corners=_quad_corners)
        # # for example, _template_key == "key_0001"
        # _factory = TemplateFactory()

        # _template = getattr(_factory, _template_key)
        # # for example, _template.name == "0001"

        # _scaled_translated_vertices_dual = scale_then_translate(
        #     ref=_template.vertices_dual, scale=_cell.size, translate=_cell.center
        # )

        # # return (_template.vertices_dual, _template.faces_dual)
        # return (_scaled_translated_vertices_dual, _template.faces_dual)

    def duals(self):
        """Returns the dual template(s) embedded in the QuadTree.
        See
        https://github.com/sandialabs/sibl/blob/master/geo/doc/dual_quad_transitions.md
        for the has illustrations.

        Returns:
            A tuple of the dual template(s) embedded by the QuadTree.
        """
        if self.level_max < 1:
            raise ValueError(
                "level_max must be one or greater for dual template to exist."
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
    def _mesh_dual(*, cell: Cell, level: int, quad_levels_recursive_subset: tuple):
        """Returns the dual mesh encoded by the QuadTree."""

        _factory = TemplateFactory()

        if cell.has_children:
            subset_sw = quad_levels_recursive_subset[0]
            subset_nw = quad_levels_recursive_subset[1]
            subset_se = quad_levels_recursive_subset[2]
            subset_ne = quad_levels_recursive_subset[3]

            n_nested_sw = len(tuple(QuadTree._tuple_flatten(subset_sw)))
            n_nested_nw = len(tuple(QuadTree._tuple_flatten(subset_nw)))
            n_nested_se = len(tuple(QuadTree._tuple_flatten(subset_se)))
            n_nested_ne = len(tuple(QuadTree._tuple_flatten(subset_ne)))

            _template_key = template_key(
                quad_corners=tuple([n_nested_sw, n_nested_nw, n_nested_se, n_nested_ne])
            )

            if _template_key == "key_unknown":

                # A known template cannot be fit to the combination of quad_corners,
                # so recursively march down until a key is found.

                return (
                    QuadTree._mesh_dual(
                        cell=cell.sw,
                        level=level + 1,
                        quad_levels_recursive_subset=subset_sw,
                    ),
                    QuadTree._mesh_dual(
                        cell=cell.nw,
                        level=level + 1,
                        quad_levels_recursive_subset=subset_nw,
                    ),
                    QuadTree._mesh_dual(
                        cell=cell.se,
                        level=level + 1,
                        quad_levels_recursive_subset=subset_se,
                    ),
                    QuadTree._mesh_dual(
                        cell=cell.ne,
                        level=level + 1,
                        quad_levels_recursive_subset=subset_ne,
                    ),
                )

            else:
                # A known template can be constructed.

                _template = getattr(_factory, _template_key, None)
                # for example, _template.name == "0001"
                assert _template

                _scaled_translated_vertices_dual = scale_then_translate(
                    ref=_template.vertices_dual, scale=cell.size, translate=cell.center
                )

                _new_coordinates = coordinates(pairs=_scaled_translated_vertices_dual)

                # return (_template.vertices_dual, _template.faces_dual)
                # return (_scaled_translated_vertices_dual, _template.faces_dual)
                mesh = Mesh(
                    coordinates=_new_coordinates, connectivity=_template.vertices_dual
                )
                return (mesh,)
                # return 42

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
