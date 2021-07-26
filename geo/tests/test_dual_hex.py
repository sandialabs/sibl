"""This module is a unit test of the dual_hex implementation.

To run
> conda activate siblenv
> cd ~/sibl
> pytest geo/tests/test_dual_hex.py -v
"""

import ptg.dual_hex as dhex


def test_flat_scheme():
    flat = dhex.Flat()
    assert flat

    known_vertices = (
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (1.0, 1.0, 0.0),
        (0.0, 0.0, 1.0),
        (1.0, 0.0, 1.0),
        (0.0, 1.0, 1.0),
        (1.0, 1.0, 1.0),
        (0.0, 0.3, 0.0),
        (0.5, 0.0, 0.5),
        (0.0, 0.0, 0.5),
        (1.0, 0.0, 0.5),
        (0.0, 0.5, 0.0),
        (0.5, 0.3, 0.0),
        (1.0, 0.5, 0.0),
        (0.5, 0.0, 1.0),
        (0.5, 0.0, 0.0),
        (0.0, 0.5, 1.0),
    )

    known_polygons = (
        (5, 6, 8, 10, 2),
        (6, 7, 9, 11, 3),
        (10, 13, 12, 16, 17, 0),
        (11, 17, 15, 19, 18, 14, 4, 1),
    )

    known_faces = (
        (10, 4, 15, 9),
        (9, 15, 5, 11),
        (0, 10, 9, 16),
        (16, 9, 11, 1),
        (6, 7, 3, 2),
        (10, 0, 8),
        (9, 16, 13),
        (11, 1, 14),
        (0, 16, 13, 8),
        (16, 1, 14, 13),
        (10, 9, 13, 8),
        (9, 11, 14, 13),
        (4, 15, 17),
        (8, 13, 12),
        (17, 12, 2, 6),
        (12, 13, 14, 3, 2),
        (8, 10, 4, 17, 12),
        (13, 9, 15, 17, 12),
        (5, 15, 17, 6, 7),
        (11, 5, 7, 3, 14),
    )

    coded_vertices = flat.vertices
    coded_faces = flat.faces
    coded_polygons = flat.polygons

    assert known_vertices == coded_vertices
    assert known_faces == coded_faces
    assert known_polygons == coded_polygons
