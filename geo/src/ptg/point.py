# Copyright 2020 National Technology and Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
# certain rights in this software.


"""Creates a Point composite type composed of (x, y) float pairs."""
from typing import NamedTuple, Iterable


def pairs(
    x_coordinates: Iterable[float], y_coordinates: Iterable[float]
) -> tuple[tuple[float, float], ...]:
    """Given a sequence of coordinates in x and y, returns those items as pairs.

    This uses the zip() function and returns a zip object, which is an iterator
    of tuples where the first item in each passed iterator is paired together,
    and then the second item in each passed iterator are paired together etc.

    If the passed iterators have different lengths, the iterator with the fewest
    number of items decides the length of the new iterator.
    """
    pairs = tuple(zip(x_coordinates, y_coordinates))
    return pairs


def quadrant_one(
    pairs: tuple[tuple[float, float], ...]
) -> tuple[tuple[float, float], ...]:
    """Given (x, y) pairs, returns a subset of those that live the first quadrant."""
    return tuple(filter(lambda p: p[0] >= 0 and p[1] >= 0, pairs))


def quadrant_two(
    pairs: tuple[tuple[float, float], ...]
) -> tuple[tuple[float, float], ...]:
    """Given (x, y) pairs, returns a subset of those that live the second quadrant."""
    return tuple(filter(lambda p: p[0] < 0 and p[1] >= 0, pairs))


def quadrant_three(
    pairs: tuple[tuple[float, float], ...]
) -> tuple[tuple[float, float], ...]:
    """Given (x, y) pairs, returns a subset of those that live the third quadrant."""
    return tuple(filter(lambda p: p[0] < 0 and p[1] < 0, pairs))


def quadrant_four(
    pairs: tuple[tuple[float, float], ...]
) -> tuple[tuple[float, float], ...]:
    """Given (x, y) pairs, returns a subset of those that live the fourth quadrant."""
    return tuple(filter(lambda p: p[0] >= 0 and p[1] < 0, pairs))


class Point2D(NamedTuple):
    """Creates a coordinate as a (x, y) pair of floats."""

    x: float  # x-coordinate
    y: float  # y-coordinate


class Points:
    """Constructs a collection of Point items."""

    def __init__(self, *, pairs: tuple[tuple[float, float], ...]):
        """Given a tuple of (x, y) float pairs, creates a
        collection of Point2D object.

        Arguments:
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
