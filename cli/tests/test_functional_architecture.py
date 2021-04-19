"""This module tests the `xyfigure.functional_architecture.py` module.

Example:
> conda activate siblenv
> cd ~/sibl
> pytest cli/tests/test_functional_architecture.py -rP
"""

# import numpy as np
from pathlib import Path  # stop using os.path, use pathlib instead

import pytest

import xyfigure.functional_architecture as fa


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
    known_x = tuple(map(float, [x for x in range(n_samples)]))
    known_y = tuple([0.5 * y ** 2 for y in range(n_samples)])
    assert C.x == known_x
    assert C.y == known_y


def main():
    test_Csv()
    test_csv_data()


# retain main for debugging this file in VS code
if __name__ == "__main__":
    # main()  # calls unittest.main()
    main()  # calls unittest.main()
