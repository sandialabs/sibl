# Copyright 2020 National Technology and Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
# certain rights in this software.


from typing import Final, Iterable, NamedTuple, Union
from functools import reduce
import math
from itertools import permutations, repeat
from statistics import mean

import ptg.dual_quad as dual_quad
from ptg.point import Point2D, Points

# import ptg.polygon as poly


# class Coordinate(NamedTuple):
#     """Creates a coordinate as a (x, y) pair of floats."""
#
#     x: float  # x-coordinate
#     y: float  # y-coordinate


# def coordinates(*, pairs: tuple[tuple[float, float], ...]) -> tuple[Coordinate, ...]:
#     """Creates a tuple of Coordinates from a tuple of (x, y) pairs.
#
#     Argments:
#         pairs (tuple of tuple of floats), e.g.,
#             ((x0, y0), (x1, y1), ... (xn, yn))
#
#
#     Returns:
#         tuple of Coordinates:
#             A tuple of Coordinates, which is a NamedTuple
#             representation of the pairs.
#     """
#
#     # xs = tuple(pairs[k][0] for k in range(len(pairs)))
#     # ys = tuple(pairs[k][1] for k in range(len(pairs)))
#     xs, ys = zip(*pairs)
#     # cs = tuple(Coordinate(x=pairs[i][0], y=pairs[i][1]) for i in range(len(pairs)))
#     cs = tuple(map(Coordinate, xs, ys))  # coordinates
#     return cs


# Vertex = Coordinate  # a vertex belongs to a quad
# # A vertex and a coordinate have the same data type, but different
# # semantic.  A quad is composed of four vertices.  A quad is not
# # composed of four coordinates.


class Quad(NamedTuple):
    """Creates a Quad with vertices in a counter-clockwise manner,
    starting from (0, 0) as the southwest corner.
    """

    sw: Point2D  # southwest corner
    se: Point2D  # southeast corner
    ne: Point2D  # northeast corner
    nw: Point2D  # northwest corner


class Mesh(NamedTuple):
    """Creates a mesh, which consists of a tuple of coordinates and
    a tuple of connectivity.

    Notation connection with Finite Element Method (FEM), cf., TJR Hughes
        nnp = number of nodal points = len(coordinates)
        nel = number of elements = len(connectivity)
    """

    # coordinates: tuple[Coordinate, ...]
    coordinates: Points
    # connectivity: tuple[tuple[int, int, int, int], ...]
    connectivity: tuple[tuple[int, ...], ...]


def edges(*, mesh: Mesh) -> tuple[tuple[int, int], ...]:
    """Given a Mesh, return a tuple of edges, where each edge consisting of a
    start point node number and stop point node number.

    Arguments:
        mesh (Mesh): The mesh object, composed of coordinates and connectivity.

    Returns:
        tuple[tuple[int, int], ...]: A tuple of edges defined by a start node number
            and stop node number.
            e.g.,
                (
                    (x0_start, y0_start), (x0_stop, y0_stop),
                    (x1_start, y1_start), (x1_stop, y1_stop),
                    ...
                    (xn_start, yn_start), (xn_stop, yn_stop),
                )
    """

    cs = mesh.connectivity

    # extend the connectivity to repeat the first node number after the last
    cs_ext = tuple(c + (c[0],) for c in cs)

    # group the items as pairs ((x0, y0), (x1, y1), ... (xn, yn))
    cs_ext_pairs = tuple((c[i], c[i + 1]) for c in cs_ext for i in range(len(c) - 1))
    edges = tuple(set(tuple(frozenset(i)) for i in set(cs_ext_pairs)))
    return edges


# def centroid(*, coordinates: tuple[Coordinate, ...]) -> Coordinate:
def centroid(*, coordinates: Points) -> Point2D:
    """Given a tuple of Coordinates, returns the centroid of those
    coordinates as a Coordinate.

    Arguments:
        coordinates (tuple[Coordinate, ...]): The tuple of coordinates
            that define the 2D shape, typically a quadrilateral.

    Returns:
        Coordinate: the (x_cg, y_cg) coordinate locating the centroid
            of the 2D shape.

    """
    return Point2D(x=mean(coordinates.xs), y=mean(coordinates.ys))


