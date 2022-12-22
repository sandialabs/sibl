# Copyright 2020 National Technology and Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
# certain rights in this software.


from ptg.point import Point2D, Points


def is_left(P2: Point2D, *, P0: Point2D, P1: Point2D) -> int:
    """Determines if the probe point P2 is to the left, on, or to the right of
    an infinite line through the line segment from point P0 to P1.  This is
    equivalent to taking the cross product between vector a = (P1 - P0) and
    vector b = (P2 - P0), and determining if that cross product is
        positive (point P2 is to the to the left of the line),
        zero (point P2 is on the line), or
        negative (point P2 is to the right of the line).

    Arguments:
        P2 (Point2D): The probe point with coordinates (x2, y2) that is found
            to be to the left, on, or to the right of the infinite line going through
            the directed line segment from P0 to P1.

    Keyword Arguments:
        P0 (Point2D): The beginning point of the line segment with coordinates
            (x0, y0).
        P1 (Point2D): The ending point of the line segment with coordinates
            (x1, y2).

    Returns:
        int in [-1, 0, 1] where
            1: Point P2 is to the left of the line from P0 to P1.
            0: Point P2 is on the line from P0 to P1.
           -1: Point P2 is to the right of the line from P0 to P1.
    """
    cross_product = (P1.x - P0.x) * (P2.y - P0.y) - (P2.x - P0.x) * (P1.y - P0.y)

    if cross_product > 0:
        return 1
    elif cross_product < 0:
        return -1
    else:
        return 0

    """Copyright notice:
    This function is an adaption of the 'isLeft()' function by Daniel Sunday.
    Copyright 2001, 2012, 2021 Dan Sunday
    This code may be freely used at modified for any purpose
    provided that this copyright notice is included with it.
    There is no warranty for this code, and the author of it cannot
    be held liable for any real or imagined damage from its use.
    Users of this code must verify correctness for their application.
    """


class Polygon2D:
    def __init__(self, *, boundary: Points):
        """A closed polygon in 2D.

        Arguments:
            boundary (Points): is a tuple of (n+1) pairs of floats,
                ((x0, y0), (x1, y1), ... (xn, yn)), that describe the path sequence
                of the boundary.  The boundary is closed, so the final boundary
                sgement connects from (xn, yn) to (x0, y0).  There are thus (n+1)
                line segments that compose the boundary.

        Raises:
            ValueError if len(boundary) < 3. A minimum of three points must be used
                to specify a boundary.

        References:
            Nice graphically illustration of Family Tree of polygons:
            https://www.mathsisfun.com/quadrilaterals.html
        """

        if boundary.length < 3:
            raise ValueError("Number of boundary points must be >= 3.")

        self._boundary = boundary

    @property
    def length(self) -> int:
        """Returns the number of points composing the Polygon2D."""
        return self._boundary.length

    def winding_number(self, probe: Point2D) -> int:
        """Calculates the winding number, which is the number of times a polygon wraps,
        in a counter-clockwise direction taken as a positive result, around the probe
        point.

        Arguments:
            probe (Point2D): The probe point with coordinates (P.x, P.y) that
                is used to determine the winding number of the polygon.

        Returns:
            int: A integer number of times the polygon has wrapped around the probe
                point as follows:
                A value of zero indicates the probe point is outside of the polygon.
                A positive number indicates the number of times the polygon wraps
                    around the probe point in a counter-clockwise direction.
                A negative number indicates the number of times the polygon wraps
                    around the probe point in a clockwise direction.

        References:
            For additional reading, see https://en.wikipedia.org/wiki/Winding_number
            or Anirudh Topiwala (https://anirudhtopiwala.com/) page on Medium
            https://towardsdatascience.com/tagged/winding-number 09 Sep 2020.
        """

        wn = 0  # The winding number counter, defaults to zero, outside of the polygon

        """
        The algorithm in Sunday [sunday2021practical], page 49,
        uses a W.E.T. boundary vertex description with the first vertex repeated
        as the last vertex in the collection of vertices.
        Sunday defines a polygon with V[n+1] vertices as explicitly closed, such
        that V[n] = V[0].  For example, a square polygon is an n-gon where n=4, thus
        five points are used {V0, V1, V2, V3, V4}.

        In contrast, we have defined all polygons in this class to be closed, a priori.
        We thus prefer a D.R.Y. boundary vertex description.  For example, a square
        polygon is sufficiently described with four points {V0, V1, V2, V3} where
        the four edges are V0-V1, V1-V2, V2-V3, and V3-V0.

        @book{sunday2021practical,
          title     = {Practical Geometry Algorithms with {C++} Code},
          author    = {Sunday, Daniel},
          year      = {2021},
          publisher = {Amazon KDP},
          note      = {https://www.geomalgorithms.com/}
        }
        """

        # Use Sunday convention to repeat the first vertex as the last vertex.
        V = self._boundary.points2D + (self._boundary.points2D[0],)

        # Match Sunday's probe point notation
        P = probe

        # loop over each edge segment composing the polygon
        for i in range(len(V) - 1):
            if V[i].y <= P.y:  # start y <= P.y
                if V[i + 1].y > P.y:  # an upward crossing
                    if is_left(P2=P, P0=V[i], P1=V[i + 1]) > 0:
                        wn += 1  # have a valid up intersect
            else:  # start y > P.y (no test needed)
                if V[i + 1].y <= P.y:  # a downward crossing
                    if is_left(P2=P, P0=V[i], P1=V[i + 1]) < 0:  # P right of edge
                        wn -= 1  # have a valid down intersect

        return wn

        """Copyright notice:
        This function is an adaption of the 'wn_PnPoly()' function by Daniel Sunday.
        Copyright 2001, 2012, 2021 Dan Sunday
        This code may be freely used at modified for any purpose
        provided that this copyright notice is included with it.
        There is no warranty for this code, and the author of it cannot
        be held liable for any real or imagined damage from its use.
        Users of this code must verify correctness for their application.
        """

    def contains(self, *, probe: Point2D) -> bool:
        """Determines if a probe Point lies within the boundary of the Polygon2D.

        Arguments:
            probe (Point2D): The probe point with coordinates (P.x, P.y) that is
                determined to be contained or not contained in hte Polygon2D.
                For a square Polygon2D, a point:
                    on the bottom or left boundary is considered "in" (contained),
                    on the top or right boundary is considered "out" (not contained),
                        bottom-left corner is considered "in"
                        top-left, bottom-right, top-right coners are considered "out"

        Returns:
            bool: True if the point is contained in the boundary, False otherwise.
        """
        if self.winding_number(probe=probe) == 0:
            return False
        else:
            return True
