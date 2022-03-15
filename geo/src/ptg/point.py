from typing import NamedTuple


class Point2D(NamedTuple):
    """Creates a coordinate as a (x, y) pair of floats."""

    x: float  # x-coordinate
    y: float  # y-coordinate


class Points:
    def __init__(self, *, pairs: tuple[tuple[float, float], ...]):
        """Given a tuple of (x, y) float pairs, creates a
        collection of Point2D object.

        Argments:
            pairs (tuple of tuple of floats), e.g.,
                ((x0, y0), (x1, y1), ... (xn, yn))
        """
        self._pairs = pairs
        self._xs, self._ys = zip(*pairs)

    @property
    def xs(self) -> tuple[float, ...]:
        """Returns the x coordinates of the Points."""
        return self._xs

    @property
    def ys(self) -> tuple[float, ...]:
        """Returns the y coordinates of the Points."""

        return self._ys

    @property
    def length(self) -> int:
        """Returns the length of the Points collection."""
        return len(self._xs)

    @property
    def pairs(self) -> tuple[tuple[float, float], ...]:
        """Returns the original pairs used to create the Points."""
        return self._pairs

    @property
    def points2D(self) -> tuple[Point2D, ...]:
        """Returns the original pairs with each pair cast as
        a Point2D object.
        """
        return tuple(map(Point2D, self._xs, self._ys))
