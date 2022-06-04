from typing import NamedTuple, Iterable
from itertools import cycle, tee

# Type alias for functional style methods
# https://docs.python.org/3/library/typing.html#type-aliases
Vertex = tuple[float, ...]
Face = tuple[int, ...]


class Mesh(NamedTuple):
    """Defines a generic mesh type, possibly 1D, 2D, or 3D, composed of
    vertices and faces.  A vertex is a collection of float values, and vertices
    are a collection of vertex values.  A face is a collection of int values,
    where each value is an index into specific vertex in the vertices
    collection.  Vertices are a collection of vertex values.  Faces are a
    collection of ints, where each int is the index into the vertices tuple.
    """

    # vertices: tuple[tuple[float, ...], ...]
    # faces: tuple[tuple[int, ...], ...]

    vertices: tuple[Vertex, ...]
    faces: tuple[Face, ...]


def pairwise(x: Iterable) -> Iterable:
    """Return successive overlapping pairs taken from the input iterable.

    The number of 2-tuples in the output iterator will be one fewer than the
    number of inputs. It will be empty if the input iterable has fewer than
    two values.

    Example:
        pairwise('ABCDEFG') --> AB BC CD DE EF FG

    This appears to be implemented in Python 3.10
    https://docs.python.org/3/library/itertools.html#itertools.pairwise
    but we currently use 3.9, so we implement `pairwise` here.
    """
    a, b = tee(x)
    next(b, None)
    return zip(a, b)


def pairwise_circular(x: Iterable) -> Iterable:
    """Return successive overlapping pairs taken from the input iterable, with
    a circular loop back to the first element.

    The number of 2-tuples in the output iterator will be one fewer than the
    number of inputs. It will be empty if the input iterable has fewer than
    two values.

    Example:
        pairwise('ABCDEFG') --> AB BC CD DE EF FG GA
    """
    # a, b = tee(x)
    # c = cycle(b)
    # next(c)
    # return zip(a, c)
    a = cycle(x)
    next(a)
    return zip(x, a)


def pairwise_loop_first(x: tuple[int, ...]) -> tuple[tuple[int, int]]:
    augmented = x + (x[0],)
    paired = tuple(pairwise(x=augmented))
    return paired


def upper_diagonal(x: tuple[int, int]) -> tuple[int, int]:
    """Given (i, j) index in a symmtric matrix M, if
    (i, j) is in the lower diagonal, return the (j, i)
    index, otherwise return the (i, j) index."""
    if x[0] > x[1]:
        return tuple(reversed(x))
    else:
        return x


# def adjacency_vector(faces: Iterable):
#     pairs = pairwise_loop_first(face) for face in faces
#     bb = tuple([upper_diagonal(pair) for pair in pairs])
#     return bb


# def all_pairs(x: Iterable) -> tuple(tuple[int, int]):
#     aa = tuple([xi for xi in x])
#     return aa


# def adjacency_vector(mesh: Mesh) -> tuple[tuple[int, int]]:
#    fs = mesh.faces
