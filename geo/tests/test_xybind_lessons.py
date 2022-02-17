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

from pathlib import Path

# from ptg import dual as ptg_main
# from ptg import dual as ptg_dual
# from ptg import main

from ptg import main as ptg_main


def test_lesson_04():
    """Tests that Lesson 04 can be run from the command line
    to completion.
    """
    # argv = ["--input-file", "geo/data/mesh/lesson_04.yml"]

    # remember to suppress production of "lesson_04.png"
    # io = "geo/data/mesh/lesson_04.yml"
    io = str(Path("~/sibl/geo/doc/dual/lesson_04/lesson_04.yml").expanduser())
    completed = ptg_main.dualize(input_path_file=io)
    assert completed


def test_lesson_10():
    """Tests that Lesson 10 can be run from the command line
    to completion.
    """
    # argv = ["--input-file", "geo/data/mesh/lesson_10.yml"]

    # remember to suppress production of "lesson_10.png"
    # io = "geo/data/mesh/lesson_10.yml"
    io = str(Path("~/sibl/geo/doc/dual/lesson_10/lesson_10.yml").expanduser())
    completed = ptg_main.dualize(input_path_file=io)
    assert completed
