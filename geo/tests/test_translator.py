"""This module is a unit test for the Translator implementation.

To run:
conda activate siblenv
cd ~/sibl
pytest geo/tests/test_translator.py -v

For a specific test (e.g., the first test):
pytest geo/tests/test_translator.py::test_io_inp_file_node

For coverage:
pytest geo/tests/test_translator.py -v --cov=geo/src/ptg --cov-report term-missing

For black style:
black --check geo/tests/test_translator.py --diff

For flake8:
flake8 --ignore E203,E501,W503 geo/tests/test_translator.py --statistics
"""
from pathlib import Path

import pytest

import ptg.translator as trans


def test_io_inp_file_node():
    """Given three items of inp_file_node type, tests they are converted
    to three equivalent strings, suitable for serialization.
    """
    xs = (
        trans.inp_file_node(node_id=1, x=-0.54, y=-0.86, z=-0.07),
        trans.inp_file_node(node_id=2, x=-0.51, y=-0.87, z=-0.08),
        trans.inp_file_node(node_id=3, x=-0.55, y=-0.88, z=-0.09),
    )
    ys = (
        "1, -0.54, -0.86, -0.07\n",
        "2, -0.51, -0.87, -0.08\n",
        "3, -0.55, -0.88, -0.09\n",
    )
    for x, y in zip(xs, ys):
        fx = trans.io_inp_file_node(x)
        assert y == fx


def test_io_mesh_file_hexahedron():
    """Given three strings, describing three hexahedra from a .mesh file,
    tests that three items of mesh_file_hexahedra type are returned.
    """
    xs = (
        "1 2 5 4 10 11 14 13 1\n",
        "2 3 6 5 11 12 15 14 1\n",
        "4 5 8 7 13 14 17 16 1\n",
    )
    ys = (
        trans.mesh_file_hexahedron(nodes=(1, 2, 5, 4, 10, 11, 14, 13), vol_id=1),
        trans.mesh_file_hexahedron(nodes=(2, 3, 6, 5, 11, 12, 15, 14), vol_id=1),
        trans.mesh_file_hexahedron(nodes=(4, 5, 8, 7, 13, 14, 17, 16), vol_id=1),
    )
    for (x, y) in zip(xs, ys):
        fx = trans.io_mesh_file_hexahedron(x)
        assert y == fx


def test_io_mesh_file_vertex():
    """Given three strings, describing three vertices from a .mesh file,
    returns three items of mesh_file_vertex type.
    """
    xs = (
        "-0.54 -0.86 -0.07 23\n",
        "-0.51 -0.87 -0.08 42\n",
        "-0.55 -0.88 -0.09 12\n",
    )
    ys = (
        trans.mesh_file_vertex(x=-0.54, y=-0.86, z=-0.07, face_id=23),
        trans.mesh_file_vertex(x=-0.51, y=-0.87, z=-0.08, face_id=42),
        trans.mesh_file_vertex(x=-0.55, y=-0.88, z=-0.09, face_id=12),
    )
    for (x, y) in zip(xs, ys):
        fx = trans.io_mesh_file_vertex(x)
        assert y == fx


def test_io_mesh_file_hexahedra_to_inp_file_element():
    """Given three strings, describing three hexahedra from a '.mesh' file,
    returns three strings in an '.inp' file format.
    """
    xs = (
        "1 2 5 4 10 11 14 13 1\n",
        "2 3 6 5 11 12 15 14 1\n",
        "4 5 8 7 13 14 17 16 1\n",
    )
    ys = (
        "1, 1, 2, 5, 4, 10, 11, 14, 13\n",
        "2, 2, 3, 6, 5, 11, 12, 15, 14\n",
        "3, 4, 5, 8, 7, 13, 14, 17, 16\n",
    )
    for i, (x, y) in enumerate(zip(xs, ys)):
        fx = trans.io_mesh_file_hexahedron_to_inp_file_element(
            element_id=i + 1, input=x
        )
        assert y == fx


def test_io_mesh_file_vertex_to_inp_file_node():
    """Given three strings, describing three vertices from a '.mesh' file,
    returns three strings in '.inp' file format.
    """
    xs = (
        "-0.54 -0.86 -0.07 23\n",
        "-0.51 -0.87 -0.08 42\n",
        "-0.55 -0.88 -0.09 12\n",
    )
    ys = (
        "1, -0.54, -0.86, -0.07\n",
        "2, -0.51, -0.87, -0.08\n",
        "3, -0.55, -0.88, -0.09\n",
    )
    for i, (x, y) in enumerate(zip(xs, ys)):
        fx = trans.io_mesh_file_vertex_to_inp_file_node(node_id=i + 1, input=x)
        assert y == fx


