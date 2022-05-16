"""This module provides translation functions for '.mesh' file types
and '.inp' file types.
"""

import argparse
from pathlib import Path
import sys

from typing import Final, NamedTuple


class inp_file_node(NamedTuple):
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


class mesh_file_hexahedron(NamedTuple):
    """A single hexahedron structure in a '.mesh' file style.

    Example:  The structure appears, in context, three times in the
    snippet below:
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


class mesh_file_hexahedra(NamedTuple):
    """A collection of mesh file hexahedron plus header data.

    Example:  The structure appears as a header, an element count of 3, and
    three hexahedra elements:
    ...
    Hexahedra
    3
    1 2 5 4 10 11 14 13 1
    2 3 6 5 11 12 15 14 1
    3 5 8 7 13 14 17 16 1
    ...
    """

    n_hexahedra: int
    hexahedra: tuple[mesh_file_hexahedron, ...]
    label: str = "Hexahedra"


class mesh_file_vertex(NamedTuple):
    """A vertex structure in a '.mesh' file style.

    Example:  The structure appears three times in the snippet below, where
    only three of 28056 vertex items are shown:
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


class mesh_file_vertices(NamedTuple):
    """A collection of mesh file vertex types plus header data.
    Example:
    ...
    Vertices
    28056
    -0.54657809374999999 -0.86812413750000006 -0.071433312500000054 0
    -0.51534003125000005 -0.86604159999999997 -0.071433312500000054 0
    -0.55048285156249999 -0.861876525 -0.092258687500000047 0
    ...
    """

    n_vertices: int
    vertices: tuple[mesh_file_vertex, ...]
    label: str = "Vertices"


class mesh_file(NamedTuple):
    """A collection of mesh_file_hexahedra, mesh_file_vertices, and other
    meta data to compose a complete '.mesh' file.
    """

    vertices_block: mesh_file_vertices
    hexahedra_block: mesh_file_hexahedra
    header: str = "MeshVersionFormatted 1\n Dimension 3\n"
    footer: str = "End"


def io_inp_file_node(node: inp_file_node) -> str:
    """Given an item of 'inp_file_node' type, returns the equivalent string
    for serialization to an '.inp'_file.
    """
    items = (node.node_id, node.x, node.y, node.z)
    return ", ".join(map(str, items)) + "\n"


def io_mesh_file_hexahedron(input: str) -> mesh_file_hexahedron:
    """Given a string describing a hexahedron in '.mesh' format, e.g.,
    'n1 n2 n3 n4 n5 n6 n7 n8 vol_id', returns an item of 'mesh_file_hexahedron'
    type.
    """
    items = input.split()
    nodes = tuple(map(int, items[0:8]))
    vol = int(items[8])
    return mesh_file_hexahedron(nodes=nodes, vol_id=vol)


def io_mesh_file_hexahedron_to_inp_file_element(*, element_id: int, input: str) -> str:
    a = str(element_id) + ", "
    b = io_mesh_file_hexahedron(input)
    c = a + ", ".join(map(str, b.nodes)) + "\n"
    return c


def io_mesh_file_vertex(input: str) -> mesh_file_vertex:
    """Given a string describing a vertex in a '.mesh' format, e.g.,
    'x y z face_id', returns an item of 'mesh_file_vertex' type.
    """
    items = input.split()
    return mesh_file_vertex(
        x=float(items[0]),
        y=float(items[1]),
        z=float(items[2]),
        face_id=int(items[3]),
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


def translate_file(*, path_mesh_file: str) -> bool:
    """Given a string that contains a valid path and file name to
    a .mesh file, creates a .inp file in the same path location.
    Returns true if successful, false otherwise.
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

    with open(str(input_path_file), "rt") as in_stream:
        # line = in_stream.readline()

        with open(str(output_path_file), "wt") as out_stream:

            # out_stream.write(line)

            for line in in_stream:
                if "Vertices" in line:
                    n_vertices = int(in_stream.readline().strip())
                    out_stream.write(
                        "********************************** N O D E S **********************************\n"
                    )
                    out_stream.write("*NODE, NSET=ALLNODES\n")
                    for i in range(1, n_vertices + 1):
                        line = in_stream.readline()
                        out_line = io_mesh_file_vertex_to_inp_file_node(
                            node_id=i, input=line
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
                        out_line = io_mesh_file_hexahedron_to_inp_file_element(
                            element_id=i, input=line
                        )
                        out_stream.write(out_line)
                # else:
                # skip the current line and continue to the next line

    # If we reach this point, the input and output buffers are not closed
    # and the function was successful.
    success = True  # overwrite
    return success


def main(argv):

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "mesh_file",
        help="the .mesh file input",
    )

    args = parser.parse_args()
    mesh_file = args.mesh_file

    print(f"translator.py is translating {mesh_file}")
    translated = translate_file(path_mesh_file=mesh_file)
    success: Final[str] = "success: translation completed"
    failure: Final[str] = "error: translation unsucessful"
    print(success if translated else failure)


if __name__ == "__main__":
    """Runs the translator from the command line.
    Example:
    $ conda activate siblenv
    $ cd ~/sibl/geo/src/ptg
    $ python translate.py ../../data/mesh/hexa_2x2x2.mesh

    produces hexa_2x2x2.inp
    """
    main(sys.argv[1:])
