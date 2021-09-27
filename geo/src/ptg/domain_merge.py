"""The module merges two domains at a single boundary."""
# from typing import NamedTuple

import numpy as np

# from ptg.quadtree import Mesh
from ptg.quadtree import Domain, Mesh, Coordinate


def boundary_match(
    *,
    boundary0: tuple[tuple[int, ...], ...],
    coordinates0: tuple[Coordinate, ...],
    boundary1: tuple[tuple[int, ...], ...],
    coordinates1: tuple[Coordinate, ...],
    tolerance: float,
) -> tuple[tuple[int, ...], ...]:
    tol = tolerance  # typical is 1e-6

    n_seg0 = len(boundary0)  # number of boundary segments
    n_seg1 = len(boundary1)

    # number of points per boundary segment
    n_pts_per_seg0 = tuple(len(x) for x in boundary0)
    n_pts_per_seg1 = tuple(len(x) for x in boundary1)

    # x and y coordinates in boundary zero
    c0x = tuple([c.x for c in coordinates0])
    c0y = tuple([c.y for c in coordinates0])

    # x and y coordinates in boundary one
    c1x = tuple([c.x for c in coordinates1])
    c1y = tuple([c.y for c in coordinates1])

    matches = [[0 for j in range(0, n_seg1)] for i in range(0, n_seg0)]
    n_matches = 0

    for m, b0 in enumerate(boundary0):

        for n, b1 in enumerate(boundary1):

            if len(b0) == len(b1):

                (b0x, b0y) = (
                    np.array([c0x[k] for k in b0]),
                    np.array([c0y[k] for k in b0]),
                )
                (b1x, b1y) = (
                    np.array([c1x[k] for k in b1]),
                    np.array([c1y[k] for k in b1]),
                )

                (diffx, diffy) = (b0x - b1x, b0y - b1y)
                (normx, normy) = (
                    np.abs(np.linalg.norm(diffx)),
                    np.abs(np.linalg.norm(diffy)),
                )

                if normx < tol and normy < tol:
                    # b0 and b1 match
                    n_matches += 1
                    matches[m][n] = n_matches
                    break  # stop further evaluation of this loop

                # no match yet, so flip order of the second boundary
                b1_r = b1[::-1]

                (b1x_r, b1y_r) = (
                    np.array([c1x[k] for k in b1_r]),
                    np.array([c1y[k] for k in b1_r]),
                )

                (diffx_r, diffy_r) = (b0x - b1x_r, b0y - b1y_r)

                (normx_r, normy_r) = (
                    np.abs(np.linalg.norm(diffx_r)),
                    np.abs(np.linalg.norm(diffy_r)),
                )

                if normx_r < tol and normy_r < tol:
                    # b0 and b1_r match
                    n_matches += 1
                    # remove these matches from the unmatched buckets
                    matches[m][
                        n
                    ] = -n_matches  # negative number indicates order reversal
                    break  # stop further evaluation of this loop

    match_tuple = tuple(
        tuple(matches[i][j] for j in range(0, n_seg1)) for i in range(0, n_seg0)
    )

    return match_tuple


