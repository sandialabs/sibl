"""This module creates all the NamedTuple tupes of models and views
used to create figures.
"""

from typing import NamedTuple
from pathlib import Path


class Kwargs(NamedTuple):
    """The keyword arguments, kwargs, forwarded to Matplotlib."""

    alpha: float = 0.5
    color: str = "blue"
    label: str = "label"
    linestyle: str = "-"
    linewidth: int = 2


class Model(NamedTuple):
    """The basic ingredients to create a single (x, y) trace."""

    folder: Path
    file: Path
    plot_kwargs: Kwargs
    skip_rows: int = 1
    ycolumn: int = 1


class RhsAxis(NamedTuple):
    """The constituents of a right hand side vertical axis."""

    scale: float
    label: str
    yticks: list[float] | None


class View(NamedTuple):
    """The plot on which the models are placed."""

    folder: Path
    file: Path
    size: list[float]
    title: str
    ylabel: str
    yaxis_rhs: RhsAxis | None
    details: bool = False
    display: bool = True
    dpi: int = 300
    latex: bool = False
    serialize: bool = False
