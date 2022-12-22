# Copyright 2020 National Technology and Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
# certain rights in this software.


from typing import NamedTuple, Iterable
from itertools import cycle, tee
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from ptg.mesh_typing import (
    Edges,
    Face,
    Faces,
    FixedDisplacements,
    QuadVertices,
    Vertices,
    Vertex,
)


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
            b += (i,)  # overwrite
        else:
            # b += ((i[1], i[0]),)
            b += (tuple(reversed(i)),)  # overwrite
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


def inp_path_file_to_coordinates(*, pathfile: str) -> dict[str, Vertex]:
    """Given an .inp file, returns the coordinates as a dictionary.  The keys
    of the dictionary are a string index that contains the node number, which
    is generally nonsequential.  The values of the dictionary contain a tuple of
    floats that are the (x, y, z) position of the coordinate.
    """
    print(f"Reading coordinates from file: {pathfile}")
    keys = []
    values = []
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


def inp_path_file_to_connectivities(*, pathfile: str) -> Faces:
    """Given an .inp file, returns the element number and connectivity as a tuple
    of ints.  The first item in the tuple is the element number, which is generally
    non-sequential.  The remaining values in the tuple are the ordered connectivity
    of the element.
    """
    print(f"Reading connectivities from file: {pathfile}")
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


def inp_path_file_to_boundary(*, pathfile: str) -> FixedDisplacements:
    """Given an .inp file, returns the boundary as a dictionary.  The keys
    of the dictionary are a string index that contains the node number, which
    is generally nonsequential.  The values of the dictionary contain a tuple of
    degree of freedom numbers, 1, 2, and/or 3, as prescribed homogeneous
    boundary conditions (fixed x, y, and/or z displacements).
    """
    print(f"Reading boundary from file: {pathfile}")
    keys = []
    values = []
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
                        new_fixed_displacements = tuple(
                            map(lambda x: int(eval(x)), line)
                        )
                        values.append(new_fixed_displacements)
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


def faces_as_nodes_to_faces_as_vertices(
    *, faces: Faces, coordinates: dict[str, Vertex]
) -> tuple[tuple[Vertex, ...], ...]:
    result = tuple(tuple(coordinates[str(column)] for column in row) for row in faces)
    return result


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
    # figure_shown = options.get("figure_shown", False)
    color = options.get("color", "blue")
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
            color=color,
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

    # if figure_shown:
    #     plt.show()

    plt.close("all")

    # If we reach this point, we have finished the function.
    success = True  # overwrite False default
    return success


def perimeter_segment_lengths(*, coordinates: Vertices) -> tuple[float, ...]:
    pairs = pairwise_circular(coordinates)
    lengths = tuple()

    for item in pairs:
        point_i = np.asarray(item[0])
        point_k = np.asarray(item[1])
        vector_ik = np.subtract(point_k, point_i)
        len_ik = np.linalg.norm(vector_ik)
        lengths = lengths + (len_ik,)

    return lengths


class quad_node_1(NamedTuple):
    """Provides (xi, eta) = (a, b) values of parametric variables
    at discrete node point 1 of quadrilateral element.
    """

    a: float = -1.0
    b: float = -1.0


class quad_node_2(NamedTuple):
    """Provides (xi, eta) = (a, b) values of parametric variables
    at discrete node point 2 of quadrilateral element.
    """

    a: float = 1.0
    b: float = -1.0


class quad_node_3(NamedTuple):
    """Provides (xi, eta) = (a, b) values of parametric variables
    at discrete node point 3 of quadrilateral element.
    """

    a: float = 1.0
    b: float = 1.0


class quad_node_4(NamedTuple):
    """Provides (xi, eta) = (a, b) values of parametric variables
    at discrete node point 4 of quadrilateral element.
    """

    a: float = -1.0
    b: float = 1.0


class quad_center(NamedTuple):
    """Provides (xi, eta) = (a, b) values of parametric variables
    at center of quadrilateral element.
    """

    a: float = 0.0
    b: float = 0.0


def jacobian_of_quad(
    *, xi: float, eta: float, vertices: QuadVertices
) -> tuple[tuple[float, float], tuple[float, float]]:

    assert len(vertices) == 4
    assert -1.0 <= xi and xi <= 1.0
    assert -1.0 <= eta and eta <= 1.0

    A = 0.25 * np.array(
        [
            [-1.0 + eta, 1.0 - eta, 1.0 + eta, -1.0 - eta],
            [-1.0 + xi, -1.0 - xi, 1.0 + xi, 1.0 - xi],
        ]
    )

    B = np.asarray(vertices)

    C = np.matmul(A, B)
    return ((C[0, 0], C[0, 1]), (C[1, 0], C[1, 1]))


def det_jacobian_of_quad(*, xi: float, eta: float, vertices: QuadVertices) -> float:
    J = jacobian_of_quad(xi=xi, eta=eta, vertices=vertices)
    return np.linalg.det(np.asarray(J))


def det_jacobian_of_quad_check(
    *, xi: float, eta: float, vertices: QuadVertices
) -> float:
    # The det(J) = c0 + c1 * a + c2 * b, where
    ((x1, y1), (x2, y2), (x3, y3), (x4, y4)) = vertices
    c0 = ((x1 - x3) * (y2 - y4) - (x2 - x4) * (y1 - y3)) / 8.0
    c1 = ((x3 - x4) * (y1 - y2) - (x1 - x2) * (y3 - y4)) / 8.0
    c2 = ((x2 - x3) * (y1 - y4) - (x1 - x4) * (y2 - y3)) / 8.0

    value = c0 + c1 * xi + c2 * eta
    return value


def nodal_areas_of_quad(*, vertices: QuadVertices) -> tuple[float, float, float, float]:

    ((x1, y1), (x2, y2), (x3, y3), (x4, y4)) = vertices

    e1 = np.array([(x2 - x1), (y2 - y1), 0.0])
    e2 = np.array([(x3 - x2), (y3 - y2), 0.0])
    e3 = np.array([(x4 - x3), (y4 - y3), 0.0])
    e4 = np.array([(x1 - x4), (y1 - y4), 0.0])

    # normals from edges
    N1 = np.cross(e4, e1)
    N2 = np.cross(e1, e2)
    N3 = np.cross(e2, e3)
    N4 = np.cross(e3, e4)

    # normal at center of quad is defined up and out of the page, +z direction
    nc = np.array([0.0, 0.0, 1.0])

    # retain this dot product formalism from the 3D case to accurately capture
    # 2D cases when the Jacobian goes negative
    a1 = np.dot(N1, nc)
    a2 = np.dot(N2, nc)
    a3 = np.dot(N3, nc)
    a4 = np.dot(N4, nc)

    areas = tuple([a1, a2, a3, a4])

    return areas


def minimum_jacobian_of_quad(*, vertices: QuadVertices) -> float:
    areas = nodal_areas_of_quad(vertices=vertices)
    return min(areas)


def minimum_scaled_jacobian_of_quad(*, vertices: QuadVertices) -> float:

    # signed areas
    areas = nodal_areas_of_quad(vertices=vertices)

    # edge lengths
    ls = perimeter_segment_lengths(coordinates=vertices)

    # edge length combinations
    L4L1 = ls[3] * ls[0]
    L1L2 = ls[0] * ls[1]
    L2L3 = ls[1] * ls[2]
    L3L4 = ls[2] * ls[3]

    lilk = tuple([L4L1, L1L2, L2L3, L3L4])

    scaled_js = tuple([a / L for (a, L) in zip(areas, lilk)])

    return min(scaled_js)