def boundary_substraction(
    *,
    boundary: tuple[tuple[int, ...], ...],
    subtracted: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    """From a boundary composed of tuples of node number segments, subtracts the subset
    of those segments contained in the subtracted tuple.

    Arguments:
        boundary (tuple[tuple[int, ...], ...]):  A tuple of tuples of ints, where each
            integer is a node number in sequence along a discrete boundary.
        subtracted (tuple[tuple[int, ...], ...]):  A subset of the boundary.

    Returns:
        tuple[tuple[int, ...], ...]: The difference of boundary less subtracted.
    """
    output = tuple(
        boundary_i for boundary_i in boundary if boundary_i not in subtracted
    )
    return output


def domain_merge(
    *,
    domain0: Domain,
    domain1: Domain,
    tolerance: float,
) -> Domain:
    """Merges two separate domains into a single domain.  Each domain has
    a tuple of boundaries.  Two domains may be merged only along a boundary sequence
    per domain.

    xxx (no longer enforced)
    xxx Once a matching pair of boundaries is found (one boundary from
    xxx `domain0` and one boundary from `domain1`), all other boundaries are disregarded.
    xxx This method does not merge domains among mutiple boundaries.

    Arguments:
        domain0 (Domain): The first domain, composed of a mesh and mergeable
            boundary(ies).
        domain1 (Domain): The second domain, composed of a mesh and mergeable
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
    # match = False  # start from no matching borders
    n_matches = 0  # start from zero matching border pairs
    n_unmatches = 0  # count of the number of unmatched border pairs

    # x and y coordinates in mesh zero
    c0x = tuple([c.x for c in domain0.mesh.coordinates])
    c0y = tuple([c.y for c in domain0.mesh.coordinates])

    # x and y coordinates in mesh one
    c1x = tuple([c.x for c in domain1.mesh.coordinates])
    c1y = tuple([c.y for c in domain1.mesh.coordinates])

    # sort all boundaries into matched and unmatched buckets
    b0_matched = tuple()
    b1_matched = tuple()
    b0_unmatched = domain0.boundaries
    b1_unmatched = domain1.boundaries

    # Compare boundaries from the two domains.
    # It is possible that no boundaries are joined.

    m = 0  # increment in b0 dimension

    b0 = b0_unmatched[m]

    match_in_n = False

    # while not match_in_n:
    for n in range(0, len(b1_unmatched)):  # increment in b1 dimension
        # given a segment b0, try to find a match across all b1 candidates
        b1 = b1_unmatched[n]

        (b0x, b0y) = (np.array([c0x[k] for k in b0]), np.array([c0y[k] for k in b0]))
        (b1x, b1y) = (np.array([c1x[k] for k in b1]), np.array([c1y[k] for k in b1]))

        (diffx, diffy) = (b0x - b1x, b0y - b1y)
        (normx, normy) = (np.abs(np.linalg.norm(diffx)), np.abs(np.linalg.norm(diffy)))

        if normx < tol and normy < tol:
            # b0 and b1 match
            match_in_n = True
            if n_matches == 0:
                b0_matched = (b0,)  # eliminate empty placeholder
                b1_matched = (b1,)  # eliminate empty placeholder
            else:
                b0_matched = b0_matched + (b0,)
                b1_matched = b1_matched + (b1,)
            n_matches += 1
            # remove these matches from the unmatched buckets
            b0_unmatched = boundary_substraction(
                boundary=b0_unmatched, subtracted=(b0,)
            )
            b1_unmatched = boundary_substraction(
                boundary=b1_unmatched, subtracted=(b1,)
            )
            break  # stop further evaluation of this loop

        # no match yet, so flip order of the second boundary
        b1_r = b1[::-1]

        (b1x_r, b1y_r) = (
            np.array([c1x[k] for k in b1_r]),
            np.array([c1y[k] for k in b1_r]),
        )

        (diffx_r, diffy_r) = (b0x - b1x_r, b0y - b1y_r)

        (normx_r, normy_r) = (
            np.abs(np.linalg.norm(diffx_r)),
            np.abs(np.linalg.norm(diffy_r)),
        )

        if normx_r < tol and normy_r < tol:
            # b0 and b1_r match
            match_in_n = True
            if n_matches == 0:
                b0_matched = (b0,)  # eliminate empty placeholder
                b1_matched = (b1_r,)  # eliminate empty placeholder
            else:
                b0_matched = b0_matched + (b0,)
                b1_matched = b1_matched + (b1_r,)  # retain original ordering
            n_matches += 1
            # remove these matches from the unmatched buckets
            b0_unmatched = boundary_substraction(
                boundary=b0_unmatched, subtracted=(b0,)
            )
            b1_unmatched = boundary_substraction(
                boundary=b1_unmatched, subtracted=(b1,)
            )  # retain original ordering of b1 to match with b1_unmatched original
            break  # stop further evaluation of this loop

    if not match_in_n:
        # a given segment b0 matched no b1 and no b1r
        if n_unmatches == 0:
            b0_unmatched = (b0,)
        else:
            b0_unmatched = b0_unmatched + (b0,)

    """ old method
    for b0 in domain0.boundaries:
        for b1 in domain1.boundaries:

            # x and y coordinates in a domain0.boundary
            b0x = np.array([c0x[k] for k in b0])
            b0y = np.array([c0y[k] for k in b0])

            # x and y coordinates in a domain1.boundary
            b1x = np.array([c1x[k] for k in b1])
            b1y = np.array([c1y[k] for k in b1])

            diffx = b0x - b1x
            diffy = b0y - b1y

            normx = np.abs(np.linalg.norm(diffx))
            normy = np.abs(np.linalg.norm(diffy))
            if normx < tol and normy < tol:
                if n_matches == 0:
                    b0_matched = (b0,)  # eliminate empty placeholder
                    b1_matched = (b1,)  # eliminate empty placeholder
                else:
                    b0_matched = b0_matched + (b0,)
                    b1_matched = b1_matched + (b1,)
                n_matches += 1
            else:
                # flip the ordering of the second boundary
                b1_reversed = b1[::-1]

                # reverse ordered x and y coordinates in domain1.boundary
                b1x_reversed = np.array([c1x[k] for k in b1_reversed])
                b1y_reversed = np.array([c1y[k] for k in b1_reversed])

                diffx_reversed = b0x - b1x_reversed
                diffy_reversed = b0y - b1y_reversed

                normx_reversed = np.abs(np.linalg.norm(diffx_reversed))
                normy_reversed = np.abs(np.linalg.norm(diffy_reversed))

                if normx_reversed < tol and normy_reversed < tol:
                    if n_matches == 0:
                        b0_matched = (b0,)  # eliminate empty placeholder
                        b1_matched = (b1_reversed,)  # eliminate empty placeholder
                    else:
                        b0_matched = b0_matched + (b0,)
                        b1_matched = b1_matched + (
                            b1_reversed,
                        )  # retain original ordering
                    n_matches += 1

                else:
                    # b1 boundary segment, forward and reversed, does
                    # not match b0 boundary segment, so collect both
                    # segments into the unmatched buckets
                    a = 4
                    if n_unmatches == 0:
                        b0_unmatched = (b0,)  # eliminate empty placeholder
                        b1_unmatched = (b1,)  # eliminate empty placeholder
                    else:
                        b0_unmatched = b0_unmatched + (b0,)
                        b1_unmatched = b1_unmatched + (b1,)  # retain original ordering
                    n_unmatches += 1
    """

    # number of nodal points
    nnp0 = len(domain0.mesh.coordinates)  # number of nodal points in mesh0
    nnp1 = len(domain1.mesh.coordinates)  # number of nodal points in mesh1

    # number of faces
    n_faces0 = len(domain0.mesh.connectivity)
    n_faces1 = len(domain1.mesh.connectivity)

    # number of nodes per element (=4 for quads)
    nen0 = len(domain0.mesh.connectivity[0])
    nen1 = len(domain1.mesh.connectivity[0])

    if nen0 != 4 or nen1 != 4:
        raise ValueError("Only 2D quadrilateral elements are allowed.")

    # number of boundaries on each domain
    n_bound0 = len(domain0.boundaries)  # number of boundaries on mesh0
    n_bound1 = len(domain1.boundaries)  # number of boundaries on mesh1

    # number of points per boundary
    n_pts_per_bound0 = tuple(len(x) for x in domain0.boundaries)
    n_pts_per_bound1 = tuple(len(x) for x in domain1.boundaries)

    # globally renumber faces
    faces0 = tuple(
        tuple(
            domain0.mesh.connectivity[i][j] + nnp0
            if domain0.mesh.connectivity[i][j] < 0
            else domain0.mesh.connectivity[i][j]
            for j in range(0, nen0)
        )
        for i in range(0, n_faces0)
    )
    faces1 = tuple(
        tuple(
            domain1.mesh.connectivity[i][j] + nnp1 + nnp0
            if domain1.mesh.connectivity[i][j] < 0
            else domain1.mesh.connectivity[i][j] + nnp0
            for j in range(0, nen1)
        )
        for i in range(0, n_faces1)
    )

    # globally renumber boundaries
    bounds0 = tuple(
        tuple(
            domain0.boundaries[i][j] + nnp0
            if domain0.boundaries[i][j] < 0
            else domain0.boundaries[i][j]
            for j in range(0, n_pts_per_bound0[i])
        )
        for i in range(0, n_bound0)
    )
    bounds1 = tuple(
        tuple(
            domain1.boundaries[i][j] + nnp1 + nnp0
            if domain1.boundaries[i][j] < 0
            else domain1.boundaries[i][j] + nnp0
            for j in range(0, n_pts_per_bound1[i])
        )
        for i in range(0, n_bound1)
    )

    vertices = domain0.mesh.coordinates + domain1.mesh.coordinates

    # if not match:
    if n_matches == 0:
        # just return the two domains, without merged boudaries, as a new

        # single domain

        faces = faces0 + faces1

        new_mesh = Mesh(coordinates=vertices, connectivity=faces)

        new_boundaries = bounds0 + bounds1

        new_domain = Domain(mesh=new_mesh, boundaries=new_boundaries)
        return new_domain

    else:

        # n_boundary_merged_points = len(b0_matched)
        # n_boundary_merged_points = tuple(len(x) for x in b0_matched)

        # tuple of segments in b0_matched, count number of merged points per segment
        # n_points_merged_per_seg = n_boundary_merged_points
        n_points_merged_per_seg = tuple(len(x) for x in b0_matched)

        # merge the matched boundaries along each segment
        # b0_merged = tuple(
        #     b0_matched[k] + nnp0 if b0_matched[k] < 0 else b0_matched[k]
        #     for k in range(0, len(b0_matched))
        # )

        # _matched is a collection of node numbers per segment in the input domain
        # _merged is the same collection with renumbered node numbers in the output domain

        b0_merged = tuple(
            tuple(seg[k] + nnp0 if seg[k] < 0 else seg[k] for k in range(len(seg)))
            for seg in b0_matched
        )
        # b1_merged = tuple(
        #     b1_matched[k] + nnp1 + nnp0 if b1_matched[k] < 0 else b1_matched[k] + nnp0
        #     for k in range(0, len(b1_matched))
        # )
        b1_merged = tuple(
            tuple(
                seg[k] + nnp0 + nnp1 if seg[k] < 0 else seg[k] + nnp0
                for k in range(0, len(seg))
            )
            for seg in b1_matched
        )

        # collect the non-merged boundaries from each domain
        b0_unmerged = boundary_substraction(boundary=bounds0, subtracted=b0_merged)
        b1_unmerged = boundary_substraction(boundary=bounds1, subtracted=b1_merged)

        # b0_unmerged = tuple(filter(lambda x: x != b0_merged, bounds0))
        # b1_unmerged = tuple(filter(lambda x: x != b1_merged, bounds1))

        # collect all unmerged boundaries as the new boundary of the new domain
        new_boundaries = b0_unmerged + b1_unmerged

        # renumber the new faces1
        for segment in range(0, len(n_points_merged_per_seg)):
            for point in range(0, n_points_merged_per_seg[segment]):
                faces1 = tuple(  # not faces1_merged, need to update face1 each k loop
                    tuple(
                        faces1[i][j]
                        if faces1[i][j] != b1_merged[segment][point]
                        else b0_merged[segment][point]
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
