"""This module is a unit test for the mesh smoothing implementation.

To run:
conda activate siblenv
cd ~/sibl
pytest geo/tests/test_mesh_smoothing.py -v

For a specific test (e.g., test_pairwise() function):
pytest geo/tests/test_mesh_smoothing.py::test_specific_function

For coverage:
pytest geo/tests/test_mesh_smoothing.py -v --cov=geo/src/ptg --cov-report term-missing

For black style:
black --check geo/tests/test_mesh_smoothing.py --diff

For flake8:
flake8 --ignore E203,E501,W503 geo/tests/test_mesh_smoothing.py --statistics
"""
import ptg.mesh_smoothing as pms


def test_two_quads_two_dof():
    """Given two quadrilaterals with non-squential node numbers and
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

    boundary_nodes = {
        "101": (False, True),
        "2": (True, True),
        "103": (True, False),
        "4": (True, True),
        "6": (True, True),
    }

    deltas = pms.smooth_neighbor_nonweighted(
        nodes=nodes, elements=elements, boundary_nodes=boundary_nodes, update_ratio=0.1
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
