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
import ptg.mesh_morph as morph


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