# def trim(*, mesh: Mesh, boundary: tuple[Coordinate, ...]):
#     """Given a finite element mesh and a boundary, returns the subset mesh
#     connectivity of elements who have a geometric center contained by the
#     boundary.
#
#     The returned mesh connectivity may be the empty set, indicating no element
#     in the mesh is contained in the boundary.
#
#     Arguments:
#         mesh (Mesh): A data structure containing a tuple of coordinates and a tuple
#             of connectivity.
#         boundary (tuple[tuple[float, float], ...]): A tuple of tuple of float pairs,
#             e.g., ((x0, y0), (x1, y1), ... (xn, yn)).
#
#     Returns:
#         Mesh.connectivity:  The subset of mesh elements, possibly the empty set, that
#             is contained in the boundary.
#     """
#     _polygon = poly.Polygon2D(boundary=boundary)
#     _subset = ((),)
#
#     for element in mesh.connectivity:
#         cg = centroid(coordinates=mesh.coordinates[i] for i in element])
#
#
#     return _subset


class Domain(NamedTuple):
    """Creates a Domain, which consists of a Mesh and a boundaries tuple.

    Mesh: see definition above.

    boundaries (tuple[tuple[int, ...], ...]):  Each tuple is a boundary. Each
        boundary is a tuple of integers that identify the node number in the mesh.
        The boundary integers should be sequential along the boundary.  There
        ordering of the boundary from first to last node or last to first node is
        immaterial, since the `domain_merge` function compares both forward and
        backward boundary sequences.
    """

    mesh: Mesh
    boundaries: tuple[tuple[int, ...], ...]


# Reference: recursive type hinting:
# https://stackoverflow.com/questions/53845024/defining-a-recursive-type-hint-in-python
# Garthoks = Union[Garthok, Iterable['Garthoks']]
# and
# Forward references:
# https://www.python.org/dev/peps/pep-0484/#forward-references
Quads = Union[Iterable["Quads"], tuple[Quad, ...]]  # support for recursive type hint
# Quads = Iterable["Quads"] | tuple[Quad, ...]  # support for recursive type hint  # python 3.10
Meshes = Union[Iterable["Meshes"], tuple[Mesh, ...]]
# Meshes = Iterable["Meshes"] | tuple[Mesh, ...]  # python 3.10
# Ints = Union[Iterable["Ints"], tuple[int, ...]]
# NestedInts = Union[Tuple[int], Iterable["NestedInts"]]


