"""The module merges two domains at a single boundary."""
from functools import reduce

import numpy as np

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
    a tuple of boundaries.  Two domains may be merged only along a boundary
    sequence per domain.

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

    # Compare boundaries from the two domains.
    # It is possible that no boundaries are joined.
    # mm is the so-called "match matrix"
    match_matrix = boundary_match(
        boundary0=domain0.boundaries,
        coordinates0=domain0.mesh.coordinates,
        boundary1=domain1.boundaries,
        coordinates1=domain1.mesh.coordinates,
        tolerance=tol,
    )

    n_matches = max(map(abs, reduce(lambda x, y: x + y, match_matrix)))

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

    # renumber faces to global numbering scheme
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

    # renumber boundaries to global numbering scheme
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

    if n_matches == 0:
        # just return the two domains, without merged boudaries,
        # as a new single domain

        faces = faces0 + faces1

        new_mesh = Mesh(coordinates=vertices, connectivity=faces)

        new_boundaries = bounds0 + bounds1

        new_domain = Domain(mesh=new_mesh, boundaries=new_boundaries)
        return new_domain

    else:

        # initialize a copy of unmerged boundaries
        bounds0_unmatched = bounds0
        bounds1_unmatched = bounds1

        for m, row in enumerate(match_matrix):
            for n, match_k in enumerate(row):
                if match_k != 0:
                    seg0 = bounds0[m]
                    if match_k > 0:
                        seg1 = bounds1[n]
                    elif match_k < 0:
                        seg1 = bounds1[n][::-1]  # reversed
                    # renumber the new faces1
                    for pt in range(0, len(seg1)):
                        faces1 = tuple(  # not faces1_merged, need to update face1 each k loop
                            tuple(
                                faces1[i][j] if faces1[i][j] != seg1[pt] else seg0[pt]
                                for j in range(0, nen1)
                            )
                            for i in range(0, n_faces1)
                        )
                    # remove merged boundaries
                    bounds0_unmatched = boundary_substraction(
                        boundary=bounds0_unmatched, subtracted=(bounds0[m],)
                    )
                    bounds1_unmatched = boundary_substraction(
                        boundary=bounds1_unmatched, subtracted=(bounds1[n],)
                    )

        new_boundaries = bounds0_unmatched + bounds1_unmatched

        faces = faces0 + faces1

        # new mesh retains so-called dangling nodes from donor mesh
        # as evidence of where they were prior to merge
        new_mesh = Mesh(coordinates=vertices, connectivity=faces)

        new_domain = Domain(mesh=new_mesh, boundaries=new_boundaries)
        return new_domain


def winding_number(
    *,
    x_center: float,
    y_center: float,
    xs_boundary: tuple[float, ...],
    ys_boundary: tuple[float, ...],
) -> int:
    """
    Computes the winding number.
    The boundary, composed of paired x and y cooredinates as `xs_boundary` and
    `ys_boundary` is assume to be closed.  Thus, the first and the last number for each
    of the x and y coordinates is repeated, thus x[0] = x[-1] and y[0] = y[-1],
    where x is `xs_boundary` and y is `ys_boundary`, respectively.

    Arguments:
        x_center (float): The x-coordinate of the observer, typically 0.0.
        y_center (float): The y-coordinate of the observer, typically 0.0.
        xs_boundary (tuple[float, ...]): A tuple sequential x-coordinates along the
            boundary path.
        ys_boundary (tuple[float, ...]): A tuple sequential y-coordinates along the
            boundary path.


    Returns:
        The integer winding number, defined here:
        https://en.wikipedia.org/wiki/Winding_number

    Raises:
        ValueError: If the two boundary arrays are not equal length.
        ValueError: If the boundary is not closed.
    """

    if len(xs_boundary) != len(ys_boundary):
        raise ValueError("x_boundary and y_boundary must be of equal length")

    if xs_boundary[0] != xs_boundary[-1]:
        raise ValueError("x_boundary is open; it must be closed")

    if ys_boundary[0] != ys_boundary[-1]:
        raise ValueError("y_boundary is open; it must be closed")

    x = [item - x_center for item in xs_boundary]
    y = [item - y_center for item in ys_boundary]

    # a=>a.map(([x,y])=>r+=Math.atan2(y*b-x*c,y*c+x*b,b=x,c=y),b=c=r=0)&&r/Math.PI/2
    # a=>a.map(([x,y])=>r+=Math.atan2(y*b-x*c, y*c+x*b, b=x, c=y), b=c=r=0) && r/math.pi/2

    return 0
