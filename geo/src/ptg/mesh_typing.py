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
