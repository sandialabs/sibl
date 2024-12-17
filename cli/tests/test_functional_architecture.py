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

#  a=f(b) b=g(c)
#  a --> b --> c
#
# b = f(a)
# c = g(b)
# c = g(f(a))


# @pytest.mark.skip(reason="work in progress")
# def test_Csv() -> fa.Csv:
def the_csv() -> fa.Csv:
    """Helper function."""
    this_file = Path(__file__)
    this_path = this_file.resolve().parent

    test_file = "u-squared.csv"
    test_path = this_path.joinpath("differentiation").resolve()

    assert test_path.exists() and test_path.is_dir()

    test_file_pathed = Path.joinpath(test_path, test_file)
    assert test_file_pathed.exists()
    assert test_file_pathed.is_file()

    bb = fa.Csv(filename=test_file, filepath=str(test_path))

    assert bb.filename == test_file
    assert bb.filetype == "csv"
    assert bb.filepath == str(test_path)

    return bb


def test_csv_data():
    """
    Test the functionality of the CSV data handling.

    This function verifies that the CSV data is correctly loaded and processed
    by checking the type of the loaded data and asserting that the expected
    values for x and y coordinates match the computed values.

    It performs the following checks:
    - Asserts that the loaded CSV data is an instance of the `fa.Csv` class.
    - Asserts that the x values are equal to a known tuple of float values
      generated from a range of sample indices.
    - Asserts that the y values are equal to a known tuple of values computed
      as 0.5 times the square of the corresponding x values.

    Raises:
        AssertionError: If any of the assertions fail, indicating that the
        CSV data does not match the expected format or values.
    """
    # B = test_Csv()
    bb = the_csv()
    assert isinstance(bb, fa.Csv)

    cc = fa.csv_data(bb)
    n_samples = 11  # number of samples
    # known_x = tuple(map(float, [x for x in range(n_samples)]))
    # known_y = tuple([0.5 * y ** 2 for y in range(n_samples)])
    known_x = tuple(map(float, range(n_samples)))
    known_y = tuple(map(lambda x: 0.5 * x**2, range(n_samples)))
    assert cc.x == known_x
    assert cc.y == known_y


def test_Figure():
    """
    Test the functionality of the Figure class in the fa module.

    This function verifies that a Figure object can be created using
    CSV data loaded from two different sources. It checks that the
    Figure object is correctly instantiated with the specified parameters.

    The function performs the following steps:
    - Loads CSV data from a test CSV file using the `fa.csv_data` function.
    - Resolves the path to the current file and constructs the path to the
      directory containing the test CSV file.
    - Loads another set of CSV data from a specified test file located in
      the "differentiation" directory.
    - Creates a Figure object using the loaded CSV data, specifying the
      x-axis maximum and y-axis minimum and maximum values, as well as the
      filename for saving the figure.

    Raises:
        AssertionError: If the created Figure object is not an instance of
        the `fa.Figure` class, indicating that the figure was not created
        successfully.
    """
    # c0 = fa.csv_data(test_Csv())
    c0 = fa.csv_data(the_csv())

    this_file = Path(__file__)
    this_path = this_file.resolve().parent

    test_file = "t-v-sines.csv"
    test_path = this_path.joinpath("differentiation").resolve()

    c1 = fa.csv_data(fa.Csv(filename=test_file, filepath=str(test_path)))
    dd = fa.Figure(
        series=(c0, c1), xmax=10, ymin=-2, ymax=50, filename="test_figure.pdf"
    )
    assert isinstance(dd, fa.Figure)
    # fa.figure_save(D)


def main():
    """The main entry point."""
    # test_Csv()
    test_csv_data()
    test_Figure()


# retain main for debugging this file in VS code
if __name__ == "__main__":
    # main()  # calls unittest.main() // no longer descend from unittest
    main()  # calls local main()


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
