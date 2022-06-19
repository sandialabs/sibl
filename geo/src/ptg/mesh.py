from typing import NamedTuple, Iterable
from itertools import cycle, tee
from pathlib import Path

import matplotlib.pyplot as plt

# Type alias for functional style methods
# https://docs.python.org/3/library/typing.html#type-aliases
Vertex = tuple[float, ...]
Face = tuple[int, ...]
Faces = tuple[Face, ...]
Edge = tuple[int, int]
Edges = tuple[Edge, ...]


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


def adjacency_upper_diagonal(x: Face) -> Edges:
    """Given a single face, composed of integer node numbers, returns indices
    of all edges that compose that face as the upper diagonal non-zero elements
    of the adjacency matrix.
    """
    a = pairwise_circular(x)
    b = tuple()
    for i in a:
        if i[0] < i[1]:
            # b += ((i[0], i[1]),)
            b += (i,)
        else:
            # b += ((i[1], i[0]),)
            b += (tuple(reversed(i)),)
    return b


def adjacencies_upper_diagonal(xs: Faces) -> Edges:
    """Given a Faces collection, returns the indices of all edges that compose
    the union of Face items as the upper diagonal non-zero elements of the
    adjacency matrix.
    """
    a = tuple()
    for x in xs:
        es = adjacency_upper_diagonal(x)
        for e in es:
            if e not in a:
                a += (e,)
    return a


def inp_path_file_to_stream(*, pathfile: str):
    pf = Path(pathfile)
    if not pf.is_file():
        print(f"Error: no such file: {pf}")
        raise FileNotFoundError
    return open(str(pf), "rt")


def inp_path_file_to_coordinates(*, pathfile: str):
    """Given an .inp file, returns the coordinates as a dictionary.  The keys
    of the dictionary are a string index that contains the node number, which
    is generally nonsequential.  The values of the dictionary contain a tuple of
    floats that are the (x, y, z) position of the coordinate.
    """
    keys = []
    values = []
    # coordinates = ()  # emtpy tuple
    with inp_path_file_to_stream(pathfile=pathfile) as f:
        try:
            line = f.readline()
            while line:
                if "*NODE" in line or "*Node" in line:
                    # collect all nodes
                    line = f.readline()  # get the next line
                    while "*" not in line:
                        line = line.split(",")
                        keys.append(
                            line[0]
                        )  # collect the node number, generally nonseqential
                        line = line[1:]  # ignore the first column node number
                        line = [x.strip() for x in line]  # remove whitespace and \t \n
                        new_coordinate = tuple(map(lambda x: float(eval(x)), line))
                        values.append(new_coordinate)
                        # coordinates += (new_coordinate),
                        line = f.readline()
                else:
                    line = f.readline()
            print(f"Finished reading file: {pathfile}")
        except SyntaxError:
            print(f"Cannot read file: {pathfile}")
            raise OSError
    # return coordinates
    zip_iterator = zip(keys, values)
    return dict(zip_iterator)


def inp_path_file_to_connectivities(*, pathfile: str):
    """Given an .inp file, returns the element number and connectivity as a tuple
    of ints.  The first item in the tuple is the element number, which is generally
    non-sequential.  The remaining values in the tuple are the ordered connectivity
    of the element.
    """
    connectivities = ()  # empty tuple
    with inp_path_file_to_stream(pathfile=pathfile) as f:
        try:
            line = f.readline()
            while line:
                if "*ELEMENT" in line or "*Element" in line:
                    # collect all elements
                    line = f.readline()  # get the next line
                    while "*" not in line and len(line) > 0:
                        line = line.split(",")
                        # line = line[1:]  # ignore the first column node number
                        line = [x.strip() for x in line]  # remove whitespace and \t \n
                        new_connectivity = tuple(map(lambda x: int(eval(x)), line))
                        connectivities += ((new_connectivity),)
                        line = f.readline()
                else:
                    line = f.readline()
            print(f"Finished reading file: {pathfile}")
        except NameError:
            print(f"Cannot read file: {pathfile}")
            raise OSError
    return connectivities


