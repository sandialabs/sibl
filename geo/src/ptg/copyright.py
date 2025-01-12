# Copyright 2020 National Technology and Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
# certain rights in this software.


"""

This module checks if a copyright assertion text block exists in
the file(s) contained within a path, recursively.

If the text block does not exist in a particular file, the text block will be
appended.

Returns True if the append operation was successful, or the text block already
exists; returns False otherwise (the text block did not exist, the append
operation was attempted but failed.)
"""

from pathlib import Path
from shutil import copyfile
from typing import Final


def text_block() -> str:
    copyright_text: Final = (
        "# Copyright 2020 National Technology and Engineering Solutions of Sandia, LLC (NTESS).\n# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains\n# certain rights in this software.\n"
    )
    return copyright_text


def input_path(path: Path) -> bool:
    """Sets the input path, returns True if the set operation was successful;
    returns False otherwise.
    """
    path_exists = False
    path_exists = path.expanduser().is_dir()
    return path_exists


def modules_list(path: Path) -> list[Path]:
    return list(path.glob("*.py"))


def copyright_exists(path: Path) -> bool:
    """Given a single python file as a Path, returns True if the copyright
    block is contained in the python file, returns False otherwise.
    """
    copyright_exists = False

    with open(path, mode="r") as fin:
        contents = fin.read()
        if text_block() in contents:
            copyright_exists = True  # overwrite

    return copyright_exists


def prepend_copyright(path: Path) -> bool:
    """Given a Python file, prepends the copyright block."""
    prepend_success = False

    # path_temp = path.joinpath("temp")
    path_temp = Path(str(path) + ".temp")

    with open(path, mode="r") as fin:
        contents = fin.read()
        contents_new = text_block() + "\n\n" + contents
        with open(path_temp, mode="w") as fout:
            fout.write(contents_new)

        # overwrite old original file with new temp file
        copyfile(src=path_temp, dst=path)

        # remove the new temp file
        path_temp.unlink()

        prepend_success = True  # overwrite

    return prepend_success


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
