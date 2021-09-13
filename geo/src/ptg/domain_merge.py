"""The module merges two domains at a single boundary."""
from typing import NamedTuple

import numpy as np

from ptg.quadtree import Mesh


class Domain(NamedTuple):
    """Creates a Domain, which consists of a Mesh and a boundaries tuple.

    Mesh: see definition in the included Python module above.

    boundaries (tuple[tuple[int, ...], ...]):  Each tuple is a boundary. Each
        boundary is a tuple of integers that identify the node number in the mesh.
        The boundary integers should be sequential along the boundary.  There
        ordering of the boundary from first to last node or last to first node is
        immaterial, since the `domain_merge` function compares both forward and
        backward boundary sequences.
    """

    mesh: Mesh
    boundaries: tuple[tuple[int, ...], ...]


def domain_merge(
    *,
    d0: Domain,
    d1: Domain,
    tolerance: float,
) -> Domain:
    """Merges two separate domains into a single domain.  Each domain has
    a tuple of boundaries.  Two domains may be merged only along one boundary
    per domain.  Once a matching pair of boundaries is found (one boundary from
    `d0` and one boundary from `d1`), all other boundaries are disregarded.
    This method does not merge domains among mutiple boundaries.

    Arguments:
        d0 (Domain): The first domain, composed of a mesh and mergeable
            boundary(ies).
        d1 (Domain): The second domain, composed of a mesh and mergeable
            boundary(ies).
        tolerance (float): The maximum small distance magnitude that can
            exist separately in both the x and y directions between two
            separate nodes belonging to two separate meshes in a domain for
            the two points to be considered coincident and thus merged
            into a single point in returned domain.
            Typically set to 1e-6.

    Returns:
        (Domain): The domain merged from the first and second domains.
            If no points from the boundaries overlap (are within tolerance),
                then the returned single (non-joined) domain with global
                mesh coordinate numbering, connectivity, and domain boundaries.
            If points in the boundaries overlap (are within tolerance), then
                the nodes are merged and the two domains are joined at
                the overlapping nodes.

    Raises:
        ValueError: if meshes with elements that are not 2D quadrilaterals.
    """
    tol = tolerance  # typical is 1e-6
    match = False  # start from no matching borders

    # x and y coordinates in mesh zero
    c0x = tuple([c.x for c in d0.mesh.coordinates])
    c0y = tuple([c.y for c in d0.mesh.coordinates])

    # x and y coordinates in mesh one
    c1x = tuple([c.x for c in d1.mesh.coordinates])
    c1y = tuple([c.y for c in d1.mesh.coordinates])

    b0_matched = tuple()
    b1_matched = tuple()

    # Compare boundaries from the two domains, break out of comparison if/when a
    # boundary match is found.  Only a single boundary pair is ever joined.
    # It is also possible that no boundaries are joined.

    for b0 in d0.boundaries:
        for b1 in d1.boundaries:

            # only two boundaries of equal length can be a match
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

                # flip the ordering of the second boundary
                b1_reversed = b1[::-1]

                # reverse ordered x and y coordinates in d1.boundary
                b1x_reversed = np.array([c1x[k] for k in b1_reversed])
                b1y_reversed = np.array([c1y[k] for k in b1_reversed])

                diffx_reversed = b0x - b1x_reversed
                diffy_reversed = b0y - b1y_reversed

                normx_reversed = np.abs(np.linalg.norm(diffx_reversed))
                normy_reversed = np.abs(np.linalg.norm(diffy_reversed))
                if normx_reversed < tol and normy_reversed < tol:
                    b0_matched = b0
                    b1_matched = b1_reversed
                    match = True
                    break

            # else:
            # go on to the next boundary pairs

    # number of nodal points
    nnp0 = len(d0.mesh.coordinates)  # number of nodal points in mesh0
    nnp1 = len(d1.mesh.coordinates)  # number of nodal points in mesh1

    # number of faces
    n_faces0 = len(d0.mesh.connectivity)
    n_faces1 = len(d1.mesh.connectivity)

    # number of nodes per element (=4 for quads)
    nen0 = len(d0.mesh.connectivity[0])
    nen1 = len(d1.mesh.connectivity[0])

    if nen0 != 4 or nen1 != 4:
        raise ValueError("Only 2D quadrilateral elements are allowed.")

    # number of boundaries on each domain
    n_bound0 = len(d0.boundaries)  # number of boundaries on mesh0
    n_bound1 = len(d1.boundaries)  # number of boundaries on mesh1

    # number of points per boundary
    n_pts_per_bound0 = tuple(len(x) for x in d0.boundaries)
    n_pts_per_bound1 = tuple(len(x) for x in d1.boundaries)

    # globally renumber faces
    faces0 = tuple(
        tuple(
            d0.mesh.connectivity[i][j] + nnp0
            if d0.mesh.connectivity[i][j] < 0
            else d0.mesh.connectivity[i][j]
            for j in range(0, nen0)
        )
        for i in range(0, n_faces0)
    )
    faces1 = tuple(
        tuple(
            d1.mesh.connectivity[i][j] + nnp1 + nnp0
            if d1.mesh.connectivity[i][j] < 0
            else d1.mesh.connectivity[i][j] + nnp0
            for j in range(0, nen1)
        )
        for i in range(0, n_faces1)
    )

    # globally renumber boundaries
    bounds0 = tuple(
        tuple(
            d0.boundaries[i][j] + nnp0
            if d0.boundaries[i][j] < 0
            else d0.boundaries[i][j]
            for j in range(0, n_pts_per_bound0[i])
        )
        for i in range(0, n_bound0)
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

    if not match:
        # just return the two domains, without merged boudaries, as a new
        # single domain

        faces = faces0 + faces1

        new_mesh = Mesh(coordinates=vertices, connectivity=faces)

        new_boundaries = bounds0 + bounds1

        new_domain = Domain(mesh=new_mesh, boundaries=new_boundaries)
        return new_domain

    else:

        n_boundary_merged_points = len(b0_matched)

        # merge the matched boundaries
        b0_merged = tuple(
            b0_matched[k] + nnp0 if b0_matched[k] < 0 else b0_matched[k]
            for k in range(0, len(b0_matched))
        )
        b1_merged = tuple(
            b1_matched[k] + nnp1 + nnp0 if b1_matched[k] < 0 else b1_matched[k] + nnp0
            for k in range(0, len(b1_matched))
        )

        # collect the non-merged boundaries from each domain
        b0_unmerged = tuple(filter(lambda x: x != b0_merged, bounds0))
        b1_unmerged = tuple(filter(lambda x: x != b1_merged, bounds1))

        # collect all unmerged boundaries as the new boundary of the new domain
        new_boundaries = b0_unmerged + b1_unmerged

        # renumber the new faces1
        for k in range(0, n_boundary_merged_points):
            faces1 = tuple(  # not faces1_merged, need to update face1 each k loop
                tuple(
                    faces1[i][j] if faces1[i][j] != b1_merged[k] else b0_merged[k]
                    for j in range(0, nen1)
                )
                for i in range(0, n_faces1)
            )

        faces = faces0 + faces1

        # new mesh retains so-called dangling nodes from donor mesh
        # as evidence of where they were prior to merge
        new_mesh = Mesh(coordinates=vertices, connectivity=faces)

        new_domain = Domain(mesh=new_mesh, boundaries=new_boundaries)
        return new_domain
