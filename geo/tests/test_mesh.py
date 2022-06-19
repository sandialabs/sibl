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
from pathlib import Path

import pytest

import ptg.mesh as mesh


def test_pairwise():
    x = "ABCD"
    y = (("A", "B"), ("B", "C"), ("C", "D"))
    fx = mesh.pairwise(x)
    fx2 = tuple(fx)
    assert y == fx2


def test_pairwise_circular():
    x = "ABCD"
    y = (("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"))
    fx = mesh.pairwise_circular(x)
    fx2 = tuple(fx)
    assert y == fx2


def test_adjacency():
    x = (3, 4, 1)
    # y = ((1, 3), (1, 4), (3, 4))
    y = ((3, 4), (1, 4), (1, 3))
    fx = mesh.adjacency_upper_diagonal(x)
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
    x = ((3, 4, 1), (3, 1, 2))  # right hand rule
    # y = ((1, 2), (1, 3), (1, 4), (2, 3), (3, 4))
    y = ((3, 4), (1, 4), (1, 3), (1, 2), (2, 3))
    fx = mesh.adjacencies_upper_diagonal(x)
    assert y == fx


def test_adjacencies_two_quads_nonsequential():
    """Given two quadrilaterals with non-sequential node numbers,
    test that the edge uppder diagonal adjacencies are returned.
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
    x = ((101, 2, 105, 4), (2, 103, 6, 105))  # right hand rule
    y = ((2, 101), (2, 105), (4, 105), (4, 101), (2, 103), (6, 103), (6, 105))
    fx = mesh.adjacencies_upper_diagonal(x)
    assert y == fx


def test_inp_path_file_to_stream_bad():
    """Given a file name or path that does not exist, checks that
    a FileNotFoundError is raised."""
    self_path_file = Path(__file__)
    self_path = self_path_file.resolve().parent
    data_path = self_path.joinpath("../", "data", "mesh").resolve()
    input_mesh_file = data_path.joinpath("this_file_does_not_exist.inp")

    with pytest.raises(FileNotFoundError) as error:
        mesh.inp_path_file_to_stream(pathfile=str(input_mesh_file))
    assert error.typename == "FileNotFoundError"


def test_inp_path_file_bad_nodes():
    """Given a file that does exist, verify the nodes cannot be read."""

    self_path_file = Path(__file__)
    self_path = self_path_file.resolve().parent
    data_path = self_path.joinpath("../", "data", "mesh").resolve()
    input_mesh_file = data_path.joinpath("four_quads_bad_nodes.inp")

    with pytest.raises(OSError) as error:
        mesh.inp_path_file_to_coordinates(pathfile=str(input_mesh_file))
    assert error.typename == "OSError"


def test_inp_path_file_bad_elements():
    """Given a file that does exist, verify the elements cannot be read."""

    self_path_file = Path(__file__)
    self_path = self_path_file.resolve().parent
    data_path = self_path.joinpath("../", "data", "mesh").resolve()
    input_mesh_file = data_path.joinpath("four_quads_bad_elements.inp")

    with pytest.raises(OSError) as error:
        mesh.inp_path_file_to_connectivities(pathfile=str(input_mesh_file))
    assert error.typename == "OSError"


def test_inp_path_file_to_coordinates_and_connectivity():
    """Given a valid Abaqus input file, tests that the expected coordinates
    and connectivities are returned."""
    self_path_file = Path(__file__)
    self_path = self_path_file.resolve().parent
    data_path = self_path.joinpath("../", "data", "mesh").resolve()
    input_mesh_file = data_path.joinpath("abaqus_nonseq_hex_2x2x2.inp")

    # test coordinates
    known = {
        "101": (0.0, 0.0, 0.0),
        "2": (0.5, 0.0, 0.0),
        "103": (1.0, 0.0, 0.0),
        "4": (0.0, 0.5, 0.0),
        "105": (0.5, 0.5, 0.0),
        "6": (1.0, 0.5, 0.0),
        "107": (0.0, 1.0, 0.0),
        "8": (0.5, 1.0, 0.0),
        "109": (1.0, 1.0, 0.0),
        "10": (0.0, 0.0, 0.5),
        "111": (0.5, 0.0, 0.5),
        "12": (1.0, 0.0, 0.5),
        "113": (0.0, 0.5, 0.5),
        "14": (0.5, 0.5, 0.5),
        "115": (1.0, 0.5, 0.5),
        "16": (0.0, 1.0, 0.5),
        "117": (0.5, 1.0, 0.5),
        "18": (1.0, 1.0, 0.5),
        "119": (0.0, 0.0, 1.0),
        "20": (0.5, 0.0, 1.0),
        "121": (1.0, 0.0, 1.0),
        "22": (0.0, 0.5, 1.0),
        "123": (0.5, 0.5, 1.0),
        "24": (1.0, 0.5, 1.0),
        "125": (0.0, 1.0, 1.0),
        "26": (0.5, 1.0, 1.0),
        "127": (1.0, 1.0, 1.0),
    }
    found = mesh.inp_path_file_to_coordinates(pathfile=str(input_mesh_file))
    assert known == found

    # test connectivity
    known = (
        (1, 101, 2, 105, 4, 10, 111, 14, 113),
        (20, 2, 103, 6, 105, 111, 12, 115, 14),
        (3, 4, 105, 8, 107, 113, 14, 117, 16),
        (40, 105, 6, 109, 8, 14, 115, 18, 117),
        (5, 10, 111, 14, 113, 119, 20, 123, 22),
        (60, 111, 12, 115, 14, 20, 121, 24, 123),
        (7, 113, 14, 117, 16, 22, 123, 26, 125),
        (80, 14, 115, 18, 117, 123, 24, 127, 26),
    )
    found = mesh.inp_path_file_to_connectivities(pathfile=str(input_mesh_file))
    assert known == found


def test_plot_mesh():
    """Given an examplar input file, cover the plotting functionality."""
    self_path_file = Path(__file__)
    self_path = self_path_file.resolve().parent
    data_path = self_path.joinpath("../", "data", "mesh").resolve()
    input_mesh_file = data_path.joinpath("four_quads_nonseq.inp")
    basename = Path(__file__).stem
    ext = ".png"
    output_path_file = self_path.parent.parent.joinpath(basename + ext)

    # assert, prior to test, that
    # (a) the input file exists and
    assert input_mesh_file.is_file()
    # (b) the output file does not exist
    assert not output_path_file.is_file()

    nodes = mesh.inp_path_file_to_coordinates(pathfile=str(input_mesh_file))

    elements = mesh.inp_path_file_to_connectivities(pathfile=str(input_mesh_file))

    elements_wo_element_number = tuple([x[1:] for x in elements])

    edges = mesh.adjacencies_upper_diagonal(xs=elements_wo_element_number)

    mesh_dict = {
        "title": "Test Mesh",
        "nodes_shown": True,
        "node_numbers_shown": True,
        "serialize": True,
        "basename": basename,
        "ext": ext,
    }
    plotted = mesh.plot_mesh(nodes=nodes, edges=edges, options=mesh_dict)

    # assert the plotting was successful
    assert plotted

    # assert the output file now does exist
    assert output_path_file.is_file()

    # clean up, delete the output file
    output_path_file.unlink()

    # confirm the output file no longer exists
    assert not output_path_file.is_file()
