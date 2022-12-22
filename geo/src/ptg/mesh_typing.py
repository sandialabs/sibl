# Copyright 2020 National Technology and Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
# certain rights in this software.


"""This module provides types fundamental to meshes."""

# Type alias for functional style methods
# https://docs.python.org/3/library/typing.html#type-aliases

Vertex = tuple[float, ...]
Vertices = tuple[Vertex, ...]

Edge = tuple[int, int]  # integer IDs of two vertices forming a single edge connection
Edges = tuple[Edge, ...]

Face = tuple[int, ...]  # integer IDs of n vertices forming a face in a CCW convention
Faces = tuple[Face, ...]

FixedDisplacements = dict[
    str, tuple[int, ...]
]  # string IDs of interger degrees of freedom <: (1, 2, 3)

# integer IDs, lower left hand node is the first, lower right hand is the second,
# upper right hand node is the third, upper left hand is the fourth
Quad = tuple[int, int, int, int]
QuadVertices = tuple[Vertex, Vertex, Vertex, Vertex]
