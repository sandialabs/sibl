"""This module tests operation and coverage of the copyright module.

To run
$ conda activate siblenv
$ cd ~/sibl
$ pytest geo/tests/test_copyright.py -v
$ pytest geo/tests/test_copyright.py -v --cov=geo/src/ptg --cov-report term-missing
"""

from pathlib import Path
from shutil import copyfile

import ptg.copyright as cr


def test_text_block():
    """Test that the text block of the copyright is as expected."""

    known = "Copyright 2020 National Technology and Engineering Solutions of Sandia, LLC (NTESS).\nUnder the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains\ncertain rights in this software."

    found = cr.text_block()

    assert known == found


def test_invalid_path():
    """If a bad path is provided, then False is returned."""
    aa = Path("/this/is_an_invented/bad/path")
    assert not cr.input_path(aa)


def test_valid_path():
    """If a valid path is provided, then True is returned."""
    aa = Path(__file__)
    bb = aa.parent
    assert cr.input_path(bb)

    cc = bb.parent.joinpath("src", "ptg")
    assert cr.input_path(cc)

    dd = cr.modules_list(bb)
    assert aa in dd


def test_copyright_exists():
    """Given two test files, one with a copyright block and one without,
    verify that the function returns True and False, respectively.
    """
    aa = Path(__file__).parent.joinpath("files")

    bb = aa.joinpath("copyright_exists.py")
    assert bb.is_file()
    assert cr.copyright_exists(bb)

    cc = aa.joinpath("copyright_not_exist.py")
    assert cc.is_file()
    assert not cr.copyright_exists(cc)  # assert no copyright in this file


def test_prepend_copyright():
    """Given a test file without a copyright, insert a copyright block and verify
    the copyright exists in the mutated file.
    """
    aa = Path(__file__).parent.joinpath("files")
    bb = aa.joinpath("copyright_not_exist.py")

    # Make a clone of bb, check it has no copyright, prepend, check it now
    # does have a copyright, then delete the cloned file.
    cc = aa.joinpath((str(bb) + ".clone"))
    copyfile(src=bb, dst=cc)

    assert not cr.copyright_exists(cc)  # assert first that it does not exist
    cr.prepend_copyright(cc)
    assert cr.copyright_exists(cc)

    # delete the temporary cloned file
    cc.unlink()
    assert not cc.is_file()
