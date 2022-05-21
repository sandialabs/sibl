"""This module provides translation functions for `.mesh` file types
and `.inp` file types.
"""

import argparse
from datetime import datetime
from pathlib import Path
import pytz
import sys

from typing import Final, NamedTuple


class MeshFileVertex(NamedTuple):
    """A vertex structure in a `.mesh` file style.

    Example:  The structure appears, in context, three times in the
    snippet below (a subset of 28056 vertices):
    ...
    Vertices
    28056
    -0.546578 -0.868124 -0.071433 0  <-- a single vertex
    -0.515340 -0.866041 -0.071433 0
    -0.550482 -0.861876 -0.092258 0
    ...
    """

    x: float  # x-coordinate
    y: float  # y-coordinate
    z: float  # z-coordinate
    face_id: int  # face number


class MeshFileHexahedron(NamedTuple):
    """A single hexahedron structure in a `.mesh` file style.

    Example:  The structure appears, in context, three times in the
    snippet below (a subset of 8 hexahedra):
    ...
    Hexahedra
    8
    1 2 5 4 10 11 14 13 1  <-- a single hexahedron
    2 3 6 5 11 12 15 14 1
    3 5 8 7 13 14 17 16 1
    ...
    """

    # Eight nodes of int type describe a single hexahedron nodal indices.
    nodes: tuple[int, int, int, int, int, int, int, int]
    vol_id: int


class InpFileNode(NamedTuple):
    """A single node structure in .inp file style.

    Example:  The structure appears, in context, three times in the
    snippet below:
    ...
    *Node
    1, -0.546578, -0.868124, -0.0714333  <-- a single node
    2, -0.515340, -0.866041, -0.0714333
    3, -0.550482, -0.861876, -0.0922586
    ...
    """

    node_id: int  # an integer node number
    x: float  # x-coordinate
    y: float  # y-coordinate
    z: float  # z-coordinate


def string_to_vertex(*, vertex_string: str) -> MeshFileVertex:
    """Converts a `vertex_string` (e.g., `x y z face_id`) found in a `.mesh` file
    to a `MeshFileVertex`.
    """
    items = vertex_string.split()
    return MeshFileVertex(
        x=float(items[0]),
        y=float(items[1]),
        z=float(items[2]),
        face_id=int(items[3]),
    )


def vertex_to_node(*, node_id: int, vertex: MeshFileVertex) -> InpFileNode:
    """Converts a `MeshFileVertex` into a `InpFileNode` bearing a `node_id`
    node number."""
    return InpFileNode(node_id=node_id, x=vertex.x, y=vertex.y, z=vertex.z)


def node_to_string(*, node: InpFileNode) -> str:
    """Converts a `InpFileNode` into an equivalent string, suitable for writing
    to a `.inp` file.
    """
    items = (node.node_id, node.x, node.y, node.z)
    return ", ".join(map(str, items)) + "\n"


def vertex_string_to_node_string(*, node_id: int, vertex_string: str) -> str:
    """Converts a `vertex_string` (e.g., `x y z face_id`) found in a `.mesh` file
    into an equivalent string with `node_id` node number, suitable for writing
    to a `.inp` file.
    """
    a = string_to_vertex(vertex_string=vertex_string)
    b = vertex_to_node(node_id=node_id, vertex=a)
    c = node_to_string(node=b)
    return c


def string_to_hexahedron(*, hex_string: str) -> MeshFileHexahedron:
    """Converts a `hex_string` (e.g., `n1 n2 n3 n4 n5 n6 n7 n8 vol_id`) found in
    a `.mesh` file to a `MeshFileHexahedron`.
    """
    items = hex_string.split()
    nodes = tuple(map(int, items[0:8]))
    vol = int(items[8])
    return MeshFileHexahedron(nodes=nodes, vol_id=vol)


def hexahedron_string_to_element_string(*, element_id: int, hex_string: str) -> str:
    """Converts a `hex_string` (e.g., `n1 n2 n3 n4 n5 n6 n7 n8 vol_id`) found in
    a `.mesh` file to an equivalent string with `element_id` element number,
    suitable for writing to a `.inp` file.
    """
    a = str(element_id) + ", "
    b = string_to_hexahedron(hex_string=hex_string)
    c = a + ", ".join(map(str, b.nodes)) + "\n"
    return c


def translate(*, path_mesh_file: str) -> bool:
    """Given a string that contains a valid path and file name to
    a `.mesh` file, creates a `.inp` file in the same path location.
    Returns `True` if successful, `False` otherwise.
    """
    success = False

    input_path_file = Path(path_mesh_file)

    if not input_path_file.is_file():
        raise FileNotFoundError

    input_path = input_path_file.parent
    input_file_no_ext = input_path_file.stem
    output_file_ext: Final[str] = ".inp"
    output_file = input_file_no_ext + output_file_ext
    output_path_file = input_path.joinpath(output_file)

    input_path_file_str: Final[str] = str(input_path_file)
    output_path_file_str: Final[str] = str(output_path_file)

    with open(input_path_file_str, "rt") as in_stream:
        # line = in_stream.readline()

        with open(output_path_file_str, "wt") as out_stream:
            # out_stream.write(line)
            now = datetime.now(pytz.utc)
            now_str = now.strftime("%Y-%m-%d %H:%M:%S (UTC)")
            header = "***** " + __file__ + "\n"
            header += "***** translated from " + input_path_file_str + "\n"
            header += "***** to " + output_path_file_str + "\n"
            header += "***** on " + now_str + "\n"
            out_stream.write(header)

            for line in in_stream:
                if "Vertices" in line:
                    n_vertices = int(in_stream.readline().strip())
                    out_stream.write(
                        "********************************** N O D E S **********************************\n"
                    )
                    out_stream.write("*NODE, NSET=ALLNODES\n")
                    for i in range(1, n_vertices + 1):
                        line = in_stream.readline()
                        out_line = vertex_string_to_node_string(
                            node_id=i, vertex_string=line
                        )
                        out_stream.write(out_line)
                elif "Hexahedra" in line:
                    n_hexes = int(in_stream.readline().strip())
                    out_stream.write(
                        "********************************** E L E M E N T S ****************************\n"
                    )
                    out_stream.write("*ELEMENT, TYPE=C3D8R\n")
                    for i in range(1, n_hexes + 1):
                        line = in_stream.readline()
                        out_line = hexahedron_string_to_element_string(
                            element_id=i, hex_string=line
                        )
                        out_stream.write(out_line)
                # else:
                # skip the current line and continue to the next line

    # If we reach this point, the input and output buffers are not closed
    # and the function was successful.
    success = True  # overwrite False default
    return success


def main(argv):

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "mesh_file",
        help="the .mesh file input",
    )

    args = parser.parse_args()
    mesh_file = args.mesh_file

    print(f"{__file__} is translating:\n{mesh_file}")
    translated = translate(path_mesh_file=mesh_file)
    success: Final[str] = "success: translation completed"
    failure: Final[str] = "error: translation unsucessful"
    print(success if translated else failure)


if __name__ == "__main__":
    """Runs the translator from the command line.
    Example:
    $ conda activate siblenv
    $ cd ~/sibl/geo/src/ptg
    $ python translator.py ../../data/mesh/hexa_2x2x2.mesh

    produces hexa_2x2x2.inp
    """
    main(sys.argv[1:])
