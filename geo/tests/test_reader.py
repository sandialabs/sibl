"""This module tests the yml_reader service.

To run
> conda activate siblenv
> cd ~/sibl/geo
#
# pytest (without code coverage)
> pytest tests/test_yml_reader.py -v
#
# pytest (with code coverage)
> pytest --cov=src/ptg --cov-report term-missing
"""

# import pytest

# import yaml

from ptg import reader as reader


def test_lesson_04():
    """
    Tests the ability to read lesson_04.yml.
    """
    argv = "geo/data/mesh/lesson_04.yml"

    r = reader.Reader(input_file=argv)
    found = r.extract(key="version")
    known = 1.0  # version 1.0 of the input file
    assert found == known


# def test_extract_fails():
#     """
#     Testing ability of Reader object to extract specific
#     portions of the larger input .yml database
#     """
#     argv = "input/example.yml"
#
#     gr = reader.Reader(input_file=argv)
#     grDict = gr.extract(key="Chadbucks")
#     assert len(grDict) == 0
#
#
# def test_extract_deep():
#     """Testing that deep extraction with nested keys works."""
#     argv = "input/example.yml"
#
#     gr = reader.Reader(input_file=argv)
#
#     found = gr.extract_deep(keys=("person_object", "name"))
#     known = "Jason Smith"
#     assert found == known
#
#     found = gr.extract_deep(keys=("person_object", "age"))
#     known = 26
#     assert found == known
#
#     # with a key, get values
#     found = gr.extract_deep(keys=("person_object", "hobbies"))
#     known = ["hockey", "cooking", "quilting"]
#     assert found == known
#
#     # with a key, get a subdictionary
#     found = gr.extract_deep(keys=("person_object", "manager"))
#     known = {
#         "name": "Jessica Davis",
#         "age": 45,
#         "hobbies": ["fishing", "tennis", "golf"],
#         "manager": None,
#     }
#     assert found == known
#
#     # with a bad key, get an empty dictionary
#     found = gr.extract_deep(keys=("bad_key", "name"))
#     known = {}
#     assert len(found) == 0
#     assert found == known
#
#     found = gr.extract_deep(keys=("narrative",))
#     known = "This is a multi-line example; this is line 1\nand this is line 2, and finally\nthis is line 3.\n"
#     assert found == known