def inp_path_file_to_boundary(*, pathfile: str):
    """Given an .inp file, returns the boundary as a dictionary.  The keys
    of the dictionary are a string index that contains the node number, which
    is generally nonsequential.  The values of the dictionary contain a tuple of
    degree of freedom as in the boundary (True) thus prescribed, or not in the
    boundary (False) and thus an active degree of freedom.
    """
    keys = []
    values = []
    # coordinates = ()  # emtpy tuple
    with inp_path_file_to_stream(pathfile=pathfile) as f:
        try:
            line = f.readline()
            while line:
                if "*BOUNDARY" in line or "*Boundary" in line:
                    # collect all nodes
                    line = f.readline()  # get the next line
                    while "*" not in line:
                        line = line.split(",")
                        keys.append(
                            line[0]
                        )  # collect the node number, generally nonseqential
                        line = line[1:]  # ignore the first column node number
                        line = [x.strip() for x in line]  # remove whitespace and \t \n
                        in_boundary = [False, False]  # default to 2D both dof active
                        # flip to boundary range
                        rr = tuple(map(lambda x: int(eval(x)), line))
                        # include end of domain, thus +1
                        flips = tuple(range(rr[0], rr[1] + 1))
                        for k in flips:
                            in_boundary[k - 1] = True  # 0-index in Python
                        values.append(tuple(in_boundary))
                        # coordinates += (new_coordinate),
                        line = f.readline()
                else:
                    line = f.readline()
            print(f"Finished reading file: {pathfile}")
        except NameError:
            print(f"Cannot read file: {pathfile}")
            raise OSError
    # return coordinates
    zip_iterator = zip(keys, values)
    return dict(zip_iterator)


def plot_mesh(*, nodes, edges, options) -> bool:
    """
    Plots the .inp file nodes, edges, with keyword options.
    Returns `True` if successful, `False` otherwise.
    """
    success = False

    title = options.get("title", "")
    dpi = options.get("dpi", 100)
    height = options.get("height", 3.0)
    width = options.get("width", 3.0)
    nodes_shown = options.get("nodes_shown", True)
    node_numbers_shown = options.get("node_numbers_shown", False)
    serialize = options.get("serialize", False)
    basename = options.get("basename", Path(__file__).stem)
    extension = options.get("extension", ".png")  # ".png" | ".pdf" | ".svg"

    (ix, iy) = (0, 1)  # global index with (x, y) semantic

    fig = plt.figure(figsize=(width, height), dpi=dpi)
    # ax = plt.gca()
    ax = fig.gca()

    for edge in edges:
        edge_points = [nodes[ii] for ii in map(str, edge)]
        # xs = [nodes[e - 1][ix] for e in edge]  # nodes[e-1] to convert from 1-index to 0-index
        # ys = [nodes[e - 1][iy] for e in edge]
        xs = [point[ix] for point in edge_points]
        ys = [point[iy] for point in edge_points]
        # plt.plot(xs, ys, **plot_kwargs)
        plt.plot(
            xs,
            ys,
            alpha=1.0,
            linewidth=0.5,
            color="blue",
            marker=None,
            markerfacecolor="red",
        )

    ax.set_aspect("equal")
    ax.set_title(title)

    if nodes_shown:
        # plot nodes
        xs = [item[ix] for item in nodes.values()]
        ys = [item[iy] for item in nodes.values()]
        ax.scatter(
            xs,
            ys,
            linestyle="solid",
            edgecolor="black",
            color="yellow",
            alpha=0.9,
            s=100,
        )

    if node_numbers_shown:
        # plot node numbers
        for item in nodes.items():
            c = item[0]
            x = item[1][ix]
            y = item[1][iy]
            ax.text(x, y, c, horizontalalignment="center", verticalalignment="center")

    if serialize:
        # extension = ".png"  # ".png" | ".pdf" | ".svg"
        # filename = Path(__file__).stem + "_" + test_case + extension
        filename = basename + extension
        pathfilename = Path.cwd().joinpath(filename)
        fig.savefig(pathfilename, bbox_inches="tight", pad_inches=0)
        print(f"Serialized to {pathfilename}")

    plt.close("all")

    # If we reach this point, we have finished the function.
    success = True  # overwrite False default
    return success
