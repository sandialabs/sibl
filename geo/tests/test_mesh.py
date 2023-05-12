"""This module is a unit test for the Mesh implementation.

To run:
# conda activate siblenv
cd ~/sibl
source .venv/bin/activate.fish  # activate the virtual environment
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
from math import isinf, isnan
from pathlib import Path

import numpy as np
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
    """Given a file that does exist, verify that bad nodes cannot be read."""

    self_path_file = Path(__file__)
    self_path = self_path_file.resolve().parent
    data_path = self_path.joinpath("../", "data", "mesh").resolve()
    input_mesh_file = data_path.joinpath("four_quads_bad_nodes.inp")

    with pytest.raises(OSError) as error:
        mesh.inp_path_file_to_coordinates(pathfile=str(input_mesh_file))
    assert error.typename == "OSError"


def test_inp_path_file_bad_elements():
    """Given a file that does exist, verify that bad elements cannot be read."""

    self_path_file = Path(__file__)
    self_path = self_path_file.resolve().parent
    data_path = self_path.joinpath("../", "data", "mesh").resolve()
    input_mesh_file = data_path.joinpath("four_quads_bad_elements.inp")

    with pytest.raises(OSError) as error:
        mesh.inp_path_file_to_connectivities(pathfile=str(input_mesh_file))
    assert error.typename == "OSError"


def test_inp_path_file_bad_boundary():
    """Given a file that does exist, verify that a bad boundary cannot be read."""

    self_path_file = Path(__file__)
    self_path = self_path_file.resolve().parent
    data_path = self_path.joinpath("../", "data", "mesh").resolve()
    input_mesh_file = data_path.joinpath("four_quads_bad_boundary.inp")

    with pytest.raises(OSError) as error:
        mesh.inp_path_file_to_boundary(pathfile=str(input_mesh_file))
    assert error.typename == "OSError"


def test_inp_path_file_four_quads():
    """Given the canonical example, four_quad_nonseq.inp, verify
    The nodes, elements, and boundary are correctly read.
    """
    self_path_file = Path(__file__)
    self_path = self_path_file.resolve().parent
    data_path = self_path.joinpath("../", "data", "mesh").resolve()
    input_mesh_file = data_path.joinpath("four_quads_nonseq.inp")

    # test coordinates
    known_coordinates = {
        "101": (1.0, 1.0),
        "2": (2.5, 1.0),
        "103": (3.0, 1.0),
        "4": (1.0, 2.5),
        "105": (2.5, 2.5),
        "6": (3.0, 2.5),
        "13": (1.0, 3.0),
        "23": (2.5, 3.0),
        "33": (3.0, 3.0),
    }

    found = mesh.inp_path_file_to_coordinates(pathfile=str(input_mesh_file))
    assert known_coordinates == found

    # test elements
    known = (
        (1, 101, 2, 105, 4),
        (20, 2, 103, 6, 105),
        (31, 105, 6, 33, 23),
        (44, 4, 105, 23, 13),
    )
    found = mesh.inp_path_file_to_connectivities(pathfile=str(input_mesh_file))
    assert known == found

    elements_wo_element_number = tuple([x[1:] for x in known])
    known = (
        ((1.0, 1.0), (2.5, 1.0), (2.5, 2.5), (1.0, 2.5)),
        ((2.5, 1.0), (3.0, 1.0), (3.0, 2.5), (2.5, 2.5)),
        ((2.5, 2.5), (3.0, 2.5), (3.0, 3.0), (2.5, 3.0)),
        ((1.0, 2.5), (2.5, 2.5), (2.5, 3.0), (1.0, 3.0)),
    )
    found = mesh.faces_as_nodes_to_faces_as_vertices(
        faces=elements_wo_element_number, coordinates=known_coordinates
    )
    assert known == found

    # test boundary
    known = {
        "101": (1, 2),
        "2": (2,),
        "103": (1, 2),
        "4": (1,),
        "6": (1,),
        "13": (1, 2),
        "23": (2,),
        "33": (1, 2),
    }

    found = mesh.inp_path_file_to_boundary(pathfile=str(input_mesh_file))
    assert known == found


def test_inp_path_file_to_coordinates_connectivity():
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


def test_tri_edge_lengths():
    """Given a trianguarl element in \real_{\nsd},
    verifies the lengths of the three edges that are returned.
    """

    # 1D case
    cs = (
        (1.0,),
        (2.0,),
        (4.0,),
    )
    ls = mesh.perimeter_segment_lengths(coordinates=cs)
    assert ls == (1.0, 2.0, 3.0)

    # 2D case with 3, 4, 5, triangle
    cs = ((0.0, 0.0), (3.0, 0.0), (3.0, 4.0))
    ls = mesh.perimeter_segment_lengths(coordinates=cs)
    assert ls == (3.0, 4.0, 5.0)

    # 3D case
    cs = ((-1.0, 2.0, 3.0), (4.0, 5.0, 6.0), (7.0, 8.0, 9.0))
    ls = mesh.perimeter_segment_lengths(coordinates=cs)
    knowns = (6.557438524302, 5.196152422706632, 11.661903789690601)

    assert knowns == pytest.approx(ls)


def test_quad_edge_lengths():
    """Given a quadrilateral element in \real_{\nsd},
    verifies the length of the four edges that are returned.
    """
    # Test 2D quad that matches the parameteric space.
    cs = ((-1.0, -1.0), (1.0, -1.0), (1.0, 1.0), (-1.0, 1.0))
    ls = mesh.perimeter_segment_lengths(coordinates=cs)
    assert ls == (2.0, 2.0, 2.0, 2.0)

    # Test 3D quad that matches the parameteric space.
    cs = ((-1.0, -1.0, 0.0), (1.0, -1.0, 0.0), (1.0, 1.0, 0.0), (-1.0, 1.0, 0.0))
    ls = mesh.perimeter_segment_lengths(coordinates=cs)
    assert ls == (2.0, 2.0, 2.0, 2.0)


def test_quad_undeformed():
    """Given a quadrilateral in 2D, verify the
    Jacobian matrix, evaluated at each of the four quad corners, quad is a simple
    undeformed quad.  Verifies mimimum scaled Jacobian, skew, and aspect ratio.
    """
    # Reference: Memphis_edu_C_03c_slides-quads.pdf

    cs = ((1.0, 1.0), (2.0, 1.0), (2.0, 2.0), (1.0, 2.0))

    n = mesh.quad_node_1()
    assert mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == (
        (0.5, 0.0),
        (0.0, 0.5),
    )
    assert mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == 0.25

    n = mesh.quad_node_2()  # overwrite
    assert mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == (
        (0.5, 0.0),
        (0.0, 0.5),
    )
    assert mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == 0.25

    n = mesh.quad_node_3()  # overwrite
    assert mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == (
        (0.5, 0.0),
        (0.0, 0.5),
    )
    assert mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == 0.25

    n = mesh.quad_node_4()  # overwrite
    assert mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == (
        (0.5, 0.0),
        (0.0, 0.5),
    )
    assert mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == 0.25
    assert mesh.det_jacobian_of_quad_check(xi=n.a, eta=n.b, vertices=cs) == 0.25

    assert mesh.minimum_jacobian_of_quad(vertices=cs) == 1.0

    ls = mesh.perimeter_segment_lengths(coordinates=cs)
    assert ls == (1.0, 1.0, 1.0, 1.0)

    assert mesh.minimum_scaled_jacobian_of_quad(vertices=cs) == 1.0

    # test principal axes
    a, b = mesh.principal_axes_of_quad(vertices=cs)
    assert a == (2.0, 0.0)
    assert b == (0.0, 2.0)

    # test skew
    skew = mesh.skew_of_quad(vertices=cs)
    assert skew == 0.0

    # test aspect ratio
    ar = mesh.aspect_ratio_of_quad(vertices=cs)
    assert ar == 1.0


def test_quad_shear():
    """Given a quadrilateral in 2D, verify the
    Jacobian matrix, evaluated at each of the four quad corners in simple shear.
    Verifies mimimum scaled Jacobian, skew, and aspect ratio.
    """
    cs = ((1.0, 1.0), (2.0, 1.0), (3.0, 2.0), (2.0, 2.0))

    n = mesh.quad_node_1()
    assert mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == (
        (0.5, 0.0),
        (0.5, 0.5),
    )
    assert mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == 0.25

    n = mesh.quad_node_2()  # overwrite
    assert mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == (
        (0.5, 0.0),
        (0.5, 0.5),
    )
    assert mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == 0.25

    n = mesh.quad_node_3()  # overwrite
    assert mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == (
        (0.5, 0.0),
        (0.5, 0.5),
    )
    assert mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == 0.25

    n = mesh.quad_node_4()  # overwrite
    assert mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == (
        (0.5, 0.0),
        (0.5, 0.5),
    )
    assert mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == 0.25
    assert mesh.det_jacobian_of_quad_check(xi=n.a, eta=n.b, vertices=cs) == 0.25

    assert mesh.minimum_jacobian_of_quad(vertices=cs) == 1.0

    ls = mesh.perimeter_segment_lengths(coordinates=cs)
    assert ls == pytest.approx((1.0, 1.4142135623730951, 1.0, 1.4142135623730951))

    assert mesh.minimum_scaled_jacobian_of_quad(vertices=cs) == pytest.approx(
        0.7071067811865476
    )

    # test principal axes
    a, b = mesh.principal_axes_of_quad(vertices=cs)
    assert a == (2.0, 0.0)
    assert b == (2.0, 2.0)

    # test skew
    skew = mesh.skew_of_quad(vertices=cs)
    assert skew == pytest.approx(np.sqrt(2.0) / 2.0)  # sqrt(2)/2

    # test aspect ratio
    ar = mesh.aspect_ratio_of_quad(vertices=cs)
    assert ar == pytest.approx(np.sqrt(2.0))  # sqrt(2)


def test_quad_trapezoid():
    """Given a quadrilateral in 2D, verify the
    Jacobian matrix, evaluated at each of the four quad corners as a trapezoid.
    Verifies mimimum scaled Jacobian, skew, and aspect ratio.
    """
    cs = ((1.0, 1.0), (2.5, 1.0), (2.0, 2.0), (1.5, 2.0))

    n = mesh.quad_node_1()
    assert mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == (
        (0.75, 0.0),
        (0.25, 0.5),
    )
    assert mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == 0.375

    n = mesh.quad_node_2()  # overwrite
    assert mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == (
        (0.75, 0.0),
        (-0.25, 0.5),
    )
    assert mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == 0.375

    n = mesh.quad_node_3()  # overwrite
    assert mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == (
        (0.25, 0.0),
        (-0.25, 0.5),
    )
    assert (
        pytest.approx(mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)) == 0.125
    )

    n = mesh.quad_node_4()  # overwrite
    assert mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == (
        (0.25, 0.0),
        (0.25, 0.5),
    )
    assert (
        pytest.approx(mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)) == 0.125
    )
    assert (
        pytest.approx(mesh.det_jacobian_of_quad_check(xi=n.a, eta=n.b, vertices=cs))
        == 0.125
    )

    assert mesh.minimum_jacobian_of_quad(vertices=cs) == 0.5

    ls = mesh.perimeter_segment_lengths(coordinates=cs)
    assert ls == (1.5, 1.118033988749895, 0.5, 1.118033988749895)

    assert mesh.minimum_scaled_jacobian_of_quad(vertices=cs) == pytest.approx(
        0.8944271909999159
    )

    # test principal axes
    a, b = mesh.principal_axes_of_quad(vertices=cs)
    assert a == (2.0, 0.0)
    assert b == (0.0, 2.0)

    # test skew
    skew = mesh.skew_of_quad(vertices=cs)
    assert skew == 0.0

    # test aspect ratio
    ar = mesh.aspect_ratio_of_quad(vertices=cs)
    assert ar == 1.0


def test_quad_extended():
    """Given a quadrilateral in 2D, verify the
    Jacobian matrix, evaluated at each of the four quad corners, quad has node 3 extended.
    Verifies mimimum scaled Jacobian, skew, and aspect ratio.
    """
    cs = ((1.0, 1.0), (2.0, 1.0), (2.5, 2.5), (1.0, 2.0))
    # The det(J) = 1/16 * (6 + a + b)

    n = mesh.quad_node_1()
    assert mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == (
        (0.5, 0.0),
        (0.0, 0.5),
    )
    assert mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == 0.25

    n = mesh.quad_node_2()  # overwrite
    assert mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == (
        (0.5, 0.0),
        (0.25, 0.75),
    )
    assert mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == 0.375

    n = mesh.quad_node_3()  # overwrite
    assert mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == (
        (0.75, 0.25),
        (0.25, 0.75),
    )
    assert pytest.approx(mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)) == 0.5

    n = mesh.quad_node_4()  # overwrite
    assert mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == (
        (0.75, 0.25),
        (0.0, 0.5),
    )
    assert (
        pytest.approx(mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)) == 0.375
    )
    assert (
        pytest.approx(mesh.det_jacobian_of_quad_check(xi=n.a, eta=n.b, vertices=cs))
        == 0.375
    )

    assert mesh.minimum_jacobian_of_quad(vertices=cs) == 1.0

    ls = mesh.perimeter_segment_lengths(coordinates=cs)
    assert ls == pytest.approx((1.0, 1.5811388300841898, 1.5811388300841898, 1.0))

    assert mesh.minimum_scaled_jacobian_of_quad(vertices=cs) == pytest.approx(0.800)

    # test principal axes
    a, b = mesh.principal_axes_of_quad(vertices=cs)
    assert a == (2.5, 0.5)
    assert b == (0.5, 2.5)

    # test skew
    skew = mesh.skew_of_quad(vertices=cs)
    assert skew == pytest.approx(0.3846153846153847)

    # test aspect ratio
    ar = mesh.aspect_ratio_of_quad(vertices=cs)
    assert ar == 1.0


def test_quad_tri_positive():
    """Given a quadrilateral in 2D, verify the
    Jacobian matrix, evaluated at each of the four quad corners, quad has node 3 pushed inward.
    Verifies mimimum scaled Jacobian, skew, and aspect ratio.
    """
    cs = ((1.0, 1.0), (2.0, 1.0), (1.6, 1.6), (1.0, 2.0))
    # The det(J) = 1/20 * (3 - a - b)

    n = mesh.quad_node_1()
    assert mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == (
        (0.5, 0.0),
        (0.0, 0.5),
    )
    assert mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == 0.25

    n = mesh.quad_node_2()  # overwrite
    known = ((0.5, 0.0), (-0.2, 0.3))
    found = mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)
    assert all(k == pytest.approx(f) for (k, f) in zip(known, found))
    assert mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == 0.15

    n = mesh.quad_node_3()  # overwrite
    known = ((0.3, -0.2), (-0.2, 0.3))
    found = mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)
    assert all(k == pytest.approx(f) for (k, f) in zip(known, found))
    assert (
        pytest.approx(mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)) == 0.05
    )

    n = mesh.quad_node_4()  # overwrite
    known = ((0.3, -0.2), (0.0, 0.5))
    found = mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)
    assert all(k == pytest.approx(f) for (k, f) in zip(known, found))

    assert (
        pytest.approx(mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)) == 0.15
    )
    assert (
        pytest.approx(mesh.det_jacobian_of_quad_check(xi=n.a, eta=n.b, vertices=cs))
        == 0.15
    )

    assert mesh.minimum_jacobian_of_quad(vertices=cs) == pytest.approx(0.2)

    ls = mesh.perimeter_segment_lengths(coordinates=cs)
    assert ls == pytest.approx((1.0, 0.7211102550927979, 0.7211102550927979, 1.0))

    assert mesh.minimum_scaled_jacobian_of_quad(vertices=cs) == pytest.approx(
        0.38461538461538486
    )

    # test principal axes
    a, b = mesh.principal_axes_of_quad(vertices=cs)
    assert a == pytest.approx((1.6, -0.4))
    assert b == pytest.approx((-0.4, 1.6))

    # test skew
    skew = mesh.skew_of_quad(vertices=cs)
    assert skew == pytest.approx(0.4705882352941174)

    # test aspect ratio
    ar = mesh.aspect_ratio_of_quad(vertices=cs)
    assert ar == 1.0


def test_quad_tri_negative():
    """Given a quadrilateral in 2D, verify the
    Jacobian matrix, evaluated at each of the four quad corners, quad has node 3 pushed inward
    to create a slight negative value in the Jacobian map.
    Verifies mimimum scaled Jacobian, skew, and aspect ratio.
    """
    cs = ((1.0, 1.0), (2.0, 1.0), (1.4, 1.4), (1.0, 2.0))
    # The det(J) = 1/40 * (4 - 3a - 3b)

    n = mesh.quad_node_1()
    assert mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == (
        (0.5, 0.0),
        (0.0, 0.5),
    )
    assert mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == 0.25

    n = mesh.quad_node_2()  # overwrite
    known = ((0.5, 0.0), (-0.3, 0.2))
    found = mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)
    assert all(k == pytest.approx(f) for (k, f) in zip(known, found))
    assert pytest.approx(mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)) == 0.1

    n = mesh.quad_node_3()  # overwrite
    known = ((0.2, -0.3), (-0.3, 0.2))
    found = mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)
    assert all(k == pytest.approx(f) for (k, f) in zip(known, found))
    assert (
        pytest.approx(mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)) == -0.05
    )

    n = mesh.quad_node_4()  # overwrite
    known = ((0.2, -0.3), (0.0, 0.5))
    found = mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)
    assert all(k == pytest.approx(f) for (k, f) in zip(known, found))

    assert pytest.approx(mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)) == 0.1
    assert (
        pytest.approx(mesh.det_jacobian_of_quad_check(xi=n.a, eta=n.b, vertices=cs))
        == 0.1
    )

    assert mesh.minimum_jacobian_of_quad(vertices=cs) == pytest.approx(-0.200)

    ls = mesh.perimeter_segment_lengths(coordinates=cs)
    assert ls == pytest.approx((1.0, 0.7211102550927979, 0.7211102550927979, 1.0))

    assert mesh.minimum_scaled_jacobian_of_quad(vertices=cs) == pytest.approx(
        -0.38461538461538486
    )

    # test principal axes
    a, b = mesh.principal_axes_of_quad(vertices=cs)
    assert a == pytest.approx((1.4, -0.6))
    assert b == pytest.approx((-0.6, 1.4))

    # test skew
    skew = mesh.skew_of_quad(vertices=cs)
    assert skew == pytest.approx(0.7241379310344829)
    # test aspect ratio
    ar = mesh.aspect_ratio_of_quad(vertices=cs)
    assert ar == 1.0


def test_quad_near_collapse():
    """Given a quadrilateral in 2D, verify the
    Jacobian matrix, evaluated at each of the four quad corners, quad has node 3 pushed inward
    to create a slight negative value in the Jacobian map.
    Verifies mimimum scaled Jacobian, skew, and aspect ratio.
    """
    cs = ((1.0, 1.0), (2.0, 1.0), (1.1, 1.1), (1.0, 2.0))
    # The det(J) = 1/80 * (2 - 9a - 9b)

    n = mesh.quad_node_1()
    assert mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == (
        (0.5, 0.0),
        (0.0, 0.5),
    )
    assert mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == 0.25

    n = mesh.quad_node_2()  # overwrite
    known = ((0.5, 0.0), (-0.45, 0.05))
    found = mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)
    assert all(k == pytest.approx(f) for (k, f) in zip(known, found))
    assert (
        pytest.approx(mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)) == 0.025
    )

    n = mesh.quad_node_3()  # overwrite
    known = ((0.05, -0.45), (-0.45, 0.05))
    found = mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)
    assert all(k == pytest.approx(f) for (k, f) in zip(known, found))
    assert (
        pytest.approx(mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)) == -0.2
    )

    n = mesh.quad_node_4()  # overwrite
    known = ((0.05, -0.45), (0.0, 0.5))
    found = mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)
    assert all(k == pytest.approx(f) for (k, f) in zip(known, found))

    assert (
        pytest.approx(mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)) == 0.025
    )
    assert (
        pytest.approx(mesh.det_jacobian_of_quad_check(xi=n.a, eta=n.b, vertices=cs))
        == 0.025
    )

    assert mesh.minimum_jacobian_of_quad(vertices=cs) == pytest.approx(-0.800)

    ls = mesh.perimeter_segment_lengths(coordinates=cs)
    assert ls == pytest.approx((1.0, 0.9055385138137416, 0.9055385138137416, 1.0))

    assert mesh.minimum_scaled_jacobian_of_quad(vertices=cs) == pytest.approx(
        -0.9756097560975608
    )

    # test principal axes
    a, b = mesh.principal_axes_of_quad(vertices=cs)
    assert a == pytest.approx((1.1, -0.9))
    assert b == pytest.approx((-0.9, 1.1))

    # test skew
    skew = mesh.skew_of_quad(vertices=cs)
    assert skew == pytest.approx(0.9801980198019803)
    # test aspect ratio
    ar = mesh.aspect_ratio_of_quad(vertices=cs)
    assert ar == 1.0


def test_quad_bowtie():
    """Given a quadrilateral in 2D, verify the
    Jacobian matrix, evaluated at each of the four quad corners, quad has
    node 2 and 3 inverted along the y-axis; the quad appears in a bowtie
    shape.
    Verifies mimimum scaled Jacobian, skew, and aspect ratio.
    """
    cs = ((1.0, 1.0), (2.0, 2.0), (2.0, 1.0), (1.0, 2.0))

    n = mesh.quad_node_1()  # overwrite
    assert mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == (
        (0.5, 0.5),
        (0.0, 0.5),
    )
    assert mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs) == 0.25
    assert mesh.det_jacobian_of_quad_check(xi=n.a, eta=n.b, vertices=cs) == 0.25

    n = mesh.quad_node_2()  # overwrite
    known = ((0.5, 0.5), (0.0, -0.5))
    found = mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)
    assert all(k == pytest.approx(f) for (k, f) in zip(known, found))
    assert (
        pytest.approx(mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)) == -0.25
    )
    assert mesh.det_jacobian_of_quad_check(xi=n.a, eta=n.b, vertices=cs) == -0.25

    n = mesh.quad_node_3()  # overwrite
    known = ((0.5, -0.5), (0.0, -0.5))
    found = mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)
    assert all(k == pytest.approx(f) for (k, f) in zip(known, found))
    assert (
        pytest.approx(mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)) == -0.25
    )
    assert mesh.det_jacobian_of_quad_check(xi=n.a, eta=n.b, vertices=cs) == -0.25

    n = mesh.quad_node_4()  # overwrite
    known = ((0.5, -0.5), (0.0, 0.5))
    found = mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)
    assert all(k == pytest.approx(f) for (k, f) in zip(known, found))

    assert (
        pytest.approx(mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)) == 0.25
    )
    assert mesh.det_jacobian_of_quad_check(xi=n.a, eta=n.b, vertices=cs) == 0.25

    # for the bowtie case, the Jacboian at the center of the
    # element should be zero, check this.
    n = mesh.quad_center()  # overwrite
    known = ((0.5, 0.0), (0.0, 0.0))
    found = mesh.jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)
    assert all(k == pytest.approx(f) for (k, f) in zip(known, found))

    assert pytest.approx(mesh.det_jacobian_of_quad(xi=n.a, eta=n.b, vertices=cs)) == 0.0
    assert (
        pytest.approx(mesh.det_jacobian_of_quad_check(xi=n.a, eta=n.b, vertices=cs))
        == 0.0
    )

    assert mesh.minimum_jacobian_of_quad(vertices=cs) == pytest.approx(-1.0)

    ls = mesh.perimeter_segment_lengths(coordinates=cs)
    assert ls == pytest.approx((1.4142135623730951, 1.0, 1.4142135623730951, 1.0))

    assert mesh.minimum_scaled_jacobian_of_quad(vertices=cs) == pytest.approx(
        -0.7071067811865475
    )

    # test principal axes
    a, b = mesh.principal_axes_of_quad(vertices=cs)
    assert a == pytest.approx((2.0, 0.0))
    assert b == pytest.approx((0.0, 0.0))

    # test skew
    skew = mesh.skew_of_quad(vertices=cs)
    assert isnan(skew)  # divide by zero nan
    # test aspect ratio
    ar = mesh.aspect_ratio_of_quad(vertices=cs)
    assert isinf(ar)  # divide by zero inf


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
