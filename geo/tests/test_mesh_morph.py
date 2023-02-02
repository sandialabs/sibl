"""This module is a unit test for the mesh smoothing implementation.

To run:
conda activate siblenv
cd ~/sibl
pytest geo/tests/test_mesh_morph.py -v

For a specific test (e.g., test_pairwise() function):
pytest geo/tests/test_mesh_morph.py::test_specific_function

For coverage:
pytest geo/tests/test_mesh_morph.py -v --cov=geo/src/ptg --cov-report term-missing

For black style:
black --check geo/tests/test_mesh_morph.py --diff

For flake8:
flake8 --ignore E203,E501,W503 geo/tests/test_mesh_morph.py --statistics
"""
import numpy as np

import ptg.mesh_morph as morph


def test_two_springs_one_dof():
    """Given two 1D springs connected at a single degree of freedom, assure
    the first two mesh updates are as expected.
    """
    nodes = {"1": (0.0,), "2": (1.5,), "3": (1.0,)}
    elements = ((1, 1, 2), (2, 2, 3))
    boundary = {"1": (1,), "3": (1,)}

    deltas_k1 = morph.smooth_neighbor_nonweighted(
        nodes=nodes, elements=elements, boundary=boundary, update_ratio=0.1
    )
    known_deltas_k1 = {"1": (0.0,), "2": (-0.1,), "3": (0.0,)}
    assert known_deltas_k1 == deltas_k1

    # Now perform a second iteration
    configuration_k1 = {}
    for key, value in nodes.items():
        configuration_k1[key] = np.array(nodes[key]) + np.array(deltas_k1[key])

    known_configuration_k1 = {"1": (0.0,), "2": (1.4,), "3": (1.0,)}
    # assert known_configuration_k1 == configuration_k1
    tol = 1.0e-10  # tolerance
    close_k1 = [
        a - b < tol
        for (a, b) in zip(known_configuration_k1.values(), configuration_k1.values())
    ]
    assert all(close_k1)

    deltas_k2 = morph.smooth_neighbor_nonweighted(
        nodes=configuration_k1, elements=elements, boundary=boundary, update_ratio=0.1
    )

    known_deltas_k2 = {"1": (0.0,), "2": (-0.09,), "3": (0.0,)}
    assert known_deltas_k2 == deltas_k2

    configuration_k2 = {}
    for key, value in configuration_k1.items():
        configuration_k2[key] = np.array(configuration_k1[key]) + np.array(
            deltas_k2[key]
        )

    known_configuration_k2 = {"1": (0.0,), "2": (1.31,), "3": (1.0,)}
    # assert known_configuration_k2 == configuration_k2
    close_k2 = [
        a - b < tol
        for (a, b) in zip(known_configuration_k2.values(), configuration_k2.values())
    ]
    assert all(close_k2)


def test_two_quads_two_dof():
    """Given two quadrilaterals with non-sequential node numbers and
    two degrees of freedom, test mesh smoothing for two iterations.
    This example is from:
    ~/sibl/geo/data/mesh/two_quads_nonseq.inp

     4       105       6
     *--------*--------*
     |        |        |
     |   (1)  |  (20)  |
     |        |        |
     *--------*--------*
    101       2       103

    """
    nodes = {
        "101": (1.0, 1.0),
        "2": (2.0, 1.0),
        "103": (3.0, 1.0),
        "4": (1.0, 2.0),
        "105": (2.0, 2.0),
        "6": (3.0, 2.0),
    }

    elements = ((1, 101, 2, 105, 4), (20, 2, 103, 6, 105))  # right hand rule

    boundary = {
        "101": (2,),
        "2": (1, 2),
        "103": (1,),
        "4": (1, 2),
        "6": (1, 2),
    }

    deltas = morph.smooth_neighbor_nonweighted(
        nodes=nodes, elements=elements, boundary=boundary, update_ratio=0.1
    )

    known_deltas = {
        "101": (0.05, 0.0),
        "2": (0.0, 0.0),
        "103": (0.0, 0.05),
        "4": (0.0, 0.0),
        "105": (0.0, -0.03333333333333335),
        "6": (0.0, 0.0),
    }

    assert known_deltas == deltas


def test_two_quads_two_dof_3D_representation():
    """Given two quadrilaterals with non-sequential node numbers and
    two degrees of freedom, test mesh smoothing for two iterations.
    Same as previous test, but now these are faces in 3D, instead of quads in 2D.
    This example is from:
    ~/sibl/geo/data/mesh/two_quads_nonseq.inp modified to 3D faces.

     4       105       6
     *--------*--------*
     |        |        |
     |   (1)  |  (20)  |
     |        |        |
     *--------*--------*
    101       2       103

    """
    nodes = {
        "101": (1.0, 1.0, 0.0),
        "2": (2.0, 1.0, 0.0),
        "103": (3.0, 1.0, 0.0),
        "4": (1.0, 2.0, 0.0),
        "105": (2.0, 2.0, 0.0),
        "6": (3.0, 2.0, 0.0),
    }

    elements = ((1, 101, 2, 105, 4), (20, 2, 103, 6, 105))  # right hand rule

    boundary = {
        "101": (2, 3),
        "2": (1, 2, 3),
        "103": (1, 3),
        "4": (1, 2, 3),
        "6": (1, 2, 3),
    }

    deltas = morph.smooth_neighbor_nonweighted(
        nodes=nodes, elements=elements, boundary=boundary, update_ratio=0.1
    )

    known_deltas = {
        "101": (0.05, 0.0, 0.0),
        "2": (0.0, 0.0, 0.0),
        "103": (0.0, 0.05, 0.0),
        "4": (0.0, 0.0, 0.0),
        "105": (0.0, -0.03333333333333335, 0.0),
        "6": (0.0, 0.0, 0.0),
    }

    assert known_deltas == deltas


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
