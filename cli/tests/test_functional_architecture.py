"""This module tests the `xyfigure.functional_architecture.py` module.

Example:
> conda activate siblenv
> cd ~/sibl
> pytest cli/tests/test_functional_architecture.py -rP
"""

# import numpy as np
from pathlib import Path  # stop using os.path, use pathlib instead

# import pytest

import xyfigure.functional_architecture as fa

#     f    g
#  a --> b --> c
#
# b = f(a)
# c = g(b)
# c = g(f(a))


# @pytest.mark.skip(reason="work in progress")
def test_Csv() -> fa.Csv:
    this_file = Path(__file__)
    this_path = this_file.resolve().parent

    test_file = "u-squared.csv"
    test_path = this_path.joinpath("differentiation").resolve()

    assert test_path.exists() and test_path.is_dir()

    test_file_pathed = Path.joinpath(test_path, test_file)
    assert test_file_pathed.exists()
    assert test_file_pathed.is_file()

    B = fa.Csv(filename=test_file, filepath=test_path)

    assert B.filename == test_file
    assert B.filetype == "csv"
    assert B.filepath == test_path

    return B


def test_csv_data():
    B = test_Csv()
    assert isinstance(B, fa.Csv)

    C = fa.csv_data(B)
    n_samples = 11  # number of samples
    # known_x = tuple(map(float, [x for x in range(n_samples)]))
    # known_y = tuple([0.5 * y ** 2 for y in range(n_samples)])
    known_x = tuple(map(float, range(n_samples)))
    known_y = tuple(map(lambda x: 0.5 * x ** 2, range(n_samples)))
    assert C.x == known_x
    assert C.y == known_y


def test_Figure():
    C0 = fa.csv_data(test_Csv())

    this_file = Path(__file__)
    this_path = this_file.resolve().parent

    test_file = "t-v-sines.csv"
    test_path = this_path.joinpath("differentiation").resolve()

    C1 = fa.csv_data(fa.Csv(filename=test_file, filepath=test_path))
    D = fa.Figure(
        series=(C0, C1), xmax=10, ymin=-2, ymax=50, filename="test_figure.pdf"
    )
    assert isinstance(D, fa.Figure)
    # fa.figure_save(D)


def main():
    test_Csv()
    test_csv_data()
    test_Figure()


# retain main for debugging this file in VS code
if __name__ == "__main__":
    # main()  # calls unittest.main() // no longer descend from unittest
    main()  # calls local main()
