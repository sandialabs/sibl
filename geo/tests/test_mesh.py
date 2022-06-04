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


def test_two_triangles():
    # vs = ((0.0, 0.0), (4.0, 0.0), (0.0, 4.0), (4.0, 4.0))  # vertices
    fs = ((1, 2, 3), (2, 4, 3))  # faces

    y = ((1, 2), (2, 3))
    fx = tuple(pm.pairwise(x=fs[0]))
    assert y == fx

    y = ((2, 4), (4, 3))
    fx = tuple(pm.pairwise(x=fs[1]))
    assert y == fx

    y = ((1, 2), (2, 3), (3, 1))
    fx = pm.pairwise_loop_first(x=fs[0])
    assert y == fx
    z = ((1, 2), (2, 3), (1, 3))
    fz = tuple(pm.upper_diagonal(x) for x in fx)
    assert z == fz

    y = ((2, 4), (4, 3), (3, 2))
    fx = pm.pairwise_loop_first(x=fs[1])
    assert y == fx
    z = ((2, 4), (3, 4), (2, 3))
    fz = tuple(pm.upper_diagonal(x) for x in fx)
    assert z == fz

    # fx = pm.adjacency_vector(faces=fs)

    # m = pm.Mesh(vertices=vs, faces=fs)
