"""This module is a unit test for the Mesh implementation.

To run:
conda activate siblenv
cd ~/sibl
pytest geo/tests/test_mesh.py -v

For a specific test (e.g., test_pairwise() function):
pytest geo/tests/test_mesh.py::test_pairwise

For coverage:
pytest geo/tests/test_mesh.py -v --cov=geo/src/ptg --cov-report term-missing

For black style:
black --check geo/tests/test_mesh.py --diff

For flake8:
flake8 --ignore E203,E501,W503 geo/tests/test_mesh.py --statistics
"""
import ptg.mesh as pm


def test_pairwise():
    x = "ABCD"
    y = (("A", "B"), ("B", "C"), ("C", "D"))
    fx = pm.pairwise(x)
    fx2 = tuple(fx)
    assert y == fx2


def test_pairwise_circular():
    x = "ABCD"
    y = (("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"))
    fx = pm.pairwise_circular(x)
    fx2 = tuple(fx)
    assert y == fx2


def test_adjacency():
    x = (3, 4, 1)
    # y = ((1, 3), (1, 4), (3, 4))
    y = ((3, 4), (1, 4), (1, 3))
    fx = pm.adjacency_upper_diagonal(x)
    assert y == fx


def test_adjacencies():
    """Given a graph with four nodes and two closed triangular paths:
    2      1
    *------*
    | (2) /|
    |    / |
    |   /  |
    |  /   |
    | /    |
    |/ (1) |
    *------*
    3      4
    """
    x = ((3, 4, 1), (3, 1, 2))
    # y = ((1, 2), (1, 3), (1, 4), (2, 3), (3, 4))
    y = ((3, 4), (1, 4), (1, 3), (1, 2), (2, 3))
    fx = pm.adjacencies_upper_diagonal(x)
    assert y == fx