def test_cube_mesh_file_to_inp_file():
    """Given a small, exemplar .mesh file, the cube composed of two
    hex elements in each of the x, y, and z directions, confirm, a
    .inp file is properly created.
    """
    self_path_file = Path(__file__)
    self_path = self_path_file.resolve().parent
    data_path = self_path.joinpath("../", "data", "mesh").resolve()
    input_mesh_file = data_path.joinpath("hexahexa_2x2x2.mesh")
    trans.translate_file(path_mesh_file=str(input_mesh_file))


@pytest.mark.skip("work in progress")
def test_hex222_mesh_points_to_inp_points():
    """This test uses the hex222 mesh, which consists of a 3D cube with
    two hexahedral elements in the x, y, and z dimensions.

    given_points = [
        "0 0 0 5 \n",
        "0.5 0 0 2 \n",
        "1 0 0 3 \n",
        "0 0.5 0 5 \n",
        "0.5 0.5 0 1 \n",
        "1 0.5 0 3 \n",
        "0 1 0 5 \n",
        "0.5 1 0 4 \n",
        "1 1 0 4 \n",
        "0 0 0.5 5 \n",
        "0.5 0 0.5 2 \n",
        "1 0 0.5 3 \n",
        "0 0.5 0.5 5 \n",
        "0.5 0.5 0.5 0 \n",
        "1 0.5 0.5 3 \n",
        "0 1 0.5 5 \n",
        "0.5 1 0.5 4 \n",
        "1 1 0.5 4 \n",
        "0 0 1 6 \n",
        "0.5 0 1 6 \n",
        "1 0 1 6 \n",
        "0 0.5 1 6 \n",
        "0.5 0.5 1 6 \n",
        "1 0.5 1 6 \n",
        "0 1 1 6 \n",
        "0.5 1 1 6 \n",
        "1 1 1 6 \n",
    ]

    # hexahedral elements

    given_elements = [
        "1 2 5 4 10 11 14 13 1\n",
        "2 3 6 5 11 12 15 14 1\n",
        "4 5 8 7 13 14 17 16 1\n",
        "5 6 9 8 14 15 18 17 1\n",
        "10 11 14 13 19 20 23 22 1\n",
        "11 12 15 14 20 21 24 23 1\n",
        "13 14 17 16 22 23 26 25 1\n",
        "14 15 18 17 23 24 27 26 1\n",
    ]

    desired_points = [
        "1, 0.0, 0.0, 0.0\n",
        "2, 0.5, 0.0, 0.0\n",
        "3, 1.0, 0.0, 0.0\n",
        "4, 0.0, 0.5, 0.0\n",
        "5, 0.5, 0.5, 0.0\n",
        "6, 1.0, 0.5, 0.0\n",
        "7, 0.0, 1.0, 0.0\n",
        "8, 0.5, 1.0, 0.0\n",
        "9, 1.0, 1.0, 0.0\n",
        "10, 0.0, 0.0, 0.5\n",
        "11, 0.5, 0.0, 0.5\n",
        "12, 1.0, 0.0, 0.5\n",
        "13, 0.0, 0.5, 0.5\n",
        "14, 0.5, 0.5, 0.5\n",
        "15, 1.0, 0.5, 0.5\n",
        "16, 0.0, 1.0, 0.5\n",
        "17, 0.5, 1.0, 0.5\n",
        "18, 1.0, 1.0, 0.5\n",
        "19, 0.0, 0.0, 1.0\n",
        "20, 0.5, 0.0, 1.0\n",
        "21, 1.0, 0.0, 1.0\n",
        "22, 0.0, 0.5, 1.0\n",
        "23, 0.5, 0.5, 1.0\n",
        "24, 1.0, 0.5, 1.0\n",
        "25, 0.0, 1.0, 1.0\n",
        "26, 0.5, 1.0, 1.0\n",
        "27, 1.0, 1.0, 1.0\n",
    ]

    desired_elements = [
        "25, 1, 2, 5, 4, 10, 11, 14, 13\n",
        "26, 2, 3, 6, 5, 11, 12, 15, 14\n",
        "27, 4, 5, 8, 7, 13, 14, 17, 16\n",
        "28, 5, 6, 9, 8, 14, 15, 18, 17\n",
        "29, 10, 11, 14, 13, 19, 20, 23, 22\n",
        "30, 11, 12, 15, 14, 20, 21, 24, 23\n",
        "31, 13, 14, 17, 16, 22, 23, 26, 25\n",
        "32, 14, 15, 18, 17, 23, 24, 27, 26\n",
    ]
    """
