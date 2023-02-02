# from ptg.zell import Zell
import ptg.zell as pz


def test_tree_with_one_division():
    root = pz.Zell(level=0, parent=None, children=None, hash="0")

    # level 1
    cell, children = pz.subdivide(cell=root)

    assert cell.level == 0
    assert cell.parent is None
    assert cell.children is not None
    assert cell.hash == "0"

    assert len(children) == 4
    for i, c in enumerate(children):
        assert c.level == 1
        assert c.parent == "0"
        assert c.children is None
        assert c.hash == format(i, "b").rjust(2, "0")

    # Now test subdivision of the cell's fourth child
    cell, children = pz.subdivide(cell=children[3])  # overwrite cell, children

    assert cell.level == 1
    assert cell.parent == "0"  # the orignal root node
    assert cell.children is not None
    assert cell.hash == "11"

    assert len(children) == 4
    for i, c in enumerate(children):
        assert c.level == 2
        assert c.parent == "11"
        assert c.children is None
        assert c.hash == c.parent + format(i, "b").rjust(2, "0")


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
