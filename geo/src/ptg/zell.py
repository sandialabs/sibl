from typing import Iterable, NamedTuple, Union


# Type alias for functional style methods
# https://docs.python.org/3/library/typing.html#type-aliases


class Zell(NamedTuple):
    level: int
    parent: Union[None, str]  # [None | str]
    # children: Union[
    #     None, tuple[Zell, Zell, Zell, Zell]
    # ]  # [bool | tuple(int, int, int, int)]
    children: Union[None, Iterable]  # [bool | tuple(int, int, int, int)]
    hash: str


Children = tuple[Zell, Zell, Zell, Zell]


# def subdivide(*, cell: Zell) -> tuple[Zell, Children]:
def subdivide(*, cell: Zell):

    # create four children
    child_level = cell.level + 1
    n_children = 4
    children = ()

    for c in range(n_children):
        child_id = format(c, "b").rjust(2, "0")
        if cell.hash == "0":  # the parent is the root
            child_hash = child_id
        else:  # the parent is not the root
            child_hash = cell.hash + child_id

        c = Zell(level=child_level, parent=cell.hash, children=None, hash=child_hash)
        children = children + (c,)

    # recreate the parent
    cell_as_parent = Zell(
        level=cell.level, parent=cell.parent, children=children, hash=cell.hash
    )

    return (cell_as_parent, children)
