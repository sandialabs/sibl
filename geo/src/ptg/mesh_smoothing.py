"""This module provides smoothing operation on a mesh."""

import numpy as np

from ptg.mesh import adjacencies_upper_diagonal


def smooth_neighbor_nonweighted(*, nodes, elements, boundary, update_ratio):
    """Given nonsequential nodes, elements, boundary elements
    containing homogenous displacements in [1 .. n_space_dimensions],
    and update_ratio between (0, 1), returns the nodes in updated positions.
    """
    assert update_ratio > 0.0 and update_ratio < 1.0

    displacements = dict()  # empty prior to update

    boundary_keys = boundary.keys()

    elements_wo_element_number = tuple([x[1:] for x in elements])
    adj = adjacencies_upper_diagonal(xs=elements_wo_element_number)

    for key, value in nodes.items():
        update = []
        connected_node_labels = tuple(
            y[0] if y[0] != int(key) else y[1]
            for y in tuple(filter(lambda x: int(key) in x, adj))
        )
        if key in boundary_keys:
            node_dof_fixed = boundary[key]
            for i, fixed in enumerate(node_dof_fixed):
                if not fixed:
                    # position of subject node
                    p_subject = nodes[str(key)][i]
                    # positions for degree of freedom i for connected nodes qs
                    qs = [nodes[str(k)][i] for k in connected_node_labels]
                    num_connections = len(qs)
                    delta = (1.0 / num_connections) * sum(qs) - p_subject
                    delta = delta * update_ratio
                else:
                    delta = 0.0

                update.append(delta)

            displacements[key] = tuple(update)
        else:
            # fully unconstrained node
            p_subject = nodes[str(key)]
            np_p_subject = np.array(p_subject)
            qs = [nodes[str(k)] for k in connected_node_labels]
            num_connections = len(qs)
            np_qs = np.array(qs)
            sum_np_qs = sum(np_qs)
            deltas = (1.0 / num_connections) * sum_np_qs - np_p_subject
            deltas = deltas * update_ratio
            displacements[key] = tuple(deltas)

    return displacements
