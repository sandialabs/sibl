"""The module merges two mesh."""
from typing import NamedTuple

import numpy as np

from ptg.quadtree import Mesh


class Domain(NamedTuple):
    """Creates a mesh, which consists of a tuple of coordinates and
    a tuple of connectivity.

    Notation connection with Finite Element Method (FEM), cf., TJR Hughes
        nnp = number of nodal points = len(coordinates)
        nel = number of elements = len(connectivity)
    """

    mesh: Mesh
    boundaries: tuple[tuple[int, ...], ...]


def domain_merge(
    *,
    d0: Domain,
    d1: Domain,
    tolerance: float,
) -> Domain:
    """Merges two domains into a merged domain.

    Arguments:
        d0 (Domain): The first domain, composed of a mesh and mergeable
            boundary.
        d1 (Domain): The second domain, composed of a mesh and mergeable
            boundary.
        tolerance (float): The maximum small distance magnitude that can
            exist in both the x and y directions betwee two separate points
            belonging to two separate meshes for the two points to be
            considered coincident and thus merged into a single point in
            returned domain.

    Returns:
        (Domain): The domain merged from the first and second domains.
            If no points from the meshes overlap (are within tolerance),
                then the returned single mesh contains two floating
                but non-joined meshes with global coordinate numbering
                and connectivity.
            If points in the mesh overlap (are within tolerance), then
                the nodes are merged and the two meshes are joined at
                the overlapping nodes.
    """
    # tol = 1e-6  # tolerance
    tol = tolerance
    match = False  # start from no matching borders

    # x and y coordinates in mesh zero
    c0x = tuple([c.x for c in d0.mesh.coordinates])
    c0y = tuple([c.y for c in d0.mesh.coordinates])

    # x and y coordinates in mesh one
    c1x = tuple([c.x for c in d1.mesh.coordinates])
    c1y = tuple([c.y for c in d1.mesh.coordinates])

    for b0 in d0.boundaries:
        for b1 in d1.boundaries:

            if len(b0) == len(b1):

                # x and y coordinates in a d0.boundary
                b0x = np.array([c0x[k] for k in b0])
                b0y = np.array([c0y[k] for k in b0])

                # x and y coordinates in a d1.boundary
                b1x = np.array([c1x[k] for k in b1])
                b1y = np.array([c1y[k] for k in b1])

                diffx = b0x - b1x
                diffy = b0y - b1y

                normx = np.abs(np.linalg.norm(diffx))
                normy = np.abs(np.linalg.norm(diffy))
                if normx < tol and normy < tol:
                    b0_matched = b0
                    b1_matched = b1
                    match = True
                    break

                b1_reversed = b1[::-1]

                # reverse ordered x and y coordinates in d1.boundary
                b1x_r = np.array([c1x[k] for k in b1_reversed])
                b1y_r = np.array([c1y[k] for k in b1_reversed])

                diffx_r = b0x - b1x_r
                diffy_r = b0y - b1y_r

                normx_r = np.abs(np.linalg.norm(diffx_r))
                normy_r = np.abs(np.linalg.norm(diffy_r))
                if normx_r < tol and normy_r < tol:
                    b0_matched = b0
                    b1_matched = b1_reversed
                    match = True
                    break

            else:
                # do nothing, get the next boundary
                aa = 4

    if not match:
        # just return the two meshes, without merged boudaries, as a new
        # single mesh

        # mesh0
        nnp0 = len(d0.mesh.coordinates)  # number of nodal points in mesh0
        n_faces0 = len(d0.mesh.connectivity)
        n_en0 = len(d0.mesh.connectivity[0])  # number of element nodes, (=4 for quads)
        n_bound0 = len(d0.boundaries)  # number of boundaries on mesh0
        n_pts_per_bound0 = tuple(len(x) for x in d0.boundaries)

        faces0 = tuple(
            tuple(
                d0.mesh.connectivity[i][j] + nnp0
                if d0.mesh.connectivity[i][j] < 0
                else d0.mesh.connectivity[i][j]
                for j in range(0, n_en0)
            )
            for i in range(0, n_faces0)
        )

        bounds0 = tuple(
            tuple(
                d0.boundaries[i][j] + nnp0
                if d0.boundaries[i][j] < 0
                else d0.boundaries[i][j]
                for j in range(0, n_pts_per_bound0[i])
            )
            for i in range(0, n_bound0)
        )

        # mesh1
        nnp1 = len(d1.mesh.coordinates)  # number of nodal points in mesh1
        n_faces1 = len(d1.mesh.connectivity)
        n_en1 = len(d1.mesh.connectivity[0])  # number of element nodes, (=4 for quads)
        n_bound1 = len(d1.boundaries)  # number of boundaries on mesh1
        n_pts_per_bound1 = tuple(len(x) for x in d1.boundaries)

        faces1 = tuple(
            tuple(
                d1.mesh.connectivity[i][j] + nnp1 + nnp0
                if d1.mesh.connectivity[i][j] < 0
                else d1.mesh.connectivity[i][j] + nnp0
                for j in range(0, n_en1)
            )
            for i in range(0, n_faces1)
        )

        bounds1 = tuple(
            tuple(
                d1.boundaries[i][j] + nnp1 + nnp0
                if d1.boundaries[i][j] < 0
                else d1.boundaries[i][j] + nnp0
                for j in range(0, n_pts_per_bound1[i])
            )
            for i in range(0, n_bound1)
        )

        vertices = d0.mesh.coordinates + d1.mesh.coordinates

        faces = faces0 + faces1

        new_mesh = Mesh(coordinates=vertices, connectivity=faces)

        new_boundaries = bounds0 + bounds1

        new_domain = Domain(mesh=new_mesh, boundaries=new_boundaries)
        return new_domain

    # else:
    #     pass
    # b0_unmatched = tuple(filter(lambda x: x != b0_matched, d0.boundaries))
    # b1_unmatched = tuple(filter(lambda x: x != b1_matched, d1.boundaries))

    # # the boundaries of the new resultant mesh
    # boundaries_unmatched = b0_unmatched + b1_unmatched
