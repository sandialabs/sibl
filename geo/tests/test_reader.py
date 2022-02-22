"""This module tests the yml_reader service.

To run
> conda activate siblenv
> cd ~/sibl
#
# pytest (without code coverage)
> pytest geo/tests/test_reader.py -v
#
# pytest (with code coverage)
> pytest --cov=src/ptg --cov-report term-missing
"""

# import os

# import pytest

# import yaml

# from ptg import reader as reader
import ptg.main as ptg_main


def test_lesson_04_and_version_number():
    """Tests the ability to read lesson_04.yml."""
    ptg_main.dualize(input_path_file="geo/doc/dual/lesson_04/lesson_04.yml")
