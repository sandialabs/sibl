# Copyright 2020 National Technology and Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
# certain rights in this software.


"""This module provides smoothing operation on a mesh."""

from itertools import repeat

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

    # loop over all nodes in mesh
    for node_key, node_values in nodes.items():
        update = []
        connected_node_labels = tuple(
            y[0] if y[0] != int(node_key) else y[1]
            for y in tuple(filter(lambda x: int(node_key) in x, adj))
        )
        if node_key in boundary_keys:
            # node with at least one fixed dof
            # number of space dimensions at this node
            # node_nsd = len(nodes[node_key])
            node_nsd = len(node_values)
            # assume all ndof at node are active (non-fixed) as default
            dof_fixity = [item for item in repeat(False, node_nsd)]
            node_dof_fixed = boundary[node_key]
            # node_dof_fixed = tuple(boundary[node_key])
            # for i, fixed in enumerate(node_dof_fixed):
            # for i, fixed in enumerate(node_dof_fixed):
            # for fixed in range(node_dof_fixed[0], node_dof_fixed[-1] + 1):  # 0-index Python
            # if isinstance(node_dof_fixed, str) and node_dof_fixed.lower() == "encastre":
            #     node_dof_fixed = tuple([i + 1 for i in range(0, node_nsd)])  # 0-index Python
            # else:
            #     # cast as a tuple, guard against single dof being interpreted as an in
            #     node_dof_fixed = tuple([node_dof_fixed])
            for item in node_dof_fixed:
                # dof_index = int(item)  # satisfy type explicitly for linting in Python
                # dof_fixity[dof_index - 1] = True  # flip to be a fixed dof, 0-index Python
                dof_fixity[item - 1] = True  # flip to be a fixed dof, 0-index Python

            # for i, fixed in enumerate(node_dof_fixed):
            for i, fixed in enumerate(dof_fixity):
                if not fixed:
                    # dof is not fixed
                    # position of subject node
                    # p_subject = nodes[str(node_key)][i]
                    p_subject = node_values[i]
                    # positions for degree of freedom i for connected nodes qs
                    qs = [nodes[str(k)][i] for k in connected_node_labels]
                    num_connections = len(qs)
                    delta = (1.0 / num_connections) * sum(qs) - p_subject
                    delta = delta * update_ratio
                else:
                    # dof is fixed
                    delta = 0.0

                # for both fixed and not fixed, append
                update.append(delta)

            displacements[node_key] = tuple(update)
        else:
            # fully unconstrained node, all dof are active, no dof are fixed
            # p_subject = nodes[str(node_key)]
            p_subject = node_values
            np_p_subject = np.array(p_subject)
            qs = [nodes[str(k)] for k in connected_node_labels]
            num_connections = len(qs)
            np_qs = np.array(qs)
            sum_np_qs = sum(np_qs)
            deltas = (1.0 / num_connections) * sum_np_qs - np_p_subject
            deltas = deltas * update_ratio
            displacements[node_key] = tuple(deltas)

    return displacements
