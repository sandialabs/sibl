"""This module tests that lessons using xybind and
a yml input file run to completion.

To run
> conda activate siblenv
> cd ~/sibl

To run a single test, for example, the `test_lesson_04 test:
> pytest geo/tests/test_xybind_lessons.py::test_lesson_04 -v  # to run a single test

To run all tests in this module:
> pytest geo/tests/test_xybind_lessons.py -v  # to run all tests
"""

import pytest

from ptg import main as ptg_main


@pytest.mark.skip("TODO: make thread safe.")
def test_lesson_04():
    """Tests that Lesson 04 can be run from the command line to completion."""
    # argv = ["--input-file", "geo/data/mesh/lesson_04.yml"]

    # remember to suppress production of "lesson_04.png"
    # io = "geo/data/mesh/lesson_04.yml"
    # io = str(Path("~/sibl/geo/doc/dual/lesson_04/lesson_04.yml").expanduser())
    io = "geo/doc/dual/lesson_04/lesson_04.yml"
    completed = ptg_main.dualize(input_path_file=io)
    assert completed


@pytest.mark.skip("TODO: make thread safe.")
def test_lesson_10():
    """Tests that Lesson 10 can be run from the command line to completion."""
    # argv = ["--input-file", "geo/data/mesh/lesson_10.yml"]

    # remember to suppress production of "lesson_10.png"
    # io = "geo/data/mesh/lesson_10.yml"
    # io = str(Path("~/sibl/geo/doc/dual/lesson_10/lesson_10.yml").expanduser())
    io = "geo/doc/dual/lesson_04/lesson_04.yml"
    completed = ptg_main.dualize(input_path_file=io)
    assert completed


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
