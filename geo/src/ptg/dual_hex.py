from typing import NamedTuple, Tuple
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.ticker import MultipleLocator
from pathlib import Path

DISPLAY = True
LATEX = 0
SERIALIZE = False

# From https://github.com/mlivesu/cinolib/blob/master/include/cinolib/hex_transition_schemes.h
# the same data scheme is followed here


class Flat(NamedTuple):
    """Creates the Flat (F) data structure.

    Attributes:
        vertices (list[float]): The (x, y, z) positions of vertices on the unit cube.
        faces (list[float]): The triagular, quadrilateral, or pentagonal faces
            composed of a sequence of integer node numbers.
        polygons (list[float]): The n-gon volumes composed of a sequence of
            integer node numbers.
    """

    vertices: Tuple(Tuple[float]) = (
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

    faces: tuple[int] = (
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

    polygons: tuple[int] = (
        (5, 6, 8, 10, 2),
        (6, 7, 9, 11, 3),
        (10, 13, 12, 16, 17, 0),
        (11, 17, 15, 19, 18, 14, 4, 1),
    )