class DualHash(NamedTuple):
    """Creates dual hash of the parent primal cell's four corners.  Each int
    value is the number of dual ports in each of the four corner quadrants.

    Example:
        0 gives 2^0 = 1 port in each x and y directions within the corner quadrant,
        1 gives 2^1 = 2 ports, and
        2 gives 2^2 = 4 ports.

    Current has table:
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
    """Given a tuple of quad_corners, determines if they are known or unknown
    templates of:
    https://github.com/sandialabs/sibl/blob/master/config/workflow.md

    Arguments:
        quad_corners (tuple[int, ...]) that describes the number of sub-quads that
            are present in each of the four corners of a parent quad.

    Returns:
        True if the quad_corner is a known template, False otherwise.

    Example:
        known_quad_corner(quad_corner=tuple(1, 1, 1, 4)) returns True because it
            is a known quad_corner and is the template with key_0001.
    """
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


def template_key(*, quad_corners: tuple[int, ...], level: int, partial: bool) -> str:
    """Provides a string template key, e.g., "key_0001" that can be used with the
    TemplateFactory to return a Template.

    Arguments:
        quad_corners (tuple[int, ...]): The number of sub-quads in each of the four
            quadrant corners (sw, nw, se, ne).
        level (int):  The quadtree level >= 0 for a given template being fit.
        partial (bool): Whether or not this is a partially filled template.

    Returns:
        str that has a prefex of "key_" plus a suffix of four integers, e.g, "1114",
            for a completed key of `"key_1114".

    Example:
        template_key(quad_corners=(1, 1, 1, 4)) returns "key_0001"
    """
    if known_quad_corners(quad_corners=quad_corners):
        _rooted_quad_corners = tuple(map(number_bisections, quad_corners))
        _template_key = "key_" + str(
            reduce(lambda x, y: str(x) + str(y), _rooted_quad_corners)
        )
        if _template_key == "key_0001":
            # then further logic to determine refinement and partial status
            # r0 is not refined; r1 is refined
            # p0 is not partial; p1 is partial
            if level == 0 and partial is False:
                _template_key = _template_key + "_r0_p0"

            elif level == 0 and partial is True:
                _template_key = _template_key + "_r0_p1"

            elif level > 0 and partial is False:
                _template_key = _template_key + "_r1_p0"

            elif level > 0 and partial is True:
                _template_key = _template_key + "_r1_p1"

            else:
                raise ValueError("Level of refinement and partial status undefined.")
    else:
        _template_key = "key_unknown"

    return _template_key


# def scale_then_translate(
#     *, ref: tuple[Coordinate, ...], scale: float, translate: Coordinate
# ) -> tuple[Coordinate, ...]:
def scale_then_translate(*, ref: Points, scale: float, translate: Point2D) -> Points:
    """Scales about the origin and then translates a tuple of Coordinates
    in the reference position to a new position.

    Arguments:
        ref (tuple[Coordinate, ...]): The tuple of (x, y) coordinates in the
            reference configurations, e.g., ((x0, y0), (x1, y1), ... (xn, yn)).
        scale (float): The magnitude of scale up (scale > 1) or
            scale down (scale < 1).
            Note that scale > 0.

    Returns:
        new (tuple[Coordinate, ...]):  The new positions of the ref coordinates, now
            scaled about the origin and translated to the new coordinates.

    Raises:
        ValueError if scale is not positive.
    """
    if scale <= 0.0:
        raise ValueError("Error: scale must be positive.")

    # xs, ys = zip(*ref)

    # xnew = tuple(xs[k] * scale + translate.x for k in range(len(xs)))
    # ynew = tuple(ys[k] * scale + translate.y for k in range(len(ys)))
    # xnew = tuple(map(lambda x: x * scale + translate.x, xs))
    # ynew = tuple(map(lambda y: y * scale + translate.y, ys))
    # xnew = tuple([xi * scale + translate.x for xi in xs])
    # ynew = tuple([yi * scale + translate.y for yi in ys])

    xnew = tuple([xi * scale + translate.x for xi in ref.xs])
    ynew = tuple([yi * scale + translate.y for yi in ref.ys])

    # new = tuple((xnew[k], ynew[k]) for k in range(len(ref)))
    # new = tuple(zip(xnew, ynew))
    # new = coordinates(pairs=tuple(zip(xnew, ynew)))
    new = Points(pairs=tuple(zip(xnew, ynew)))
    return new


class TemplateFactory(NamedTuple):
    """Maps keys, which are converstion of tuple(int, int, int, int) to string, to a
    specific template.

    See https://github.com/sandialabs/sibl/blob/master/geo/doc/dual_quad_transitions.md
        for visual representations of these Template types.
    """

    key_0000: NamedTuple = dual_quad.Template_0000()

    # key_0001: NamedTuple = dual_quad.Template_0001()
    key_0001_r0_p0: NamedTuple = dual_quad.Template_0001_r0_p0()
    key_0001_r0_p1: NamedTuple = dual_quad.Template_0001_r0_p1()
    key_0001_r1_p0: NamedTuple = dual_quad.Template_0001_r1_p0()
    key_0001_r1_p1: NamedTuple = dual_quad.Template_0001_r1_p1()

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


class Cell:
    # def __init__(self, *, center: Coordinate, size: float):
    def __init__(self, *, center: Point2D, size: float):
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
            sw=Point2D(self.west, self.south),
            se=Point2D(self.east, self.south),
            ne=Point2D(self.east, self.north),
            nw=Point2D(self.west, self.north),
        )

    def contains(self, point: Point2D) -> bool:
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
        # TODO: determine if we want this to be consistent with winding number conventions
        return (
            point.x >= self.west
            and point.x <= self.east
            and point.y >= self.south
            and point.y <= self.north
        )

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
            center=Point2D(x=center_west_x, y=center_south_y), size=divided_size
        )
        self.nw = Cell(
            center=Point2D(x=center_west_x, y=center_north_y), size=divided_size
        )
        self.se = Cell(
            center=Point2D(x=center_east_x, y=center_south_y), size=divided_size
        )
        self.ne = Cell(
            center=Point2D(x=center_east_x, y=center_north_y), size=divided_size
        )

        self.has_children = True  # overwrite from False in __init__

        print("Finished cell division.")


# class QuadTree:
#     def __init__(
#         self, *, cell: Cell, level: int, level_max: int, points: tuple[Coordinate, ...]
#     ):
class QuadTree:
    def __init__(self, *, cell: Cell, level: int, level_max: int, points: Points):
        """A QuadTree is a specific instance of a cell with zero or more recursive cell
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
        # self.points = Points(pairs=tuple(filter(self.cell.contains, points.points2D)))
        _contained_points = tuple(filter(self.cell.contains, points.points2D))

        # If there is one or more point(s) inside of this parent cell, then subdivide.
        # if len(self.points) > 0:
        # if self.points.length > 0:
        if len(_contained_points) > 0:
            self.points = Points(pairs=_contained_points)

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

    def domain_dual(self) -> tuple[Domain, ...]:
        """Maps the quadtree to a collection of dualized domains.
        Returns the domains = ((mesh=(vertices, faces), boundaries),...) for all
        templates embedded in the quadtree.
        """
        _quad_levels_recursive = self.quad_levels_recursive()
        _domain_dual = QuadTree._domain_dual(
            cell=self.cell,
            level=0,
            quad_levels_recursive_subset=_quad_levels_recursive,
            partial=False,
        )
        return _domain_dual

    # def quad_levels_recursive(self) -> NestedInts:
    def quad_levels_recursive(self) -> tuple:
        qls = QuadTree._quad_levels(cell=self.cell, level=0)
        return qls

    def quad_levels(self) -> tuple[int, ...]:
        qls = self.quad_levels_recursive()
        return tuple(QuadTree._levels_flatten(nested=qls))

    @staticmethod
    def _child_vertices(
        cell: Cell,
    ) -> Quads:
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

    # def _quad_levels(*, cell: Cell, level: int) -> Ints:
    # def _quad_levels(*, cell: Cell, level: int) -> NestedInts:
    @staticmethod
    def _quad_levels(*, cell: Cell, level: int) -> tuple:
        """Given a cell, returns the cell's quad levels, and (recursively) the quad
        levels of the cell's children, grandchildren, et cetera.  Recursion ends when
        a cell level has no children.

        Example:
            Returns
                ((1,), (1,), (1,), ((2,), (2,), (2,) (2,)))
        """
        if cell.has_children:
            return (
                QuadTree._quad_levels(cell=cell.sw, level=level + 1),
                QuadTree._quad_levels(cell=cell.nw, level=level + 1),
                QuadTree._quad_levels(cell=cell.se, level=level + 1),
                QuadTree._quad_levels(cell=cell.ne, level=level + 1),
            )
        else:
            return (level,)

    @staticmethod
    def _domain_dual(
        *, cell: Cell, level: int, quad_levels_recursive_subset: tuple, partial: bool
    ) -> tuple[Domain, ...]:
        """Returns the dual domain encoded by the QuadTree."""

        _factory = TemplateFactory()

        subset_sw = quad_levels_recursive_subset[0]
        subset_nw = quad_levels_recursive_subset[1]
        subset_se = quad_levels_recursive_subset[2]
        subset_ne = quad_levels_recursive_subset[3]

        n_nested_sw = len(tuple(QuadTree._levels_flatten(subset_sw)))
        n_nested_nw = len(tuple(QuadTree._levels_flatten(subset_nw)))
        n_nested_se = len(tuple(QuadTree._levels_flatten(subset_se)))
        n_nested_ne = len(tuple(QuadTree._levels_flatten(subset_ne)))

        _template_key = template_key(
            quad_corners=tuple([n_nested_sw, n_nested_nw, n_nested_se, n_nested_ne]),
            level=level,
            partial=partial,
        )

        if _template_key == "key_unknown":

            # A known template cannot be fit to the combination of quad_corners,
            # so recursively march down until a key is found.

            # Also, capture the topology of the parent template, prepend to the
            # beginning of the recursion.

            # example: (1, 1, 1, 4) for Template_0001 parent
            # n_parent_quads = tuple(
            #     map(lambda x: len(x), (subset_sw, subset_nw, subset_se, subset_ne))
            # )
            n_parent_quads = tuple(
                [len(xi) for xi in (subset_sw, subset_nw, subset_se, subset_ne)]
            )

            # Example: ((1,), (1,), (1,), ((2,), (2,), (2,), (2,)))
            n_subquads_per_quad: Final = 4  # given transition from level -> level + 1
            quad_levels_recursive_parent = tuple(
                (
                    (
                        (level + 1,)
                        if x == 1
                        else tuple(repeat((level + 2,), n_subquads_per_quad))
                    )
                    for x in n_parent_quads
                )
            )

            # accumlate the parent part quad first
            _subdomain = QuadTree._domain_dual(
                cell=cell,
                level=level,
                quad_levels_recursive_subset=quad_levels_recursive_parent,
                partial=True,
            )

            # then accumlate each of the children
            if cell.sw.has_children:
                _subquad_sw = QuadTree._domain_dual(
                    cell=cell.sw,
                    level=level + 1,
                    quad_levels_recursive_subset=subset_sw,
                    partial=False,
                )
                _subdomain = _subdomain + _subquad_sw

            if cell.nw.has_children:
                _subquad_nw = QuadTree._domain_dual(
                    cell=cell.nw,
                    level=level + 1,
                    quad_levels_recursive_subset=subset_nw,
                    partial=False,
                )
                _subdomain = _subdomain + _subquad_nw

            if cell.se.has_children:
                _subquad_se = QuadTree._domain_dual(
                    cell=cell.se,
                    level=level + 1,
                    quad_levels_recursive_subset=subset_se,
                    partial=False,
                )
                _subdomain = _subdomain + _subquad_se

            if cell.ne.has_children:
                _subquad_ne = QuadTree._domain_dual(
                    cell=cell.ne,
                    level=level + 1,
                    quad_levels_recursive_subset=subset_ne,
                    partial=False,
                )
                _subdomain = _subdomain + _subquad_ne

            return _subdomain

        else:
            # A known template can be constructed.  Example, _template.name == "0001"
            _template = getattr(_factory, _template_key, None)
            assert _template  # _template should never be None at this point

            # _scaled_translated_vertices_dual = scale_then_translate(
            #     ref=_template.vertices_dual,
            #     scale=cell.size / 2.0,
            #     translate=cell.center,
            # )

            # _new_coordinates = coordinates(pairs=_scaled_translated_vertices_dual)
            # _new_coordinates = Points(pairs=_scaled_translated_vertices_dual)

            _new_coordinates = scale_then_translate(
                ref=Points(pairs=_template.vertices_dual),
                scale=cell.size / 2.0,
                translate=cell.center,
            )

            # temporary hard code to test key_0001
            # if _template_key == "key_0001":
            if "key_0001" in _template_key:
                _new_connectivity = _template.faces_dual + _template.faces_ports
                mesh = Mesh(
                    coordinates=_new_coordinates, connectivity=_new_connectivity
                )
            else:
                mesh = Mesh(
                    coordinates=_new_coordinates, connectivity=_template.faces_dual
                )

            domain = Domain(mesh=mesh, boundaries=_template.boundaries_dual)

            # return (mesh,)
            return (domain,)

    @staticmethod
    def _levels_flatten(nested: tuple) -> Iterable[int]:
        """Given a tuple of nest ints, yields an int in a flattened sequence.

        Example:
            Given:
            ((1,), (1,), (1,), ((2,), (2,), (2,), (2,)))
            Returns a generator for tuple of:
            (1, 1, 1, 2, 2, 2, 2,)
        """
        for i in nested:
            # yield from [i] if not isinstance(i, tuple) else QuadTree._tuple_flatten(i)
            yield from [i] if isinstance(i, int) else QuadTree._levels_flatten(i)

    @staticmethod
    def _quads_flatten(nested: Quads) -> Iterable[Quad]:
        """Given a tuple of nested quads, yields a quad in a flattened sequence."""
        for i in nested:
            yield from [i] if isinstance(i, Quad) else QuadTree._quads_flatten(i)


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
