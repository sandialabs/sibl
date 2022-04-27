"""This module provides translation functions for '.mesh' file types
and '.inp' file types.
"""


from typing import NamedTuple


class inp_file_node(NamedTuple):
    """Creates a node structure in .inp file style.

    Example:  The structure appears three times in the snippet below
    ...
    *Node
    1, -0.54657809374999999, -0.86812413750000006, -0.071433312500000054
    2, -0.51534003125000005, -0.86604159999999997, -0.071433312500000054
    3, -0.55048285156249999, -0.861876525, -0.092258687500000047
    ...
    """

    node_id: int  # an integer node number
    x: float  # x-coordinate
    y: float  # y-coordinate
    z: float  # z-coordinate


class mesh_file_vertex(NamedTuple):
    """Creates a vertex structure in .mesh file style.
    Example:  The structure appears three times in the snippet below
    ...
    Vertices
    28056
    -0.54657809374999999 -0.86812413750000006 -0.071433312500000054 0
    -0.51534003125000005 -0.86604159999999997 -0.071433312500000054 0
    -0.55048285156249999 -0.861876525 -0.092258687500000047 0
    ...
    """

    x: float  # x-coordinate
    y: float  # y-coordinate
    z: float  # z-coordinate
    face_id: int  # an integer face number


def io_inp_file_node(node: inp_file_node) -> str:
    """Given an item of 'inp_file_node' type, returns the equivalent string
    for serialization to an '.inp'_file.
    """
    items = (node.node_id, node.x, node.y, node.z)
    return ", ".join(map(str, items)) + "\n"


def io_mesh_file_vertex(input: str) -> mesh_file_vertex:
    """Given a string describing a vertex in a '.mesh' format, e.g.,
    'x y z face_id', returns an item of 'mesh_file_vertex' type.
    """
    items = input.split()
    return mesh_file_vertex(
        x=float(items[0]), y=float(items[1]), z=float(items[2]), face_id=int(items[3])
    )


def io_mesh_file_vertex_to_inp_file_node(*, node_id: int, input: str) -> str:
    """Given a '.mesh' file vertex string, returns an '.inp' file node type
    string suitable for serialization into an '.inp' file.
    """
    return io_inp_file_node(
        translate(node_id=node_id, vertex=io_mesh_file_vertex(input))
    )


def translate(*, node_id: int, vertex: mesh_file_vertex) -> inp_file_node:
    """Given an item of 'mesh_file_vertex' type, returns an equivalent
    item in 'inp_file_node' type given a given node number 'node_id'."""
    return inp_file_node(node_id=node_id, x=vertex.x, y=vertex.y, z=vertex.z)
